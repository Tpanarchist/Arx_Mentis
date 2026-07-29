"""Exact named scenarios for scoped model adoption."""

from __future__ import annotations

from .activation import activate
from .adoption import adopt
from .assessment import assess_model
from .models import model_x, model_y
from .policies import act_on_case, derive_artifact
from .records import (
    ActionRecord,
    Activation,
    Adoption,
    ArtifactUnavailable,
    Assessment,
    DerivedPolicy,
    Outcome,
    RevocationPolicy,
    Scope,
    UseMode,
)
from .world import AMBER_CASES, CASES, VIOLET_CASES, evaluate_action


def standard_assessments() -> tuple[Assessment, Assessment]:
    return (
        assess_model(model_x(), CASES, confidence=70),
        assess_model(model_y(), CASES, confidence=55),
    )


def scoped_control_adoptions(
    *,
    revocation_policy: RevocationPolicy = RevocationPolicy.LIVE_LINKED,
) -> tuple[Adoption, Adoption]:
    return (
        adopt(
            "adoption:x:amber:control",
            model_x(),
            purpose="choose-required-action",
            use_mode=UseMode.CONTROL,
            scopes=frozenset({Scope.AMBER}),
            authority=5,
            revocation_policy=revocation_policy,
            provenance=("assessment:model-x",),
        ),
        adopt(
            "adoption:y:violet:control",
            model_y(),
            purpose="choose-required-action",
            use_mode=UseMode.CONTROL,
            scopes=frozenset({Scope.VIOLET}),
            authority=5,
            revocation_policy=revocation_policy,
            provenance=("assessment:model-y",),
        ),
    )


def activate_and_derive(
    adoption: Adoption,
    *,
    snapshot_duration: int | None = None,
) -> tuple[Activation, DerivedPolicy]:
    activation = activate(adoption, activated_order=30)
    assert isinstance(activation, Activation)
    policy = derive_artifact(
        activation,
        model_x() if adoption.model_identifier == "model-x" else model_y(),
        UseMode.CONTROL,
        derived_order=40,
        snapshot_duration=snapshot_duration,
    )
    assert isinstance(policy, DerivedPolicy)
    return activation, policy


def execute_scoped_composite() -> tuple[tuple[ActionRecord, ...], tuple[Outcome, ...]]:
    x_adoption, y_adoption = scoped_control_adoptions()
    _, x_policy = activate_and_derive(x_adoption)
    _, y_policy = activate_and_derive(y_adoption)
    records: list[ActionRecord] = []
    for index, case in enumerate((*AMBER_CASES, *VIOLET_CASES)):
        policy = x_policy if case.scope is Scope.AMBER else y_policy
        result = act_on_case(policy, case, produced_order=50 + index)
        if isinstance(result, ArtifactUnavailable):
            raise AssertionError(result.reason)
        records.append(result)
    actions = tuple(records)
    outcomes = tuple(
        evaluate_action(action, case, order=100 + index)
        for index, (action, case) in enumerate(zip(actions, CASES, strict=True))
    )
    return actions, outcomes
