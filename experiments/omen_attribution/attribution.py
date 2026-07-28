"""Unequal causal hypotheses and evidence-sensitive attribution support."""

from __future__ import annotations

from dataclasses import dataclass

from .source_model import (
    CausalVariable,
    Correspondence,
    Event,
    Evidence,
    EvidenceKind,
    Hypothesis,
    HypothesisKind,
)


def make_hypotheses() -> tuple[Hypothesis, ...]:
    return (
        Hypothesis(
            HypothesisKind.CHANCE,
            "the baseline process produced the matching event",
            frozenset({CausalVariable.BASELINE_PROCESS}),
            frozenset({"baseline-rate"}),
            6,
        ),
        Hypothesis(
            HypothesisKind.SELECTION,
            "selective observation made a baseline match appear exceptional",
            frozenset({CausalVariable.REPORTING_FILTER}),
            frozenset({EvidenceKind.COMPLETE_STREAM.value}),
            4,
        ),
        Hypothesis(
            HypothesisKind.BEHAVIOR,
            "the recorded aim changed operator behavior and thereby the outcome",
            frozenset(
                {
                    CausalVariable.OPERATOR_ATTENTION,
                    CausalVariable.OPERATOR_BEHAVIOR,
                }
            ),
            frozenset({EvidenceKind.ACTION_LOG.value, EvidenceKind.INTERVENTION.value}),
            3,
        ),
        Hypothesis(
            HypothesisKind.SOCIAL_RESPONSE,
            "another person responded to signals from the operator",
            frozenset(
                {
                    CausalVariable.OPERATOR_SIGNAL,
                    CausalVariable.OTHER_PERSON_RESPONSE,
                }
            ),
            frozenset({EvidenceKind.RESPONSE_LOG.value}),
            2,
        ),
        Hypothesis(
            HypothesisKind.SELF_ORGANIZATION,
            "environmental dynamics produced the correspondence",
            frozenset({CausalVariable.ENVIRONMENTAL_DYNAMICS}),
            frozenset({EvidenceKind.ENVIRONMENTAL_RECORD.value}),
            3,
        ),
        Hypothesis(
            HypothesisKind.ANOMALOUS,
            "an unknown mediator caused the correspondence",
            frozenset({CausalVariable.UNKNOWN_MEDIATOR}),
            frozenset({EvidenceKind.ELIMINATION_RECORD.value}),
            0,
        ),
    )


@dataclass(frozen=True, slots=True)
class SupportRecord:
    hypothesis: Hypothesis
    score: int
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AttributionReport:
    event: Event
    correspondence: Correspondence
    support: tuple[SupportRecord, ...]
    used_evidence: frozenset[Evidence]
    selected: HypothesisKind | None
    underdetermined: bool


@dataclass(frozen=True, slots=True)
class EvidenceConflict:
    subject: str
    evidence: frozenset[Evidence]
    hypothesis: HypothesisKind
    reason: str


type AttributionResult = AttributionReport | EvidenceConflict


def _conflict(
    subject: str,
    evidence: frozenset[Evidence],
) -> EvidenceConflict | None:
    related = frozenset(item for item in evidence if item.subject == subject)
    for kind in EvidenceKind:
        same_kind = tuple(item for item in related if item.kind is kind)
        for hypothesis in HypothesisKind:
            supporting = any(hypothesis in item.supports for item in same_kind)
            weakening = any(hypothesis in item.weakens for item in same_kind)
            if supporting and weakening:
                return EvidenceConflict(
                    subject,
                    frozenset(same_kind),
                    hypothesis,
                    (
                        "equally classified evidence both supports and weakens one "
                        "attribution"
                    ),
                )
    return None


def attribute(
    event: Event,
    correspondence: Correspondence,
    hypotheses: tuple[Hypothesis, ...],
    evidence: frozenset[Evidence] = frozenset(),
) -> AttributionResult:
    conflict = _conflict(event.identifier, evidence)
    if conflict is not None:
        return conflict
    relevant = frozenset(item for item in evidence if item.subject == event.identifier)
    records: list[SupportRecord] = []
    for hypothesis in hypotheses:
        score = hypothesis.prior_support
        reasons = [f"prior support={hypothesis.prior_support}"]
        for item in relevant:
            if hypothesis.kind in item.supports:
                score += item.strength
                reasons.append(f"{item.identifier} supports +{item.strength}")
            if hypothesis.kind in item.weakens:
                score = max(0, score - item.strength)
                reasons.append(f"{item.identifier} weakens -{item.strength}")
        records.append(SupportRecord(hypothesis, score, tuple(reasons)))
    positive = tuple(record for record in records if record.score > 0)
    selected = positive[0].hypothesis.kind if len(positive) == 1 else None
    return AttributionReport(
        event,
        correspondence,
        tuple(records),
        relevant,
        selected,
        len(positive) != 1,
    )


def score(report: AttributionReport, kind: HypothesisKind) -> int:
    return next(item.score for item in report.support if item.hypothesis.kind is kind)
