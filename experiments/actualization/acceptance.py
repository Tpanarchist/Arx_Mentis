"""Derive and evaluate acceptance independently of production mechanics."""

from __future__ import annotations

from .source_model import AcceptanceResult, AcceptanceRule, TargetForm, WorldState


def derive_acceptance(target: TargetForm) -> AcceptanceRule:
    return AcceptanceRule(target.desired_position, target.minimum_resources)


def evaluate(rule: AcceptanceRule, state: WorldState) -> AcceptanceResult:
    return AcceptanceResult(
        rule,
        state,
        state.position is rule.desired_position
        and state.resources >= rule.minimum_resources,
    )
