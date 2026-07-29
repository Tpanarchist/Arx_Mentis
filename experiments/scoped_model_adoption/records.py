"""Immutable neutral records for scoped model adoption."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Scope(Enum):
    AMBER = "amber"
    VIOLET = "violet"


class Action(Enum):
    LEFT = "left"
    RIGHT = "right"
    COOPERATE = "cooperate"
    WITHHOLD = "withhold"


class ModelKind(Enum):
    SIGNAL_X = "signal-x"
    SIGNAL_Y = "signal-y"
    COOPERATION = "cooperation"


class UseMode(Enum):
    PREDICTIVE = "predictive"
    CONTROL = "control"
    AUDIT = "audit"


class ActivationState(Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"


class RevocationPolicy(Enum):
    LIVE_LINKED = "live-linked"
    SNAPSHOT = "snapshot"
    UNSPECIFIED = "unspecified"


class ResolutionKind(Enum):
    HIGHER_AUTHORITY = "higher-authority"
    PREFERRED_MODEL = "preferred-model"


@dataclass(frozen=True, slots=True)
class WorldCase:
    identifier: str
    scope: Scope
    signal_x: Action
    signal_y: Action
    required_action: Action


@dataclass(frozen=True, slots=True)
class Model:
    identifier: str
    kind: ModelKind
    measured_cost: int


@dataclass(frozen=True, slots=True)
class ScopeScore:
    scope: Scope
    accepted_count: int
    total_count: int


@dataclass(frozen=True, slots=True)
class Assessment:
    identifier: str
    model_identifier: str
    scores: tuple[ScopeScore, ...]
    global_accepted_count: int
    global_total_count: int
    confidence: int
    rule_identifier: str
    created_order: int


@dataclass(frozen=True, slots=True)
class Adoption:
    identifier: str
    model_identifier: str
    purpose: str
    use_mode: UseMode
    scopes: frozenset[Scope]
    authority: int
    start_condition: str
    end_condition: str
    activation_state: ActivationState
    revocation_policy: RevocationPolicy
    provenance: tuple[str, ...]
    adopted_order: int


@dataclass(frozen=True, slots=True)
class Activation:
    identifier: str
    adoption: Adoption
    state: ActivationState
    activated_order: int


@dataclass(frozen=True, slots=True)
class Lineage:
    model_identifier: str
    adoption_identifier: str
    activation_identifier: str
    derived_order: int


@dataclass(frozen=True, slots=True)
class PredictionRule:
    identifier: str
    model: Model
    scopes: frozenset[Scope]
    lineage: Lineage
    revocation_policy: RevocationPolicy
    expires_order: int | None


@dataclass(frozen=True, slots=True)
class DerivedPolicy:
    identifier: str
    model: Model
    scopes: frozenset[Scope]
    lineage: Lineage
    revocation_policy: RevocationPolicy
    expires_order: int | None


@dataclass(frozen=True, slots=True)
class Prediction:
    identifier: str
    rule_identifier: str
    case_identifier: str
    predicted_action: Action
    recorded_order: int


@dataclass(frozen=True, slots=True)
class ActionRecord:
    identifier: str
    policy_identifier: str
    case_identifier: str
    action: Action
    lineage: Lineage
    produced_order: int


@dataclass(frozen=True, slots=True)
class CausalRecord:
    model_identifier: str
    adoption_identifier: str
    policy_identifier: str
    action_identifier: str
    action_participated: bool


@dataclass(frozen=True, slots=True)
class Outcome:
    identifier: str
    case_identifier: str
    successful: bool
    observed_result: str
    causal_record: CausalRecord
    occurred_order: int


@dataclass(frozen=True, slots=True)
class OutcomeObservation:
    identifier: str
    outcome_identifier: str
    successful: bool
    observed_result: str
    available_order: int


@dataclass(frozen=True, slots=True)
class TruthAssertion:
    identifier: str
    model_identifier: str
    claim: str
    asserted_order: int


@dataclass(frozen=True, slots=True)
class Revocation:
    identifier: str
    adoption_identifier: str
    policy: RevocationPolicy
    reason: str
    revoked_order: int


@dataclass(frozen=True, slots=True)
class ArtifactUnavailable:
    artifact_identifier: str
    reason: str


@dataclass(frozen=True, slots=True)
class UnspecifiedRevocationPolicy:
    adoption_identifier: str
    reason: str


@dataclass(frozen=True, slots=True)
class UnsupportedUse:
    adoption_identifier: str
    requested_use: UseMode
    reason: str


@dataclass(frozen=True, slots=True)
class InvalidActivation:
    adoption_identifier: str
    reason: str


@dataclass(frozen=True, slots=True)
class AdoptionConflict:
    adoption_identifiers: frozenset[str]
    conflicting_scopes: frozenset[Scope]
    purpose: str
    authority: int
    reason: str


@dataclass(frozen=True, slots=True)
class CoexistingAdoptions:
    adoptions: frozenset[Adoption]
    reason: str


@dataclass(frozen=True, slots=True)
class ResolutionPolicy:
    identifier: str
    kind: ResolutionKind
    preferred_model_identifier: str | None = None


@dataclass(frozen=True, slots=True)
class ResolvedAdoption:
    adoption: Adoption
    policy: ResolutionPolicy
    reason: str


@dataclass(frozen=True, slots=True)
class EpistemicAmbiguity:
    model_identifiers: frozenset[str]
    score: tuple[int, int]
    reason: str


@dataclass(frozen=True, slots=True)
class OperationalCommitment:
    adoption: Adoption
    selection_policy_identifier: str
    epistemic_state: EpistemicAmbiguity


@dataclass(frozen=True, slots=True)
class PostHocScope:
    model_identifier: str
    selected_scope: Scope
    selected_after_outcome_identifiers: tuple[str, ...]
    precommitted: bool


@dataclass(frozen=True, slots=True)
class SwitchRecord:
    identifier: str
    previous_adoption_identifier: str
    next_adoption_identifier: str
    reason: str
    switched_order: int


@dataclass(frozen=True, slots=True)
class CountermodelRejection:
    countermodel: str
    reason: str
