"""Neutral records for targets, control, transitions, and causal histories."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Position(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"


class Preference(Enum):
    SHORTEST = "shortest"
    SAFE = "safe"


class Mechanism(Enum):
    CRITERION_ONLY = "criterion-only"
    POLICY_GUIDANCE = "policy-guidance"
    HIDDEN_BIAS = "hidden-bias"
    DIRECT_ASSIGNMENT = "direct-assignment"


@dataclass(frozen=True, slots=True)
class WorldState:
    position: Position
    resources: int
    gate_open: bool = False


@dataclass(frozen=True, slots=True)
class TargetForm:
    identifier: str
    recorded_order: int
    desired_position: Position
    minimum_resources: int
    preference: Preference


@dataclass(frozen=True, slots=True)
class AcceptanceRule:
    desired_position: Position
    minimum_resources: int


@dataclass(frozen=True, slots=True)
class ActionPolicy:
    identifier: str
    derived_from: str
    transition_order: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Transition:
    identifier: str
    source: Position
    destination: Position
    resource_gain: int
    safe: bool


@dataclass(frozen=True, slots=True)
class Constraint:
    blocked_transitions: frozenset[str] = frozenset()
    unsafe_allowed: bool = True
    maximum_steps: int = 6


@dataclass(frozen=True, slots=True)
class Feedback:
    observed_state: WorldState
    accepted: bool
    target_consulted: bool


@dataclass(frozen=True, slots=True)
class Controller:
    policy: ActionPolicy
    live_target: TargetForm | None
    sustained_feedback: bool


@dataclass(frozen=True, slots=True)
class TransitionWeight:
    transition: str
    weight: int


@dataclass(frozen=True, slots=True)
class HiddenWeighting:
    identifier: str
    derived_from: str
    weights: tuple[TransitionWeight, ...]


@dataclass(frozen=True, slots=True)
class CausalStep:
    index: int
    before: WorldState
    transition: Transition
    after: WorldState
    target_consulted: bool


@dataclass(frozen=True, slots=True)
class CausalTrace:
    mechanism: Mechanism
    target_identifier: str | None
    policy_identifier: str | None
    weighting_identifier: str | None
    target_available_during_run: bool
    steps: tuple[CausalStep, ...]
    feedback: tuple[Feedback, ...]


@dataclass(frozen=True, slots=True)
class Outcome:
    state: WorldState
    trace: CausalTrace


@dataclass(frozen=True, slots=True)
class AcceptanceResult:
    rule: AcceptanceRule
    state: WorldState
    conforms: bool


@dataclass(frozen=True, slots=True)
class Unreachable:
    state: WorldState
    trace: CausalTrace
    reason: str


@dataclass(frozen=True, slots=True)
class RejectedMechanism:
    mechanism: Mechanism
    source: WorldState
    proposed_state: WorldState
    reason: str


@dataclass(frozen=True, slots=True)
class ObserverAttribution:
    observed_state: WorldState
    candidates: frozenset[Mechanism]
    selected: Mechanism | None
