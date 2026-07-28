"""Independent checker for Dialectica Effects and Demonstrations."""

from __future__ import annotations

from .model import (
    Ars,
    ConformityResult,
    Conforms,
    Context,
    Counterexample,
    Demonstration,
    Effect,
    Implication,
    InvalidDemonstration,
    Open,
    Proposition,
    PropositionResult,
    Refutation,
    RuleName,
    VerificationResult,
    VerifiedDemonstration,
)


def _valid_modus_ponens(
    premises: tuple[Proposition, ...],
    conclusion: Proposition,
) -> bool:
    if len(premises) != 2:
        return False
    first, second = premises
    return bool(
        (
            isinstance(first, Implication)
            and first.antecedent == second
            and first.consequent == conclusion
        )
        or (
            isinstance(second, Implication)
            and second.antecedent == first
            and second.consequent == conclusion
        )
    )


def verify_demonstration(effect: Effect, context: Context) -> VerificationResult:
    """Check premises, each rule use, and the reported conclusion from scratch."""

    demonstration = effect.demonstration
    if demonstration.starting_premises != effect.source.starting_premises:
        return InvalidDemonstration("starting premises differ from the Spell", None)
    if not demonstration.starting_premises <= context.premises:
        return InvalidDemonstration("a starting premise is absent from Context", None)

    declared_rules = {rule.name for rule in context.ars.rules}
    available = set(demonstration.starting_premises)
    for index, application in enumerate(demonstration.applications):
        if application.rule not in declared_rules:
            return InvalidDemonstration(
                "the applied rule is not declared by Ars",
                index,
            )
        if not set(application.premises) <= available:
            return InvalidDemonstration(
                "an application uses an unavailable premise",
                index,
            )
        valid = application.rule is RuleName.MODUS_PONENS and _valid_modus_ponens(
            application.premises,
            application.conclusion,
        )
        if not valid:
            return InvalidDemonstration("the rule does not yield its conclusion", index)
        available.add(application.conclusion)

    if not demonstration.applications:
        return InvalidDemonstration(
            "the claimed two-step proof has no applications",
            None,
        )
    if demonstration.applications[-1].conclusion != demonstration.conclusion:
        return InvalidDemonstration(
            "the trace and demonstration conclusions differ",
            None,
        )
    if demonstration.conclusion != effect.conclusion:
        return InvalidDemonstration(
            "the Demonstration does not establish the Effect",
            None,
        )
    return VerifiedDemonstration(
        demonstration,
        demonstration.starting_premises,
        len(demonstration.applications),
        effect.conclusion,
    )


def check_will(effect: Effect, ars: Ars) -> ConformityResult:
    """Run the Ars-declared finite Will comparison after construction."""

    if effect.conclusion == effect.source.will.expected:
        return Conforms(effect, effect.source.will, ars.equality)
    return Counterexample(
        effect,
        effect.source.will,
        "the validly constructed conclusion differs from Will",
    )


def decide(proposition: Proposition, context: Context) -> PropositionResult:
    """Distinguish a settled proposition from an unresolved proposition."""

    if proposition in context.premises:
        return Demonstration(context.premises, (), proposition)
    if proposition in context.refuted:
        return Refutation(proposition, "Context carries a counterexample")
    return Open(proposition, "neither demonstration nor refutation is available")
