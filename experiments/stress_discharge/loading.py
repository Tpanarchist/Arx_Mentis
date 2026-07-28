"""Create immutable distributed fields through gradual or sudden loading."""

from __future__ import annotations

from .source_model import (
    LoadEvent,
    LoadHistory,
    LoadingMode,
    NetworkState,
    Site,
    SiteLoad,
    StressField,
)


def field_from(*, a: int = 0, b: int = 0, c: int = 0) -> StressField:
    if min(a, b, c) < 0:
        raise ValueError("site loads must be nonnegative")
    return StressField(
        (
            SiteLoad(Site.A, a),
            SiteLoad(Site.B, b),
            SiteLoad(Site.C, c),
        )
    )


def empty_state() -> NetworkState:
    return NetworkState(
        field_from(),
        delivered=0,
        dissipated=0,
        ruptured_links=frozenset(),
        history=LoadHistory(()),
    )


def load_at(field: StressField, site: Site) -> int:
    return next(item.amount for item in field.loads if item.site is site)


def total_stress(field: StressField) -> int:
    return sum(item.amount for item in field.loads)


def replace_load(field: StressField, site: Site, amount: int) -> StressField:
    values = {item.site: item.amount for item in field.loads}
    values[site] = amount
    return field_from(a=values[Site.A], b=values[Site.B], c=values[Site.C])


def add_load(
    state: NetworkState,
    site: Site,
    amount: int,
    mode: LoadingMode,
) -> NetworkState:
    if amount <= 0:
        raise ValueError("load increments must be positive")
    event = LoadEvent(len(state.history.events) + 1, site, amount, mode)
    field = replace_load(
        state.field,
        site,
        load_at(state.field, site) + amount,
    )
    return NetworkState(
        field,
        state.delivered,
        state.dissipated,
        state.ruptured_links,
        LoadHistory((*state.history.events, event)),
    )


def load_gradually(
    state: NetworkState,
    site: Site,
    *,
    increment: int,
    repetitions: int,
) -> NetworkState:
    result = state
    for _ in range(repetitions):
        result = add_load(result, site, increment, LoadingMode.GRADUAL)
    return result


def load_suddenly(state: NetworkState, site: Site, amount: int) -> NetworkState:
    return add_load(state, site, amount, LoadingMode.SUDDEN)
