"""Neutral vocabulary for a three-channel virtual-mediation mechanism.

This module deliberately contains no Arx Mentis foundation types. It models only
the proposed domain mechanics; correspondence is attempted later and elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Channel(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"


class Rotation(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2


@dataclass(frozen=True, slots=True)
class Stress:
    units: int


@dataclass(frozen=True, slots=True)
class Transfer:
    units: int


@dataclass(frozen=True, slots=True)
class Interaction:
    name: str
    source: str
    endpoint: str
    stress: Stress
    direct_transfer_prohibited: bool = True
    broken: bool = False


@dataclass(frozen=True, slots=True)
class Intervention:
    interaction: Interaction


@dataclass(frozen=True, slots=True)
class Mediator:
    channel: Channel
    directly_observed: bool


@dataclass(frozen=True, slots=True)
class Provenance:
    operation: str
    sources: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Trace:
    interaction_name: str
    mediator: Mediator
    transfer: Transfer
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class Signature:
    interaction_name: str
    channel: Channel
    marker: str


class ObservationKind(Enum):
    SIGNATURE = "signature"
    ENDPOINT = "endpoint"
    UNDECLARED = "undeclared"


@dataclass(frozen=True, slots=True)
class Observation:
    subject: str
    kind: ObservationKind
    signature: Signature | None = None


@dataclass(frozen=True, slots=True)
class Outcome:
    interaction_name: str
    endpoint: str
    transfer: Transfer
    reached: bool


class Permission(Enum):
    MEDIATE_TRANSFER = "mediate-transfer"


@dataclass(frozen=True, slots=True)
class Situation:
    permissions: frozenset[Permission]
    observations: frozenset[Observation] = frozenset()


@dataclass(frozen=True, slots=True)
class Denied:
    missing: Permission
    reason: str


@dataclass(frozen=True, slots=True)
class Breakdown:
    interaction: Interaction
    reason: str


@dataclass(frozen=True, slots=True)
class Criterion:
    name: str


@dataclass(frozen=True, slots=True)
class CriterionTruth:
    channel: Channel
    holds: bool


@dataclass(frozen=True, slots=True)
class Accepted:
    criterion: Criterion
    checked_channels: frozenset[Channel]
    reason: str


@dataclass(frozen=True, slots=True)
class Rejected:
    criterion: Criterion
    checked_channels: frozenset[Channel]
    reason: str
