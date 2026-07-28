"""Exact scenario assembly for the executable witness and evidence tests."""

from __future__ import annotations

from .assessment import admit_evidence, assess, exact_rule
from .cases import CALIBRATION_CASES, CALIBRATION_IDS, case_inputs
from .observations import observe
from .records import (
    Assessment,
    EvidenceSet,
    Intervention,
    InvalidEvidence,
    InvalidPlan,
    ModelVersion,
    Split,
    TrialBundle,
    WorldCase,
)
from .trials import (
    assemble_history,
    commit_predictions,
    make_plan,
    produce_outcomes,
)


def run_cases(
    identifier: str,
    version: ModelVersion,
    cases: tuple[WorldCase, ...],
    split: Split,
    *,
    intervention: Intervention | None = None,
) -> TrialBundle:
    inputs = case_inputs(cases)
    plan = make_plan(
        f"plan:{identifier}",
        version,
        inputs,
        split,
        intervention=intervention,
    )
    predictions = commit_predictions(plan, version, inputs)
    if isinstance(predictions, InvalidPlan):
        raise AssertionError(predictions.reason)
    occurrences = produce_outcomes(
        plan,
        predictions,
        cases,
        intervention=intervention,
    )
    if isinstance(occurrences, InvalidPlan):
        raise AssertionError(occurrences.reason)
    observations = observe(occurrences)
    history = assemble_history(predictions, occurrences, observations)
    return TrialBundle(plan, predictions, occurrences, observations, history)


def assess_bundle(identifier: str, bundle: TrialBundle) -> Assessment:
    result = assess(identifier, bundle.predictions, bundle.observations, exact_rule())
    if isinstance(result, InvalidEvidence):
        raise AssertionError(result.reason)
    return result


def calibration_evidence(
    version: ModelVersion,
) -> tuple[TrialBundle, Assessment, EvidenceSet]:
    bundle = run_cases("calibration", version, CALIBRATION_CASES, Split.CALIBRATION)
    assessment = assess_bundle("assessment:calibration", bundle)
    evidence = admit_evidence(
        "evidence:calibration",
        assessment,
        bundle.observations,
        admitted_case_identifiers=CALIBRATION_IDS,
    )
    if isinstance(evidence, InvalidEvidence):
        raise AssertionError(evidence.reason)
    return bundle, assessment, evidence
