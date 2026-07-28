"""Neutral records for distributed load and constrained discharge."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Site(Enum):
    A = "a"
    B = "b"
    C = "c"


class LoadingMode(Enum):
    GRADUAL = "gradual"
    SUDDEN = "sudden"


class LinkKind(Enum):
    TRANSFER = "transfer"
    RELEASE = "release"
    DISSIPATE = "dissipate"


class TransferKind(Enum):
    DISPLACEMENT = "displacement"
    RELEASE = "release"
    DISSIPATION = "dissipation"
    RUPTURE = "rupture"
    OSCILLATION = "oscillation"


@dataclass(frozen=True, slots=True)
class SiteLoad:
    site: Site
    amount: int


@dataclass(frozen=True, slots=True)
class StressField:
    loads: tuple[SiteLoad, ...]


@dataclass(frozen=True, slots=True)
class LoadEvent:
    order: int
    site: Site
    amount: int
    mode: LoadingMode


@dataclass(frozen=True, slots=True)
class LoadHistory:
    events: tuple[LoadEvent, ...]


@dataclass(frozen=True, slots=True)
class NetworkState:
    field: StressField
    delivered: int
    dissipated: int
    ruptured_links: frozenset[str]
    history: LoadHistory


@dataclass(frozen=True, slots=True)
class Link:
    identifier: str
    source: Site
    target: Site | None
    capacity: int
    conductance: int
    rupture_threshold: int
    kind: LinkKind


@dataclass(frozen=True, slots=True)
class ConstrainedNetwork:
    identifier: str
    links: tuple[Link, ...]


@dataclass(frozen=True, slots=True)
class ConstraintSet:
    identifier: str
    blocked_links: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class Trigger:
    identifier: str
    site: Site
    threshold: int


@dataclass(frozen=True, slots=True)
class DischargeStep:
    index: int
    link: Link
    kind: TransferKind
    amount: int
    before: StressField
    after: StressField


@dataclass(frozen=True, slots=True)
class CausalTrace:
    network_identifier: str
    constraint_identifier: str
    trigger: Trigger
    initial_field: StressField
    loading_history: LoadHistory
    steps: tuple[DischargeStep, ...]


@dataclass(frozen=True, slots=True)
class HistoricalResidue:
    loading_events: tuple[LoadEvent, ...]
    ruptured_links: frozenset[str]
    displaced_load: int
    released_load: int
    dissipated_load: int
    oscillation_reversals: int


@dataclass(frozen=True, slots=True)
class Discharge:
    before: NetworkState
    after: NetworkState
    trace: CausalTrace
    residue: HistoricalResidue


@dataclass(frozen=True, slots=True)
class DormantTrigger:
    trigger: Trigger
    observed_load: int
    required_load: int


@dataclass(frozen=True, slots=True)
class NoDischargePath:
    state: NetworkState
    trigger: Trigger
    constraints: ConstraintSet
    reason: str


@dataclass(frozen=True, slots=True)
class AmbiguousDischarge:
    state: NetworkState
    candidates: tuple[str, ...]
    trace: CausalTrace
    reason: str


@dataclass(frozen=True, slots=True)
class OscillationLaw:
    forward_link: str
    reverse_link: str
    damping: int
    maximum_pulses: int


@dataclass(frozen=True, slots=True)
class ResolutionRule:
    maximum_site_load: int
    rupture_allowed: bool


@dataclass(frozen=True, slots=True)
class ResolutionAssessment:
    state: NetworkState
    rule: ResolutionRule
    resolved: bool


@dataclass(frozen=True, slots=True)
class AcceptanceCriterion:
    minimum_delivered: int
    maximum_dissipated: int
    rupture_allowed: bool


@dataclass(frozen=True, slots=True)
class AcceptanceAssessment:
    state: NetworkState
    criterion: AcceptanceCriterion
    accepted: bool


@dataclass(frozen=True, slots=True)
class ProgressCriterion:
    minimum_delivered: int


@dataclass(frozen=True, slots=True)
class ProgressAssessment:
    state: NetworkState
    criterion: ProgressCriterion
    progressed: bool


@dataclass(frozen=True, slots=True)
class ScalarStress:
    total: int


@dataclass(frozen=True, slots=True)
class CapacityEntry:
    link_identifier: str
    capacity: int
    kind: LinkKind


@dataclass(frozen=True, slots=True)
class CapacityProfile:
    network_identifier: str
    entries: tuple[CapacityEntry, ...]
    total_capacity: int


@dataclass(frozen=True, slots=True)
class CountermodelRejection:
    countermodel: str
    reason: str


@dataclass(frozen=True, slots=True)
class IncompleteCausalAccount:
    trigger: Trigger
    missing_antecedents: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class ScalarLossReport:
    scalar: ScalarStress
    fields_differ: bool
    paths_differ: bool
    conclusion: str


@dataclass(frozen=True, slots=True)
class BlockedPathReport:
    blocked_link: str
    alternative_used: str | None
    no_path: bool


@dataclass(frozen=True, slots=True)
class CapacityBoundary:
    profile: CapacityProfile
    path_encoded: bool
    transitive_alternatives: bool
    reason: str
