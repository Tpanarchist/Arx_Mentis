"""Outcome observation, post-hoc scope, and separate truth assertion."""

from __future__ import annotations

from .records import (
    Model,
    Outcome,
    OutcomeObservation,
    PostHocScope,
    Scope,
    TruthAssertion,
)


def observe_outcome(outcome: Outcome, *, available_order: int) -> OutcomeObservation:
    return OutcomeObservation(
        f"observation:{outcome.identifier}",
        outcome.identifier,
        outcome.successful,
        outcome.observed_result,
        available_order,
    )


def assert_truth(
    model: Model,
    claim: str,
    *,
    asserted_order: int,
) -> TruthAssertion:
    return TruthAssertion(
        f"truth-assertion:{model.identifier}:{asserted_order}",
        model.identifier,
        claim,
        asserted_order,
    )


def select_scope_post_hoc(
    model: Model,
    scope: Scope,
    outcomes: tuple[Outcome, ...],
) -> PostHocScope:
    return PostHocScope(
        model.identifier,
        scope,
        tuple(item.identifier for item in outcomes),
        precommitted=False,
    )
