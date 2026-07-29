"""Available models with no intrinsic adoption or use role."""

from __future__ import annotations

from .records import Action, Model, ModelKind, WorldCase


def model_x() -> Model:
    return Model("model-x", ModelKind.SIGNAL_X, measured_cost=2)


def model_y() -> Model:
    return Model("model-y", ModelKind.SIGNAL_Y, measured_cost=3)


def cooperation_model() -> Model:
    return Model("cooperation-model", ModelKind.COOPERATION, measured_cost=1)


def model_action(model: Model, case: WorldCase | None = None) -> Action:
    if model.kind is ModelKind.SIGNAL_X:
        if case is None:
            raise ValueError("signal model requires a world case")
        return case.signal_x
    if model.kind is ModelKind.SIGNAL_Y:
        if case is None:
            raise ValueError("signal model requires a world case")
        return case.signal_y
    if model.kind is ModelKind.COOPERATION:
        return Action.COOPERATE
    raise AssertionError(f"unhandled model kind: {model.kind}")
