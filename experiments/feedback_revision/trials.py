"""Precommitted prediction and later outcome production."""

from __future__ import annotations

from .models import predict
from .records import (
    CaseInput,
    CausalRecord,
    HistoricalTrial,
    Intervention,
    InterventionKind,
    InvalidPlan,
    MechanismKind,
    ModelVersion,
    Observation,
    Prediction,
    Split,
    TrialOccurrence,
    TrialPlan,
    WorldCase,
)


def make_plan(
    identifier: str,
    version: ModelVersion,
    cases: tuple[CaseInput, ...],
    split: Split,
    *,
    assessment_rule_identifier: str = "exact-match",
    intervention: Intervention | None = None,
    committed_order: int = 0,
) -> TrialPlan:
    return TrialPlan(
        identifier,
        version.identifier,
        tuple(case.identifier for case in cases),
        split,
        assessment_rule_identifier,
        intervention.identifier if intervention else None,
        committed_order,
    )


def commit_predictions(
    plan: TrialPlan,
    version: ModelVersion,
    cases: tuple[CaseInput, ...],
) -> tuple[Prediction, ...] | InvalidPlan:
    if plan.model_version_identifier != version.identifier:
        return InvalidPlan(plan, "plan and model-version identifiers differ")
    if plan.outcomes_exposed_at_commit:
        return InvalidPlan(
            plan, "predictions must be committed before outcomes are exposed"
        )
    if tuple(case.identifier for case in cases) != plan.case_identifiers:
        return InvalidPlan(plan, "plan and supplied case inputs differ")
    return tuple(
        Prediction(
            f"prediction:{plan.identifier}:{case.identifier}",
            plan.identifier,
            version.identifier,
            case.identifier,
            predict(version.model, case),
            plan.committed_order + index + 1,
        )
        for index, case in enumerate(cases)
    )


def derive_intervention(
    version: ModelVersion,
    *,
    declared_order: int = 50,
) -> Intervention:
    return Intervention(
        f"align-to:{version.identifier}",
        version.identifier,
        InterventionKind.ALIGN_TO_PREDICTION,
        declared_order,
    )


def produce_outcomes(
    plan: TrialPlan,
    predictions: tuple[Prediction, ...],
    cases: tuple[WorldCase, ...],
    *,
    intervention: Intervention | None = None,
    occurred_order_base: int = 100,
) -> tuple[TrialOccurrence, ...] | InvalidPlan:
    if tuple(item.case_identifier for item in predictions) != plan.case_identifiers:
        return InvalidPlan(plan, "predictions do not cover the planned cases")
    if tuple(case.identifier for case in cases) != plan.case_identifiers:
        return InvalidPlan(plan, "world cases do not cover the planned cases")
    supplied_intervention = intervention.identifier if intervention else None
    if supplied_intervention != plan.intervention_identifier:
        return InvalidPlan(plan, "plan and supplied intervention differ")
    if intervention and (
        intervention.source_model_version_identifier != plan.model_version_identifier
    ):
        return InvalidPlan(plan, "intervention derives from another model version")

    occurrences: list[TrialOccurrence] = []
    for index, (prediction, case) in enumerate(zip(predictions, cases, strict=True)):
        produced = case.outcome
        mechanism = MechanismKind.PASSIVE
        if intervention:
            produced = prediction.outcome
            mechanism = MechanismKind.ADAPTIVE_INTERVENTION
        causal_record = CausalRecord(
            case.identifier,
            mechanism,
            case.outcome,
            produced,
            plan.model_version_identifier,
            supplied_intervention,
        )
        occurrences.append(
            TrialOccurrence(
                f"occurrence:{plan.identifier}:{case.identifier}",
                plan.identifier,
                prediction.identifier,
                case.identifier,
                produced,
                occurred_order_base + index,
                causal_record,
            )
        )
    return tuple(occurrences)


def assemble_history(
    predictions: tuple[Prediction, ...],
    occurrences: tuple[TrialOccurrence, ...],
    observations: tuple[Observation, ...],
) -> tuple[HistoricalTrial, ...]:
    return tuple(
        HistoricalTrial(
            f"history:{prediction.identifier}",
            prediction,
            occurrence,
            observation,
        )
        for prediction, occurrence, observation in zip(
            predictions,
            occurrences,
            observations,
            strict=True,
        )
    )
