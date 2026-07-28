"""Adversarial attempt to force unequal hypotheses into one symmetric frame."""

from __future__ import annotations

from dataclasses import dataclass

from .source_model import CausalVariable, Hypothesis, HypothesisKind


@dataclass(frozen=True, slots=True)
class StructuralSignature:
    variables: frozenset[CausalVariable]
    required_evidence: frozenset[str]
    prior_support: int


def signature(hypothesis: Hypothesis) -> StructuralSignature:
    return StructuralSignature(
        hypothesis.variables,
        hypothesis.required_evidence,
        hypothesis.prior_support,
    )


@dataclass(frozen=True, slots=True)
class AttemptedTransformation:
    source: HypothesisKind
    target: HypothesisKind
    preserves_structure: bool


@dataclass(frozen=True, slots=True)
class LawfulOrbit:
    structural_signature: StructuralSignature
    members: frozenset[HypothesisKind]


@dataclass(frozen=True, slots=True)
class SymmetryAttempt:
    transformations: tuple[AttemptedTransformation, ...]
    proposed_cycle_transitive: bool
    proposed_cycle_preserves_structure: bool
    lawful_orbits: tuple[LawfulOrbit, ...]
    lawful_relation_transitive: bool
    failures: tuple[str, ...]


def attempt_transitive_frame(
    hypotheses: tuple[Hypothesis, ...],
) -> SymmetryAttempt:
    by_kind = {item.kind: item for item in hypotheses}
    kinds = tuple(item.kind for item in hypotheses)
    transformations = tuple(
        AttemptedTransformation(
            source,
            kinds[(index + 1) % len(kinds)],
            signature(by_kind[source])
            == signature(by_kind[kinds[(index + 1) % len(kinds)]]),
        )
        for index, source in enumerate(kinds)
    )
    grouped: dict[StructuralSignature, set[HypothesisKind]] = {}
    for hypothesis in hypotheses:
        grouped.setdefault(signature(hypothesis), set()).add(hypothesis.kind)
    orbits = tuple(
        LawfulOrbit(structural_signature, frozenset(members))
        for structural_signature, members in grouped.items()
    )
    failures = tuple(
        (
            f"{item.source.value} -> {item.target.value} changes causal variables, "
            "evidence requirements, or prior support"
        )
        for item in transformations
        if not item.preserves_structure
    )
    return SymmetryAttempt(
        transformations,
        proposed_cycle_transitive=True,
        proposed_cycle_preserves_structure=all(
            item.preserves_structure for item in transformations
        ),
        lawful_orbits=orbits,
        lawful_relation_transitive=len(orbits) == 1,
        failures=failures,
    )
