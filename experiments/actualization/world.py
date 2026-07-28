"""A deterministic transition system independent of targets and controllers."""

from __future__ import annotations

from .source_model import Constraint, Position, Transition, WorldState

TRANSITIONS = (
    Transition("short-a-b", Position.A, Position.B, resource_gain=1, safe=True),
    Transition("unsafe-b-d", Position.B, Position.D, resource_gain=2, safe=False),
    Transition("safe-a-c", Position.A, Position.C, resource_gain=1, safe=True),
    Transition("safe-c-e", Position.C, Position.E, resource_gain=1, safe=True),
    Transition("safe-e-d", Position.E, Position.D, resource_gain=1, safe=True),
)


def initial_world() -> WorldState:
    return WorldState(Position.A, resources=2)


def available_transitions(
    state: WorldState,
    constraint: Constraint,
) -> tuple[Transition, ...]:
    return tuple(
        transition
        for transition in TRANSITIONS
        if transition.source is state.position
        and transition.identifier not in constraint.blocked_transitions
        and (constraint.unsafe_allowed or transition.safe)
    )


def apply_transition(state: WorldState, transition: Transition) -> WorldState:
    if transition.source is not state.position:
        raise ValueError("transition source does not match the supplied world")
    return WorldState(
        position=transition.destination,
        resources=state.resources + transition.resource_gain,
        gate_open=transition.destination is Position.D,
    )
