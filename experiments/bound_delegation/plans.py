"""Immutable source plans."""

from __future__ import annotations

from .records import ActionKind, ActionSpec, Compartment, SourcePlan


def rebalance_plan(principal_identifier: str) -> SourcePlan:
    return SourcePlan(
        "plan:rebalance-north-center",
        principal_identifier,
        "rebalance resources",
        (
            ActionSpec(ActionKind.TRANSFER, Compartment.NORTH, Compartment.CENTER, 1),
            ActionSpec(ActionKind.TRANSFER, Compartment.NORTH, Compartment.CENTER, 1),
            ActionSpec(ActionKind.WRITE_OPERATION, Compartment.CENTER, None, 0),
        ),
    )


def pressure_plan(principal_identifier: str) -> SourcePlan:
    return SourcePlan(
        "plan:consume-shared-north",
        principal_identifier,
        "consume shared resource",
        (ActionSpec(ActionKind.CONSUME_SHARED, Compartment.NORTH, None, 2),),
    )
