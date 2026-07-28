"""Mechanistic discharge selected from field, topology, and constraints."""

from __future__ import annotations

from .loading import load_at, replace_load
from .source_model import (
    AmbiguousDischarge,
    CausalTrace,
    ConstrainedNetwork,
    ConstraintSet,
    Discharge,
    DischargeStep,
    DormantTrigger,
    HistoricalResidue,
    Link,
    LinkKind,
    NetworkState,
    NoDischargePath,
    OscillationLaw,
    StressField,
    TransferKind,
    Trigger,
)


def _open_links(
    state: NetworkState,
    network: ConstrainedNetwork,
    constraints: ConstraintSet,
) -> tuple[Link, ...]:
    return tuple(
        link
        for link in network.links
        if link.identifier not in constraints.blocked_links
        and link.identifier not in state.ruptured_links
    )


def _force(field: StressField, link: Link) -> int:
    source = load_at(field, link.source)
    if link.target is None:
        return source
    return source - load_at(field, link.target)


def _choose(
    field: StressField,
    links: tuple[Link, ...],
) -> tuple[Link | None, bool, tuple[str, ...]]:
    ruptures = tuple(
        link
        for link in links
        if link.kind is LinkKind.TRANSFER
        and load_at(field, link.source) > link.rupture_threshold
    )
    candidates = ruptures or tuple(link for link in links if _force(field, link) > 0)
    if not candidates:
        return None, False, ()

    def score(link: Link) -> tuple[int, int]:
        if ruptures:
            return (
                (load_at(field, link.source) - link.rupture_threshold)
                * link.conductance,
                link.capacity,
            )
        return (_force(field, link) * link.conductance, link.capacity)

    scored = tuple((score(link), link) for link in candidates)
    maximum = max(item[0] for item in scored)
    leaders = tuple(link for value, link in scored if value == maximum)
    if len(leaders) != 1:
        return None, bool(ruptures), tuple(sorted(link.identifier for link in leaders))
    return leaders[0], bool(ruptures), ()


