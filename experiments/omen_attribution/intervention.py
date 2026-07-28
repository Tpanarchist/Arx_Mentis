"""A deterministic behavior-block intervention and its attribution evidence."""

from __future__ import annotations

from dataclasses import dataclass

from .source_model import (
    CausalVariable,
    Evidence,
    EvidenceKind,
    HypothesisKind,
    Intervention,
    RecordedAim,
    TrialSummary,
)


@dataclass(frozen=True, slots=True)
class InterventionRecord:
    intervention: Intervention
    before: TrialSummary
    after: TrialSummary
    evidence: Evidence


def block_operator_behavior(
    aim: RecordedAim,
    event_identifier: str,
) -> InterventionRecord:
    intervention = Intervention(
        "preserve aim and block operator behavior",
        frozenset({CausalVariable.OPERATOR_BEHAVIOR}),
        aim,
    )
    before = TrialSummary("behavior available", matches=4, trials=6)
    after = TrialSummary("behavior blocked", matches=1, trials=6)
    evidence = Evidence(
        "behavior-block-result",
        event_identifier,
        EvidenceKind.INTERVENTION,
        supports=frozenset({HypothesisKind.BEHAVIOR, HypothesisKind.SOCIAL_RESPONSE}),
        weakens=frozenset({HypothesisKind.CHANCE, HypothesisKind.SELF_ORGANIZATION}),
        strength=2,
        note="match count fell when operator behavior was blocked",
    )
    return InterventionRecord(intervention, before, after, evidence)
