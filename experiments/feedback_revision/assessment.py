"""Independent assessment, evidence admission, and reporting."""

from __future__ import annotations

from .records import (
    Assessment,
    AssessmentKind,
    AssessmentReport,
    AssessmentRule,
    CaseAssessment,
    Correction,
    EvidenceEntry,
    EvidenceSet,
    InvalidEvidence,
    Observation,
    Prediction,
    ReportKind,
)


def exact_rule(*, declared_order: int = 0) -> AssessmentRule:
    return AssessmentRule("exact-match", AssessmentKind.EXACT, declared_order)


def outcome_defined_rule(*, declared_order: int) -> AssessmentRule:
    return AssessmentRule(
        f"always-success:{declared_order}",
        AssessmentKind.ALWAYS_SUCCESS,
        declared_order,
    )


def assess(
    identifier: str,
    predictions: tuple[Prediction, ...],
    observations: tuple[Observation, ...],
    rule: AssessmentRule,
    *,
    created_order: int = 300,
) -> Assessment | InvalidEvidence:
    observation_by_case = {item.case_identifier: item for item in observations}
    if set(observation_by_case) != {item.case_identifier for item in predictions}:
        return InvalidEvidence(
            identifier, "predictions and observations cover different cases"
        )
    results = tuple(
        _assess_case(prediction, observation_by_case[prediction.case_identifier], rule)
        for prediction in predictions
    )
    return Assessment(
        identifier,
        predictions[0].model_version_identifier,
        rule,
        results,
        sum(item.accepted for item in results),
        len(results),
        created_order,
    )


def _assess_case(
    prediction: Prediction,
    observation: Observation,
    rule: AssessmentRule,
) -> CaseAssessment:
    accepted = prediction.outcome is observation.outcome
    if rule.kind is AssessmentKind.ALWAYS_SUCCESS:
        accepted = True
    return CaseAssessment(
        prediction.case_identifier,
        prediction.identifier,
        observation.identifier,
        prediction.outcome,
        observation.outcome,
        accepted,
    )


def admit_evidence(
    identifier: str,
    assessment: Assessment,
    observations: tuple[Observation, ...],
    *,
    admitted_case_identifiers: frozenset[str],
    admitted_order: int = 400,
) -> EvidenceSet | InvalidEvidence:
    observation_by_case = {item.case_identifier: item for item in observations}
    if not admitted_case_identifiers <= observation_by_case.keys():
        return InvalidEvidence(identifier, "admitted cases lack observations")
    entries = tuple(
        EvidenceEntry(
            result.case_identifier,
            observation_by_case[result.case_identifier].outcome,
            (observation_by_case[result.case_identifier].identifier,),
        )
        for result in assessment.cases
        if result.case_identifier in admitted_case_identifiers
    )
    return EvidenceSet(
        identifier,
        entries,
        assessment.identifier,
        admitted_order,
    )


def apply_correction(
    evidence: EvidenceSet,
    correction: Correction,
    *,
    identifier: str,
    admitted_order: int,
) -> EvidenceSet | InvalidEvidence:
    if correction.case_identifier not in {
        entry.case_identifier for entry in evidence.entries
    }:
        return InvalidEvidence(identifier, "correction concerns an unadmitted case")
    entries = tuple(
        EvidenceEntry(
            entry.case_identifier,
            correction.corrected_outcome,
            (*entry.source_record_identifiers, correction.identifier),
        )
        if entry.case_identifier == correction.case_identifier
        else entry
        for entry in evidence.entries
    )
    return EvidenceSet(
        identifier,
        entries,
        evidence.source_assessment_identifier,
        admitted_order,
        previous_evidence_set_identifier=evidence.identifier,
        correction_identifiers=(
            *evidence.correction_identifiers,
            correction.identifier,
        ),
    )


def reassess_from_evidence(
    identifier: str,
    predictions: tuple[Prediction, ...],
    evidence: EvidenceSet,
    rule: AssessmentRule,
    *,
    created_order: int,
) -> Assessment | InvalidEvidence:
    prediction_by_case = {item.case_identifier: item for item in predictions}
    if (
        not {entry.case_identifier for entry in evidence.entries}
        <= prediction_by_case.keys()
    ):
        return InvalidEvidence(
            identifier, "evidence refers to cases without predictions"
        )
    observations = tuple(
        Observation(
            f"admissible:{evidence.identifier}:{entry.case_identifier}",
            entry.source_record_identifiers[-1],
            prediction_by_case[entry.case_identifier].identifier,
            entry.case_identifier,
            entry.effective_outcome,
            evidence.admitted_order,
        )
        for entry in evidence.entries
    )
    selected_predictions = tuple(
        prediction_by_case[entry.case_identifier] for entry in evidence.entries
    )
    return assess(
        identifier,
        selected_predictions,
        observations,
        rule,
        created_order=created_order,
    )


def report_assessment(
    assessment: Assessment,
    kind: ReportKind,
) -> AssessmentReport:
    included = tuple(
        item.case_identifier
        for item in assessment.cases
        if kind is ReportKind.ALL or item.accepted
    )
    return AssessmentReport(
        f"report:{assessment.identifier}:{kind.value}",
        kind,
        assessment,
        included,
    )
