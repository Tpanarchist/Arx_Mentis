"""Named loading, constraint, and assessment scenarios."""

from __future__ import annotations

from .loading import add_load, empty_state, field_from, load_gradually, load_suddenly
from .source_model import (
    AcceptanceCriterion,
    ConstraintSet,
    LoadHistory,
    LoadingMode,
    NetworkState,
    OscillationLaw,
    ProgressCriterion,
    ResolutionRule,
    Site,
    Trigger,
)

OPEN = ConstraintSet("open")
BLOCK_NORTH = ConstraintSet("block-north", frozenset({"a-b"}))
BLOCK_BOTH = ConstraintSet("block-both", frozenset({"a-b", "a-c"}))
SOURCE_ONLY = ConstraintSet(
    "source-only",
    frozenset({"b-out", "c-out", "b-c", "c-b", "c-void"}),
)
C_RELEASE_ONLY = ConstraintSet(
    "c-release-only",
    frozenset({"a-b", "a-c", "b-out", "b-c", "c-b", "c-void"}),
)
FORCE_DISSIPATION = ConstraintSet(
    "force-dissipation",
    frozenset({"c-out", "c-b"}),
)

SOURCE_TRIGGER = Trigger("source-threshold", Site.A, 5)
C_TRIGGER = Trigger("c-threshold", Site.C, 3)
B_TRIGGER = Trigger("b-threshold", Site.B, 3)

SAFE_RESOLUTION = ResolutionRule(maximum_site_load=1, rupture_allowed=False)
DELIVERY_ACCEPTANCE = AcceptanceCriterion(
    minimum_delivered=5,
    maximum_dissipated=0,
    rupture_allowed=False,
)
DELIVERY_PROGRESS = ProgressCriterion(minimum_delivered=1)


def gradual_source_load() -> NetworkState:
    return load_gradually(
        empty_state(),
        Site.A,
        increment=2,
        repetitions=3,
    )


def sudden_source_load(amount: int = 6) -> NetworkState:
    return load_suddenly(empty_state(), Site.A, amount)


def north_obstructed_distribution() -> NetworkState:
    state = load_suddenly(empty_state(), Site.A, 6)
    return add_load(state, Site.B, 4, LoadingMode.SUDDEN)


def south_obstructed_distribution() -> NetworkState:
    state = load_suddenly(empty_state(), Site.A, 6)
    return add_load(state, Site.C, 4, LoadingMode.SUDDEN)


def dissipation_load() -> NetworkState:
    return NetworkState(
        field_from(c=4),
        delivered=0,
        dissipated=0,
        ruptured_links=frozenset(),
        history=LoadHistory(()),
    )


def oscillation_load() -> NetworkState:
    return NetworkState(
        field_from(b=5),
        delivered=0,
        dissipated=0,
        ruptured_links=frozenset(),
        history=LoadHistory(()),
    )


def oscillation_law() -> OscillationLaw:
    return OscillationLaw("b-c", "c-b", damping=1, maximum_pulses=4)
