"""Neutral records for events, correspondences, causes, and explanations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class RecordedAim:
    identifier: str
    recorded_order: int
    desired_feature: str


@dataclass(frozen=True, slots=True)
class Event:
    identifier: str
    occurred_order: int
    features: frozenset[str]
    description: str


class CauseChannel(Enum):
    ORDINARY_CHANCE = "ordinary-chance"
    SELECTIVE_REPORTING = "selective-reporting"
    OPERATOR_BEHAVIOR = "operator-behavior"
    SOCIAL_RESPONSE = "social-response"
    SELF_ORGANIZATION = "self-organization"
    ANOMALOUS_MEDIATION = "anomalous-mediation"


@dataclass(frozen=True, slots=True)
class WorldEvent:
    event: Event
    definite_cause: CauseChannel


@dataclass(frozen=True, slots=True)
class ObservedEvent:
    event: Event
    cause_available: bool = False


@dataclass(frozen=True, slots=True)
class MatchRule:
    name: str
    required_feature: str


@dataclass(frozen=True, slots=True)
class Correspondence:
    aim: RecordedAim
    event: Event
    rule: MatchRule
    matches: bool


@dataclass(frozen=True, slots=True)
class Rate:
    matches: int
    trials: int


@dataclass(frozen=True, slots=True)
class Baseline:
    name: str
    expected_rate: Rate


@dataclass(frozen=True, slots=True)
class EventStream:
    baseline: Baseline
    events: tuple[WorldEvent, ...]


@dataclass(frozen=True, slots=True)
class Observation:
    observer: str
    event: Event
    reported_order: int


class CausalVariable(Enum):
    BASELINE_PROCESS = "baseline-process"
    REPORTING_FILTER = "reporting-filter"
    OPERATOR_ATTENTION = "operator-attention"
    OPERATOR_BEHAVIOR = "operator-behavior"
    OPERATOR_SIGNAL = "operator-signal"
    OTHER_PERSON_RESPONSE = "other-person-response"
    ENVIRONMENTAL_DYNAMICS = "environmental-dynamics"
    UNKNOWN_MEDIATOR = "unknown-mediator"


class HypothesisKind(Enum):
    CHANCE = "chance"
    SELECTION = "selection"
    BEHAVIOR = "behavior"
    SOCIAL_RESPONSE = "social-response"
    SELF_ORGANIZATION = "self-organization"
    ANOMALOUS = "anomalous"


@dataclass(frozen=True, slots=True)
class Hypothesis:
    kind: HypothesisKind
    claim: str
    variables: frozenset[CausalVariable]
    required_evidence: frozenset[str]
    prior_support: int


class EvidenceKind(Enum):
    COMPLETE_STREAM = "complete-stream"
    ACTION_LOG = "action-log"
    RESPONSE_LOG = "response-log"
    INTERVENTION = "intervention"
    ENVIRONMENTAL_RECORD = "environmental-record"
    ELIMINATION_RECORD = "elimination-record"


@dataclass(frozen=True, slots=True)
class Evidence:
    identifier: str
    subject: str
    kind: EvidenceKind
    supports: frozenset[HypothesisKind]
    weakens: frozenset[HypothesisKind]
    strength: int
    note: str


@dataclass(frozen=True, slots=True)
class CausalLink:
    source: str
    relation: str
    target: str


@dataclass(frozen=True, slots=True)
class CausalAccount:
    hypothesis: HypothesisKind
    links: tuple[CausalLink, ...]
    result: WorldEvent


@dataclass(frozen=True, slots=True)
class Intervention:
    name: str
    blocked: frozenset[CausalVariable]
    preserved_aim: RecordedAim


@dataclass(frozen=True, slots=True)
class TrialSummary:
    label: str
    matches: int
    trials: int
