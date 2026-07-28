"""Neutral prediction models that cannot access case outcomes."""

from __future__ import annotations

from .records import CaseInput, Model, ModelKind, ModelVersion, Outcome


def initial_model_a() -> Model:
    return Model("model-a-feature-x", ModelKind.FEATURE_X, (), complexity=1)


def initial_model_b() -> Model:
    return Model("model-b-feature-y", ModelKind.FEATURE_Y, (), complexity=1)


def constant_negative_model() -> Model:
    return Model(
        "constant-negative",
        ModelKind.CONSTANT,
        (("constant", Outcome.NEGATIVE),),
        complexity=1,
    )


def initial_version(model: Model, identifier: str) -> ModelVersion:
    return ModelVersion(identifier, model, ordinal=0, lineage=None)


def predict(model: Model, case: CaseInput) -> Outcome:
    if model.kind is ModelKind.FEATURE_X:
        return Outcome.POSITIVE if case.feature_x else Outcome.NEGATIVE
    if model.kind is ModelKind.FEATURE_Y:
        return Outcome.POSITIVE if case.feature_y else Outcome.NEGATIVE
    if model.kind is ModelKind.XOR:
        return (
            Outcome.POSITIVE if case.feature_x != case.feature_y else Outcome.NEGATIVE
        )
    if model.kind is ModelKind.FEATURE_LOOKUP:
        key = f"{int(case.feature_x)}{int(case.feature_y)}"
        return dict(model.parameters)[key]
    if model.kind is ModelKind.MEMORIZE:
        memorized = dict(model.parameters)
        if case.identifier in memorized:
            return memorized[case.identifier]
        return Outcome.NEGATIVE if case.feature_x else Outcome.POSITIVE
    if model.kind is ModelKind.CONSTANT:
        return dict(model.parameters)["constant"]
    raise AssertionError(f"unhandled model kind: {model.kind}")
