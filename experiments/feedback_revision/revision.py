"""Prospective, evidence-bounded construction of persistent model versions."""

from __future__ import annotations

from .cases import CALIBRATION_IDS
from .records import (
    Assessment,
    EvidenceLeakage,
    EvidenceSet,
    Lineage,
    Model,
    ModelKind,
    ModelVersion,
    NoRevision,
    Outcome,
    Revision,
    RevisionConflict,
    RevisionKind,
    RevisionRule,
    ScoredRevision,
    SelectedRevision,
    SelectionKind,
    SelectionPolicy,
)


def revision_rule(
    identifier: str,
    kind: RevisionKind,
    *,
    admissible_case_identifiers: frozenset[str] = CALIBRATION_IDS,
    declared_order: int = 450,
) -> RevisionRule:
    return RevisionRule(
        identifier,
        kind,
        admissible_case_identifiers,
        declared_order,
    )


def decline_revision(
    source: ModelVersion,
    assessment: Assessment,
) -> NoRevision:
    return NoRevision(
        source,
        evidence_set_identifier=None,
        rule_identifier=None,
        evidence_evaluated=False,
        reason=(
            f"assessment {assessment.identifier} recorded; model continues unchanged"
        ),
    )


def revise(
    source: ModelVersion,
    evidence: EvidenceSet,
    rule: RevisionRule,
    *,
    created_order: int = 500,
) -> Revision | NoRevision | EvidenceLeakage:
    evidence_cases = frozenset(entry.case_identifier for entry in evidence.entries)
    forbidden = evidence_cases - rule.admissible_case_identifiers
    if forbidden:
        return EvidenceLeakage(
            source,
            evidence,
            rule,
            forbidden,
            "revision evidence crosses the rule's admitted calibration boundary",
        )
    if rule.kind is RevisionKind.NO_OP:
        return NoRevision(
            source,
            evidence.identifier,
            rule.identifier,
            evidence_evaluated=True,
            reason="revision rule found no model change",
        )

    model = _construct_model(rule, evidence)
    lineage = Lineage(
        source.identifier,
        evidence.identifier,
        rule.identifier,
        created_order,
    )
    result_version = ModelVersion(
        f"{source.identifier}->{rule.identifier}",
        model,
        source.ordinal + 1,
        lineage,
    )
    return Revision(
        f"revision:{source.identifier}:{rule.identifier}",
        source,
        evidence,
        rule,
        result_version,
        created_order,
    )


def _construct_model(rule: RevisionRule, evidence: EvidenceSet) -> Model:
    if rule.kind is RevisionKind.GENERALIZE_XOR:
        return Model("generalized-xor", ModelKind.XOR, (), complexity=2)
    if rule.kind is RevisionKind.EQUIVALENT_LOOKUP:
        return Model(
            "equivalent-feature-lookup",
            ModelKind.FEATURE_LOOKUP,
            (
                ("00", Outcome.NEGATIVE),
                ("01", Outcome.POSITIVE),
                ("10", Outcome.POSITIVE),
                ("11", Outcome.NEGATIVE),
            ),
            complexity=4,
        )
    if rule.kind is RevisionKind.OVERFIT_MEMORIZE:
        return Model(
            "calibration-memorizer",
            ModelKind.MEMORIZE,
            tuple(
                (entry.case_identifier, entry.effective_outcome)
                for entry in evidence.entries
            ),
            complexity=len(evidence.entries) + 1,
        )
    raise AssertionError(f"unhandled revision kind: {rule.kind}")


def scored_revision(
    revision: Revision,
    calibration: Assessment,
    holdout: Assessment,
) -> ScoredRevision:
    if calibration.model_version_identifier != revision.result_version.identifier:
        raise ValueError("calibration assessment belongs to another model version")
    if holdout.model_version_identifier != revision.result_version.identifier:
        raise ValueError("holdout assessment belongs to another model version")
    return ScoredRevision(
        revision,
        (calibration.accepted_count, calibration.total_count),
        (holdout.accepted_count, holdout.total_count),
    )


def select_revision(
    candidates: tuple[ScoredRevision, ...],
    policy: SelectionPolicy | None = None,
) -> RevisionConflict | SelectedRevision:
    best_score = max(candidate.holdout_score for candidate in candidates)
    leaders = tuple(
        candidate for candidate in candidates if candidate.holdout_score == best_score
    )
    if len(leaders) == 1:
        return SelectedRevision(
            leaders[0],
            SelectionPolicy(
                "higher-holdout-score",
                SelectionKind.HIGHER_HOLDOUT_SCORE,
            ),
            "declared primary holdout score has one leader",
        )
    if policy is None:
        return RevisionConflict(
            frozenset(item.revision.identifier for item in leaders),
            best_score,
            "equal score provides no discriminator and no secondary policy is declared",
        )
    if policy.kind is SelectionKind.LOWER_COMPLEXITY:
        least = min(item.revision.result_version.model.complexity for item in leaders)
        simplest = tuple(
            item
            for item in leaders
            if item.revision.result_version.model.complexity == least
        )
        if len(simplest) == 1:
            return SelectedRevision(
                simplest[0],
                policy,
                "declared lower-complexity policy uniquely discriminates",
            )
    return RevisionConflict(
        frozenset(item.revision.identifier for item in leaders),
        best_score,
        "declared secondary policy does not produce a unique leader",
    )
