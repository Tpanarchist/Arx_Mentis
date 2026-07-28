"""Immutable neutral records for feedback and model revision."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive"


class Split(Enum):
    CALIBRATION = "calibration"
    HOLDOUT = "holdout"
    ADAPTIVE = "adaptive"


class ModelKind(Enum):
    FEATURE_X = "feature-x"
    FEATURE_Y = "feature-y"
    XOR = "xor"
    FEATURE_LOOKUP = "feature-lookup"
    MEMORIZE = "memorize"
    CONSTANT = "constant"


class AssessmentKind(Enum):
    EXACT = "exact"
    ALWAYS_SUCCESS = "always-success"


class RevisionKind(Enum):
    GENERALIZE_XOR = "generalize-xor"
    EQUIVALENT_LOOKUP = "equivalent-lookup"
    OVERFIT_MEMORIZE = "overfit-memorize"
    NO_OP = "no-op"


class MechanismKind(Enum):
    PASSIVE = "passive"
    ADAPTIVE_INTERVENTION = "adaptive-intervention"


class InterventionKind(Enum):
    ALIGN_TO_PREDICTION = "align-to-prediction"


class SelectionKind(Enum):
    HIGHER_HOLDOUT_SCORE = "higher-holdout-score"
    LOWER_COMPLEXITY = "lower-complexity"


class ReportKind(Enum):
    ALL = "all"
    SUCCESSES_ONLY = "successes-only"


@dataclass(frozen=True, slots=True)
class WorldCase:
    identifier: str
    feature_x: bool
    feature_y: bool
    outcome: Outcome


@dataclass(frozen=True, slots=True)
class CaseInput:
    identifier: str
    feature_x: bool
    feature_y: bool


@dataclass(frozen=True, slots=True)
class Model:
    identifier: str
    kind: ModelKind
    parameters: tuple[tuple[str, Outcome], ...]
    complexity: int
    descriptive: bool = True


@dataclass(frozen=True, slots=True)
class Lineage:
    source_version_identifier: str
    evidence_set_identifier: str
    revision_rule_identifier: str
    created_order: int


@dataclass(frozen=True, slots=True)
class ModelVersion:
    identifier: str
    model: Model
    ordinal: int
    lineage: Lineage | None


@dataclass(frozen=True, slots=True)
class TrialPlan:
    identifier: str
    model_version_identifier: str
    case_identifiers: tuple[str, ...]
    split: Split
    assessment_rule_identifier: str
    intervention_identifier: str | None
    committed_order: int
    outcomes_exposed_at_commit: bool = False


@dataclass(frozen=True, slots=True)
class Prediction:
    identifier: str
    plan_identifier: str
    model_version_identifier: str
    case_identifier: str
    outcome: Outcome
    committed_order: int


@dataclass(frozen=True, slots=True)
class Intervention:
    identifier: str
    source_model_version_identifier: str
    kind: InterventionKind
    declared_order: int


@dataclass(frozen=True, slots=True)
class CausalRecord:
    case_identifier: str
    mechanism: MechanismKind
    passive_outcome: Outcome
    produced_outcome: Outcome
    model_version_identifier: str
    intervention_identifier: str | None


@dataclass(frozen=True, slots=True)
class TrialOccurrence:
    identifier: str
    plan_identifier: str
    prediction_identifier: str
    case_identifier: str
    outcome: Outcome
    occurred_order: int
    causal_record: CausalRecord


@dataclass(frozen=True, slots=True)
class Observation:
    identifier: str
    occurrence_identifier: str
    prediction_identifier: str
    case_identifier: str
    outcome: Outcome
    available_order: int


@dataclass(frozen=True, slots=True)
class HistoricalTrial:
    identifier: str
    prediction: Prediction
    occurrence: TrialOccurrence
    observation: Observation


@dataclass(frozen=True, slots=True)
class TrialBundle:
    plan: TrialPlan
    predictions: tuple[Prediction, ...]
    occurrences: tuple[TrialOccurrence, ...]
    observations: tuple[Observation, ...]
    history: tuple[HistoricalTrial, ...]


@dataclass(frozen=True, slots=True)
class AssessmentRule:
    identifier: str
    kind: AssessmentKind
    declared_order: int


@dataclass(frozen=True, slots=True)
class CaseAssessment:
    case_identifier: str
    prediction_identifier: str
    observation_identifier: str
    predicted: Outcome
    observed: Outcome
    accepted: bool


@dataclass(frozen=True, slots=True)
class Assessment:
    identifier: str
    model_version_identifier: str
    rule: AssessmentRule
    cases: tuple[CaseAssessment, ...]
    accepted_count: int
    total_count: int
    created_order: int


@dataclass(frozen=True, slots=True)
class EvidenceEntry:
    case_identifier: str
    effective_outcome: Outcome
    source_record_identifiers: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvidenceSet:
    identifier: str
    entries: tuple[EvidenceEntry, ...]
    source_assessment_identifier: str
    admitted_order: int
    previous_evidence_set_identifier: str | None = None
    correction_identifiers: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RevisionRule:
    identifier: str
    kind: RevisionKind
    admissible_case_identifiers: frozenset[str]
    declared_order: int


@dataclass(frozen=True, slots=True)
class Revision:
    identifier: str
    source_version: ModelVersion
    evidence_set: EvidenceSet
    rule: RevisionRule
    result_version: ModelVersion
    created_order: int


@dataclass(frozen=True, slots=True)
class NoRevision:
    source_version: ModelVersion
    evidence_set_identifier: str | None
    rule_identifier: str | None
    evidence_evaluated: bool
    reason: str


@dataclass(frozen=True, slots=True)
class EvidenceLeakage:
    source_version: ModelVersion
    evidence_set: EvidenceSet
    rule: RevisionRule
    forbidden_case_identifiers: frozenset[str]
    reason: str


@dataclass(frozen=True, slots=True)
class InvalidPlan:
    plan: TrialPlan
    reason: str


@dataclass(frozen=True, slots=True)
class InvalidEvidence:
    evidence_set_identifier: str
    reason: str


@dataclass(frozen=True, slots=True)
class Correction:
    identifier: str
    original_observation_identifier: str
    case_identifier: str
    corrected_outcome: Outcome
    reason: str
    recorded_order: int


@dataclass(frozen=True, slots=True)
class Holdout:
    identifier: str
    case_identifiers: frozenset[str]
    sealed: bool


@dataclass(frozen=True, slots=True)
class ReplayPrediction:
    case_identifier: str
    model_version_identifier: str
    would_predict: Outcome


@dataclass(frozen=True, slots=True)
class Replay:
    identifier: str
    model_version: ModelVersion
    predictions: tuple[ReplayPrediction, ...]
    historical_prediction_identifiers: tuple[str, ...]
    created_order: int


@dataclass(frozen=True, slots=True)
class ScoredRevision:
    revision: Revision
    calibration_score: tuple[int, int]
    holdout_score: tuple[int, int]


@dataclass(frozen=True, slots=True)
class RevisionConflict:
    candidate_revision_identifiers: frozenset[str]
    score: tuple[int, int]
    reason: str


@dataclass(frozen=True, slots=True)
class SelectionPolicy:
    identifier: str
    kind: SelectionKind


@dataclass(frozen=True, slots=True)
class SelectedRevision:
    candidate: ScoredRevision
    policy: SelectionPolicy
    reason: str


@dataclass(frozen=True, slots=True)
class AssessmentReport:
    identifier: str
    kind: ReportKind
    source_assessment: Assessment
    included_case_identifiers: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ObserverAttribution:
    observation_identifier: str
    candidate_model_version_identifiers: frozenset[str]
    confidence: tuple[tuple[str, int], ...]
    selected_model_version_identifier: str | None
    world_cause_available: bool


@dataclass(frozen=True, slots=True)
class CountermodelRejection:
    countermodel: str
    reason: str
