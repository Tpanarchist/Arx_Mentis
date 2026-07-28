"""Hostile reductions that erase causal or distributed structure."""

from __future__ import annotations

from .loading import total_stress
from .source_model import (
    BlockedPathReport,
    CapacityBoundary,
    CapacityProfile,
    CountermodelRejection,
    Discharge,
    IncompleteCausalAccount,
    ScalarLossReport,
    ScalarStress,
    StressField,
    Trigger,
)


def collapse_to_scalar(field: StressField) -> ScalarStress:
    return ScalarStress(total_stress(field))


def report_scalar_loss(
    left_field: StressField,
    right_field: StressField,
    left_path: str,
    right_path: str,
) -> ScalarLossReport:
    left = collapse_to_scalar(left_field)
    right = collapse_to_scalar(right_field)
    if left != right:
        raise ValueError("countermodel requires equal scalar totals")
    return ScalarLossReport(
        left,
        fields_differ=left_field != right_field,
        paths_differ=left_path != right_path,
        conclusion=(
            "one scalar preserves neither load distribution nor discharge path"
        ),
    )


def reject_target_coded_discharge(preferred_path: str) -> CountermodelRejection:
    return CountermodelRejection(
        "target-coded-discharge",
        f"preferred path {preferred_path!r} is an outcome smuggled into the cause",
    )


def reject_trigger_only_causation(trigger: Trigger) -> IncompleteCausalAccount:
    return IncompleteCausalAccount(
        trigger,
        ("distributed field", "network topology", "constraints", "transfer law"),
        "a threshold event initiates but does not determine discharge",
    )


def reject_stress_as_progress() -> CountermodelRejection:
    return CountermodelRejection(
        "stress-equals-progress",
        "stress reduction may be dissipation or displacement without desired delivery",
    )


def reject_history_erasure(discharge: Discharge) -> CountermodelRejection:
    events = len(discharge.residue.loading_events)
    return CountermodelRejection(
        "release-erases-history",
        f"discharge retains {events} loading events and its irreversible residue",
    )


def report_blocked_alternative(
    blocked_link: str,
    alternative_used: str | None,
) -> BlockedPathReport:
    return BlockedPathReport(
        blocked_link,
        alternative_used,
        no_path=alternative_used is None,
    )


def reject_capacity_as_symmetric_potential(
    profile: CapacityProfile,
) -> CapacityBoundary:
    capacities = {entry.capacity for entry in profile.entries}
    kinds = {entry.kind for entry in profile.entries}
    return CapacityBoundary(
        profile,
        path_encoded=False,
        transitive_alternatives=len(capacities) == 1 and len(kinds) == 1,
        reason=(
            "capacity constrains transfer but is neither a candidate outcome nor a "
            "transitive family of interchangeable alternatives"
        ),
    )
