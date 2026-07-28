"""Observation, correction, and observer-relative attribution."""

from __future__ import annotations

from .models import predict
from .records import (
    CaseInput,
    Correction,
    ModelVersion,
    Observation,
    ObserverAttribution,
    Outcome,
    TrialOccurrence,
)


def observe(
    occurrences: tuple[TrialOccurrence, ...],
    *,
    available_order_base: int = 200,
) -> tuple[Observation, ...]:
    return tuple(
        Observation(
            f"observation:{occurrence.identifier}",
            occurrence.identifier,
            occurrence.prediction_identifier,
            occurrence.case_identifier,
            occurrence.outcome,
            available_order_base + index,
        )
        for index, occurrence in enumerate(occurrences)
    )


def record_erroneous_observation(
    occurrence: TrialOccurrence,
    recorded_outcome: Outcome,
    *,
    available_order: int,
) -> Observation:
    return Observation(
        f"observation:error:{occurrence.identifier}",
        occurrence.identifier,
        occurrence.prediction_identifier,
        occurrence.case_identifier,
        recorded_outcome,
        available_order,
    )


def correct_observation(
    observation: Observation,
    corrected_outcome: Outcome,
    *,
    reason: str,
    recorded_order: int,
) -> Correction:
    return Correction(
        f"correction:{observation.identifier}",
        observation.identifier,
        observation.case_identifier,
        corrected_outcome,
        reason,
        recorded_order,
    )


def attribute_observation(
    observation: Observation,
    case: CaseInput,
    versions: tuple[ModelVersion, ...],
    *,
    confidence: tuple[tuple[str, int], ...] = (),
) -> ObserverAttribution:
    candidates = frozenset(
        version.identifier
        for version in versions
        if predict(version.model, case) is observation.outcome
    )
    return ObserverAttribution(
        observation.identifier,
        candidates,
        confidence,
        selected_model_version_identifier=None,
        world_cause_available=False,
    )
