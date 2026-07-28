"""Provisional inference production, intentionally independent of verification."""

from __future__ import annotations

from .model import (
    Context,
    Demonstration,
    Effect,
    ElaboratedSpell,
    Failed,
    FailureKind,
    Implication,
    InferenceApplication,
    Proposition,
    Refused,
    RuleName,
)


def _modus_ponens(
    premises: tuple[Proposition, ...],
) -> Proposition | None:
    if len(premises) != 2:
        return None
    first, second = premises
    if isinstance(first, Implication) and first.antecedent == second:
        return first.consequent
    if isinstance(second, Implication) and second.antecedent == first:
        return second.consequent
    return None


def cast(elaborated: ElaboratedSpell, context: Context) -> Effect | Refused | Failed:
    """Apply permitted rules and emit a Demonstration without verifying it."""

    missing_capabilities = elaborated.required_capabilities - context.permissions
    if missing_capabilities:
        missing = min(missing_capabilities, key=lambda capability: capability.name)
        return Refused(missing, "Context does not permit the required construction")

    missing_premises = elaborated.spell.starting_premises - context.premises
    if missing_premises:
        return Failed(
            FailureKind.MISSING_PREMISE,
            "the permitted Cast cannot begin without every starting premise",
            missing_premises,
        )

    available = set(elaborated.spell.starting_premises)
    applications: list[InferenceApplication] = []
    for instruction in elaborated.spell.instructions:
        unavailable = frozenset(instruction.premises) - available
        if unavailable:
            return Failed(
                FailureKind.INAPPLICABLE_RULE,
                "a declared rule application depends on an unavailable proposition",
                frozenset(unavailable),
            )
        conclusion: Proposition | None = None
        if instruction.rule is RuleName.MODUS_PONENS:
            conclusion = _modus_ponens(instruction.premises)
        if conclusion is None or conclusion != instruction.conclusion:
            return Failed(
                FailureKind.INAPPLICABLE_RULE,
                "the instruction is not an application of its declared rule",
                frozenset(instruction.premises),
            )
        applications.append(
            InferenceApplication(
                instruction.rule,
                instruction.premises,
                instruction.conclusion,
            )
        )
        available.add(instruction.conclusion)

    final = applications[-1].conclusion
    demonstration = Demonstration(
        elaborated.spell.starting_premises,
        tuple(applications),
        final,
    )
    return Effect(elaborated.spell, final, demonstration)
