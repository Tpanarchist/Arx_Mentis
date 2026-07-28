"""Neutral records for exact finite production, observation, and attribution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"


class StoppingKind(Enum):
    FIXED = "fixed"
    FAVORABLE_RUN = "favorable-run"


class ReportKind(Enum):
    ALL = "all"
    MATCH_TARGET = "match-target"


class MechanismKind(Enum):
    BASELINE = "baseline"
    INTERVENED = "intervened"
    CONTEXT_MIXTURE = "context-mixture"
    DIRECT_COMMAND = "direct-command"


@dataclass(frozen=True, slots=True)
class OutcomeSpace:
    outcomes: frozenset[Outcome]


@dataclass(frozen=True, slots=True)
class Weight:
    outcome: Outcome
    mass: int


@dataclass(frozen=True, slots=True)
class Kernel:
    identifier: str
    outcome_space: OutcomeSpace
    weights: tuple[Weight, ...]
    denominator: int


@dataclass(frozen=True, slots=True)
class InvalidWeights:
    identifier: str
    supplied: tuple[Weight, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class InvalidSeed:
    seed: int
    allowed: range
    reason: str


@dataclass(frozen=True, slots=True)
class ContextState:
    identifier: str
    kernel: Kernel
    visible_to_observer: bool


@dataclass(frozen=True, slots=True)
class Intervention:
    identifier: str
    target: Outcome | None
    delta: int
    priority: int
    context_identifier: str | None


@dataclass(frozen=True, slots=True)
class WeightChange:
    outcome: Outcome
    before: int
    after: int


@dataclass(frozen=True, slots=True)
class KernelTransformation:
    before: Kernel
    after: Kernel
    intervention: Intervention
    changes: tuple[WeightChange, ...]


@dataclass(frozen=True, slots=True)
class UnchangedKernel:
    kernel: Kernel
    intervention: Intervention
    reason: str


@dataclass(frozen=True, slots=True)
class InterventionConflict:
    kernel: Kernel
    priority: int
    intervention_identifiers: frozenset[str]
    reason: str


@dataclass(frozen=True, slots=True)
class ObservationWindow:
    start: int
    stop: int


@dataclass(frozen=True, slots=True)
class ReportPolicy:
    identifier: str
    kind: ReportKind
    target: Outcome | None


@dataclass(frozen=True, slots=True)
class StoppingRule:
    kind: StoppingKind
    favorable_run_length: int | None = None


@dataclass(frozen=True, slots=True)
class ComparisonRule:
    identifier: str
    expected_kernel: str


@dataclass(frozen=True, slots=True)
class TrialPlan:
    identifier: str
    recorded_order: int
    outcome_space: OutcomeSpace
    target: Outcome | None
    kernel_identifier: str
    intervention_identifiers: tuple[str, ...]
    trial_count: int
    seeds: tuple[int, ...]
    context_identifiers: tuple[str, ...]
    observation_window: ObservationWindow
    report_policy: ReportPolicy
    stopping_rule: StoppingRule
    comparison_rule: ComparisonRule


@dataclass(frozen=True, slots=True)
class Trial:
    order: int
    seed: int
    context_identifier: str
    outcome: Outcome


@dataclass(frozen=True, slots=True)
class CausalRecord:
    mechanism: MechanismKind
    kernel_identifiers: tuple[str, ...]
    intervention_identifiers: tuple[str, ...]
    context_identifiers: tuple[str, ...]
    seed_count: int


@dataclass(frozen=True, slots=True)
class EventStream:
    plan: TrialPlan
    trials: tuple[Trial, ...]
    causal_record: CausalRecord


@dataclass(frozen=True, slots=True)
class InvalidPlan:
    plan: TrialPlan
    reason: str


@dataclass(frozen=True, slots=True)
class ScheduledSeed:
    context_identifier: str
    seed: int


@dataclass(frozen=True, slots=True)
class ContextSchedule:
    entries: tuple[ScheduledSeed, ...]


@dataclass(frozen=True, slots=True)
class Sample:
    source_stream: EventStream
    window: ObservationWindow
    trials: tuple[Trial, ...]


@dataclass(frozen=True, slots=True)
class ObservedTrial:
    order: int
    outcome: Outcome
    context_available: bool


@dataclass(frozen=True, slots=True)
class ObservedSample:
    source_sample: Sample
    trials: tuple[ObservedTrial, ...]


@dataclass(frozen=True, slots=True)
class Report:
    source_stream: EventStream
    policy: ReportPolicy
    trials: tuple[Trial, ...]


@dataclass(frozen=True, slots=True)
class PostHocTarget:
    selected: Outcome
    selected_after_order: int
    precommitted: bool


@dataclass(frozen=True, slots=True)
class Frequency:
    outcome: Outcome
    count: int


@dataclass(frozen=True, slots=True)
class Distribution:
    frequencies: tuple[Frequency, ...]
    total: int


@dataclass(frozen=True, slots=True)
class KernelComparison:
    same_support: bool
    weight_changes: tuple[WeightChange, ...]


@dataclass(frozen=True, slots=True)
class DistributionComparison:
    same_public_distribution: bool
    left: Distribution
    right: Distribution


@dataclass(frozen=True, slots=True)
class Correspondence:
    trial: Trial
    target: Outcome
    matches: bool


@dataclass(frozen=True, slots=True)
class SampleCriterion:
    target: Outcome
    minimum_count: int


@dataclass(frozen=True, slots=True)
class SampleAcceptance:
    sample: Sample
    criterion: SampleCriterion
    accepted: bool


@dataclass(frozen=True, slots=True)
class ObserverAttribution:
    observed: ObservedSample
    candidate_mechanisms: frozenset[MechanismKind]
    selected: MechanismKind | None
    world_record_available: bool


@dataclass(frozen=True, slots=True)
class OptionBag:
    options: frozenset[Outcome]


@dataclass(frozen=True, slots=True)
class OptionBagLoss:
    baseline_bag: OptionBag
    biased_bag: OptionBag
    kernels_differ: bool
    behavior_lost: bool


@dataclass(frozen=True, slots=True)
class DirectCommand:
    target: Outcome
    installed_support: frozenset[Outcome]
    causal_record: CausalRecord


@dataclass(frozen=True, slots=True)
class ProbabilityBoundary:
    weighted: bool
    unequal_mass: bool
    transitive_frame_declared: bool
    settlement_operation_declared: bool
    conclusion: str


@dataclass(frozen=True, slots=True)
class CountermodelRejection:
    countermodel: str
    reason: str
