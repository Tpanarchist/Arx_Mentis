"""Counterfactual replay that never replaces historical predictions."""

from __future__ import annotations

from .models import predict
from .records import CaseInput, HistoricalTrial, ModelVersion, Replay, ReplayPrediction


def replay(
    identifier: str,
    version: ModelVersion,
    cases: tuple[CaseInput, ...],
    history: tuple[HistoricalTrial, ...],
    *,
    created_order: int = 600,
) -> Replay:
    return Replay(
        identifier,
        version,
        tuple(
            ReplayPrediction(
                case.identifier, version.identifier, predict(version.model, case)
            )
            for case in cases
        ),
        tuple(item.prediction.identifier for item in history),
        created_order,
    )