def _transfer(
    state: NetworkState,
    link: Link,
    *,
    rupture: bool,
) -> tuple[NetworkState, int, TransferKind]:
    source_amount = load_at(state.field, link.source)
    force = _force(state.field, link)
    if rupture:
        amount = min(source_amount, link.capacity * 2)
        kind = TransferKind.RUPTURE
    elif link.kind is LinkKind.TRANSFER:
        amount = min(link.capacity, max(1, (force + 1) // 2))
        kind = TransferKind.DISPLACEMENT
    elif link.kind is LinkKind.RELEASE:
        amount = min(link.capacity, source_amount)
        kind = TransferKind.RELEASE
    else:
        amount = min(link.capacity, source_amount)
        kind = TransferKind.DISSIPATION

    field = replace_load(state.field, link.source, source_amount - amount)
    delivered = state.delivered
    dissipated = state.dissipated
    ruptured = state.ruptured_links
    if link.target is not None:
        field = replace_load(
            field,
            link.target,
            load_at(field, link.target) + amount,
        )
    elif link.kind is LinkKind.RELEASE:
        delivered += amount
    else:
        dissipated += amount
    if rupture:
        ruptured = frozenset({*ruptured, link.identifier})
    return (
        NetworkState(field, delivered, dissipated, ruptured, state.history),
        amount,
        kind,
    )


def _residue(
    after: NetworkState,
    steps: tuple[DischargeStep, ...],
    *,
    oscillation_reversals: int = 0,
) -> HistoricalResidue:
    return HistoricalResidue(
        after.history.events,
        after.ruptured_links,
        sum(
            step.amount
            for step in steps
            if step.kind in {TransferKind.DISPLACEMENT, TransferKind.RUPTURE}
        ),
        sum(step.amount for step in steps if step.kind is TransferKind.RELEASE),
        sum(step.amount for step in steps if step.kind is TransferKind.DISSIPATION),
        oscillation_reversals,
    )


def discharge(
    state: NetworkState,
    network: ConstrainedNetwork,
    constraints: ConstraintSet,
    trigger: Trigger,
    *,
    maximum_steps: int = 8,
) -> Discharge | DormantTrigger | NoDischargePath | AmbiguousDischarge:
    observed = load_at(state.field, trigger.site)
    if observed < trigger.threshold:
        return DormantTrigger(trigger, observed, trigger.threshold)

    current = state
    steps: list[DischargeStep] = []
    for index in range(maximum_steps):
        link, rupture, ambiguous = _choose(
            current.field,
            _open_links(current, network, constraints),
        )
        if ambiguous:
            trace = CausalTrace(
                network.identifier,
                constraints.identifier,
                trigger,
                state.field,
                state.history,
                tuple(steps),
            )
            return AmbiguousDischarge(
                current,
                ambiguous,
                trace,
                "the declared mechanics do not distinguish a discharge path",
            )
        if link is None:
            break
        next_state, amount, kind = _transfer(current, link, rupture=rupture)
        steps.append(
            DischargeStep(
                index + 1,
                link,
                kind,
                amount,
                current.field,
                next_state.field,
            )
        )
        current = next_state

    if not steps:
        return NoDischargePath(
            state,
            trigger,
            constraints,
            "trigger fired but every mechanically available path is blocked",
        )
    trace = CausalTrace(
        network.identifier,
        constraints.identifier,
        trigger,
        state.field,
        state.history,
        tuple(steps),
    )
    step_tuple = tuple(steps)
    return Discharge(state, current, trace, _residue(current, step_tuple))


def oscillate(
    state: NetworkState,
    network: ConstrainedNetwork,
    constraints: ConstraintSet,
    trigger: Trigger,
    law: OscillationLaw,
) -> Discharge | DormantTrigger | NoDischargePath:
    observed = load_at(state.field, trigger.site)
    if observed < trigger.threshold:
        return DormantTrigger(trigger, observed, trigger.threshold)
    pair = tuple(
        link
        for link in _open_links(state, network, constraints)
        if link.identifier in {law.forward_link, law.reverse_link}
    )
    if len(pair) != 2:
        return NoDischargePath(
            state,
            trigger,
            constraints,
            "oscillation requires both declared reciprocal paths",
        )

    current = state
    steps: list[DischargeStep] = []
    amplitude: int | None = None
    previous_link: str | None = None
    reversals = 0
    for index in range(law.maximum_pulses):
        pressured = tuple(link for link in pair if _force(current.field, link) > 0)
        if len(pressured) != 1:
            break
        link = pressured[0]
        difference = _force(current.field, link)
        if amplitude is None:
            amount = min(link.capacity, difference)
        else:
            amount = min(link.capacity, difference, amplitude - law.damping)
        if amount <= 0:
            break
        before = current.field
        source_amount = load_at(before, link.source)
        after_field = replace_load(before, link.source, source_amount - amount)
        assert link.target is not None
        after_field = replace_load(
            after_field,
            link.target,
            load_at(after_field, link.target) + amount,
        )
        current = NetworkState(
            after_field,
            current.delivered,
            current.dissipated,
            current.ruptured_links,
            current.history,
        )
        steps.append(
            DischargeStep(
                index + 1,
                link,
                TransferKind.OSCILLATION,
                amount,
                before,
                after_field,
            )
        )
        if previous_link is not None and previous_link != link.identifier:
            reversals += 1
        previous_link = link.identifier
        amplitude = amount

    if not steps:
        return NoDischargePath(
            state,
            trigger,
            constraints,
            "no pressure difference initiates the declared oscillation",
        )
    trace = CausalTrace(
        network.identifier,
        constraints.identifier,
        trigger,
        state.field,
        state.history,
        tuple(steps),
    )
    step_tuple = tuple(steps)
    return Discharge(
        state,
        current,
        trace,
        _residue(current, step_tuple, oscillation_reversals=reversals),
    )
