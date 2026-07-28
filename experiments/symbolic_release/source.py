"""Neutral records for sources, carriers, interpretation, and execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EncodingKind(Enum):
    TRANSPARENT = "transparent"
    COMPILED = "compiled"
    KEYED = "keyed"
    OPAQUE = "opaque"
    LOSSY = "lossy"


class ReadingRole(Enum):
    EXACT = "exact"
    NAVIGATION = "navigation"
    AUDIT = "audit"


class RejectionStage(Enum):
    SHAPE = "shape"
    DERIVATION = "derivation"
    AUTHORIZATION = "authorization"
    MEANING = "meaning"
    ACTIVATION = "activation"
    EXECUTION = "execution"


@dataclass(frozen=True, slots=True)
class SourceForm:
    identifier: str
    guidance: tuple[str, ...]
    destination: str
    minimum_resources: int
    explanation: str


@dataclass(frozen=True, slots=True)
class EncodingRule:
    identifier: str
    kind: EncodingKind


@dataclass(frozen=True, slots=True)
class EncodedField:
    name: str
    value: str


@dataclass(frozen=True, slots=True)
class Carrier:
    symbol: str
    rule_identifier: str
    derivation_tag: str
    fields: tuple[EncodedField, ...]


@dataclass(frozen=True, slots=True)
class DerivationRecord:
    source_identifier: str
    carrier: Carrier
    rule: EncodingRule
    authorized: bool


@dataclass(frozen=True, slots=True)
class Encoding:
    source: SourceForm
    rule: EncodingRule
    carrier: Carrier
    derivation: DerivationRecord


@dataclass(frozen=True, slots=True)
class DerivationRegistry:
    records: frozenset[DerivationRecord]


@dataclass(frozen=True, slots=True)
class InterpretationKey:
    identifier: str
    role: ReadingRole


@dataclass(frozen=True, slots=True)
class Decoder:
    identifier: str
    supported_readings: frozenset[tuple[str, ReadingRole]]


@dataclass(frozen=True, slots=True)
class Provenance:
    source_identifiers: tuple[str, ...]
    encoding_rule: str
    carrier_symbol: str
    history: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SourceReconstruction:
    source: SourceForm
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class CompiledPolicy:
    identifier: str
    actions: tuple[str, ...]
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class AcceptanceRule:
    identifier: str
    destination: str
    minimum_resources: int
    provenance: Provenance


DecodedArtifact = SourceReconstruction | CompiledPolicy | AcceptanceRule


@dataclass(frozen=True, slots=True)
class Interpretation:
    carrier: Carrier
    decoder_identifier: str
    key: InterpretationKey
    artifact: DecodedArtifact


@dataclass(frozen=True, slots=True)
class Activation:
    identifier: str
    policy: CompiledPolicy
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class WorldState:
    position: str
    resources: int


@dataclass(frozen=True, slots=True)
class ExecutionStep:
    action: str
    before: WorldState
    after: WorldState


@dataclass(frozen=True, slots=True)
class Execution:
    activation_identifier: str
    policy_identifier: str
    source_state: WorldState
    steps: tuple[ExecutionStep, ...]
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class Outcome:
    state: WorldState
    execution: Execution


@dataclass(frozen=True, slots=True)
class CarrierAssessment:
    well_shaped: bool
    derivable: bool
    authorized: bool
    meaningful: bool
    operative: bool


@dataclass(frozen=True, slots=True)
class UnsupportedInterpretation:
    carrier: Carrier
    decoder: Decoder
    key: InterpretationKey
    reason: str


@dataclass(frozen=True, slots=True)
class RejectedInterpretation:
    carrier: Carrier
    stage: RejectionStage
    reason: str


@dataclass(frozen=True, slots=True)
class RejectedActivation:
    subject: Carrier | Interpretation
    stage: RejectionStage
    reason: str


@dataclass(frozen=True, slots=True)
class ExecutionRefused:
    subject: Activation | Interpretation
    stage: RejectionStage
    reason: str


@dataclass(frozen=True, slots=True)
class EncodingCollision:
    carrier: Carrier
    source_identifiers: tuple[str, ...]
    reason: str


@dataclass(frozen=True, slots=True)
class IncompleteReconstruction:
    carrier: Carrier
    preserved_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AvailableSources:
    sources: tuple[SourceForm, ...]


@dataclass(frozen=True, slots=True)
class PendingCarrier:
    carrier: Carrier
    source_identifier: str
    rule: EncodingRule


@dataclass(frozen=True, slots=True)
class MissingDependency:
    pending: PendingCarrier
    missing_source: str
    reason: str


@dataclass(frozen=True, slots=True)
class RetainedBundle:
    source: SourceForm
    carrier: Carrier
    interpretation: Interpretation


@dataclass(frozen=True, slots=True)
class ReleasedBundle:
    carrier: Carrier
    interpretation: Interpretation
    source_available: bool
    provenance: Provenance


@dataclass(frozen=True, slots=True)
class ArtifactComparison:
    same_local_value: bool
    shared_source: bool
    same_provenance: bool


@dataclass(frozen=True, slots=True)
class OutcomeComparison:
    same_state: bool
    same_policy: bool
    same_decoding: bool
