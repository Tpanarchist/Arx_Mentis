"""Immutable neutral records for bounded derived operation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Compartment(Enum):
    NORTH = "north"
    CENTER = "center"
    SOUTH = "south"


class Capability(Enum):
    READ_INVENTORY = "read-inventory"
    TRANSFER = "transfer"
    WRITE_OPERATION = "write-operation"
    CONSUME_SHARED = "consume-shared"
    ALTER_PROTECTED = "alter-protected"
    ACCESS_SOUTH = "access-south"
    DERIVE_DELEGATE = "derive-delegate"


class Role(Enum):
    AUDIT = "audit"
    CONTROL = "control"


class RevocationMode(Enum):
    LIVE_LINKED = "live-linked"
    SNAPSHOT = "snapshot"
    UNSPECIFIED = "unspecified"


class DependencyValue(Enum):
    INDEPENDENT = "independent"
    LEASE_DEPENDENT = "lease-dependent"
    ENVIRONMENT_DEPENDENT = "environment-dependent"
    FIXED = "fixed"
    REVOCABLE = "revocable"
    COMPILED = "compiled"
    RETAINED = "retained"


class ActionKind(Enum):
    READ = "read"
    TRANSFER = "transfer"
    WRITE_OPERATION = "write-operation"
    CONSUME_SHARED = "consume-shared"
    ALTER_PROTECTED = "alter-protected"


class RefusalKind(Enum):
    INADMISSIBLE = "inadmissible"
    MISSING_CAPABILITY = "missing-capability"
    SCOPE_ESCAPE = "scope-escape"
    TRANSFER_LIMIT = "transfer-limit"
    BUDGET_EXHAUSTED = "budget-exhausted"
    LEASE_INACTIVE = "lease-inactive"
    REVOKED = "revoked"
    RESOURCE_UNAVAILABLE = "resource-unavailable"
    ROLE_UNAUTHORIZED = "role-unauthorized"


class ConsequenceKind(Enum):
    SOUTH_SHORTAGE = "south-shortage"
    PRINCIPAL_RESOURCE_LOSS = "principal-resource-loss"
    REPAIRED_SHORTAGE = "repaired-shortage"


class ResolutionKind(Enum):
    HIGHER_PRIORITY = "higher-priority"
    PREFERRED_DELEGATE = "preferred-delegate"


@dataclass(frozen=True, slots=True)
class Principal:
    identifier: str
    authority_source: str
    resource_access: int


@dataclass(frozen=True, slots=True)
class ActionSpec:
    kind: ActionKind
    source: Compartment
    target: Compartment | None
    units: int


@dataclass(frozen=True, slots=True)
class SourcePlan:
    identifier: str
    principal_identifier: str
    role: str
    instructions: tuple[ActionSpec, ...]


@dataclass(frozen=True, slots=True)
class Lease:
    start_step: int
    end_step: int


@dataclass(frozen=True, slots=True)
class Budget:
    maximum_actions: int


@dataclass(frozen=True, slots=True)
class Authority:
    identifier: str
    capabilities: frozenset[Capability]
    scopes: frozenset[Compartment]
    maximum_transfer_units: int
    lease: Lease
    budget: Budget
    revocation_mode: RevocationMode
    priority: int


@dataclass(frozen=True, slots=True)
class Lineage:
    identifier: str
    source_plan_identifier: str
    principal_identifier: str
    parent_delegate_identifier: str | None
    derived_step: int


@dataclass(frozen=True, slots=True)
class Delegate:
    identifier: str
    instructions: tuple[ActionSpec, ...]
    authority: Authority
    lineage: Lineage
    compiled: bool


@dataclass(frozen=True, slots=True)
class Derivation:
    source_plan: SourcePlan
    delegate: Delegate
    registry: DerivationRegistry


@dataclass(frozen=True, slots=True)
class DelegateCopy:
    identifier: str
    instructions: tuple[ActionSpec, ...]
    authority: Authority | None
    lineage: Lineage | None
    compiled: bool


@dataclass(frozen=True, slots=True)
class DerivationRegistry:
    admitted_lineage_identifiers: frozenset[str]


@dataclass(frozen=True, slots=True)
class SourceAvailability:
    source_plan_identifier: str
    available: bool
    changed_step: int


@dataclass(frozen=True, slots=True)
class IndependenceProfile:
    source_content: DependencyValue
    authority: DependencyValue
    resources: DependencyValue
    scope: DependencyValue
    lifecycle: DependencyValue
    interpretation: DependencyValue
    provenance: DependencyValue


@dataclass(frozen=True, slots=True)
class AuditView:
    artifact_identifier: str
    instructions: tuple[ActionSpec, ...]
    explanation: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ControlView:
    artifact_identifier: str
    instructions: tuple[ActionSpec, ...]
    authority: Authority | None
    lineage: Lineage | None


@dataclass(frozen=True, slots=True)
class Activation:
    identifier: str
    delegate_identifier: str
    activated_step: int


@dataclass(frozen=True, slots=True)
class CompartmentState:
    compartment: Compartment
    readable_records: tuple[str, ...]
    writable_records: tuple[str, ...]
    protected_records: tuple[str, ...]
    resource_units: int
    external_connections: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Environment:
    compartments: tuple[CompartmentState, ...]
    shared_resource_units: int
    principal_resource_units: int


@dataclass(frozen=True, slots=True)
class Action:
    identifier: str
    delegate_identifier: str
    kind: ActionKind
    source: Compartment
    target: Compartment | None
    units: int
    direct_scopes: frozenset[Compartment]
    authority_identifier: str
    step: int


@dataclass(frozen=True, slots=True)
class Consequence:
    identifier: str
    kind: ConsequenceKind
    affected_compartment: Compartment | None
    amount: int
    causal_chain: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Spillover:
    action_identifier: str
    direct_scopes: frozenset[Compartment]
    consequence: Consequence


@dataclass(frozen=True, slots=True)
class ConsequenceResult:
    environment: Environment
    spillover: Spillover
    blowback: Consequence
    trace: Trace


@dataclass(frozen=True, slots=True)
class Revocation:
    identifier: str
    principal_identifier: str
    revoked_step: int
    reason: str


@dataclass(frozen=True, slots=True)
class Compensation:
    identifier: str
    original_consequence_identifier: str
    amount: int
    performed_step: int


@dataclass(frozen=True, slots=True)
class CompensationResult:
    environment: Environment
    compensation: Compensation
    repair_consequence: Consequence
    trace: Trace


@dataclass(frozen=True, slots=True)
class Trace:
    actions: tuple[Action, ...]
    consequences: tuple[Consequence, ...]
    compensations: tuple[Compensation, ...]


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    environment: Environment
    action: Action
    trace: Trace


@dataclass(frozen=True, slots=True)
class Refusal:
    delegate_identifier: str
    kind: RefusalKind
    reason: str
    environment: Environment
    trace: Trace


@dataclass(frozen=True, slots=True)
class InadmissibleArtifact:
    artifact_identifier: str
    reason: str


@dataclass(frozen=True, slots=True)
class Admission:
    artifact_identifier: str
    lineage_identifier: str
    admitted: bool


@dataclass(frozen=True, slots=True)
class AuthorityAmplification:
    parent_delegate_identifier: str
    requested_authority: Authority
    excess_capabilities: frozenset[Capability]
    excess_scopes: frozenset[Compartment]
    reason: str


@dataclass(frozen=True, slots=True)
class UnspecifiedRevocation:
    delegate_identifier: str
    reason: str


@dataclass(frozen=True, slots=True)
class AuthorityConflict:
    delegate_identifiers: frozenset[str]
    scopes: frozenset[Compartment]
    reason: str


@dataclass(frozen=True, slots=True)
class ResolutionPolicy:
    identifier: str
    kind: ResolutionKind
    preferred_delegate_identifier: str | None = None


@dataclass(frozen=True, slots=True)
class ResolvedDelegate:
    delegate: Delegate
    policy: ResolutionPolicy
    reason: str


@dataclass(frozen=True, slots=True)
class SwitchRecord:
    identifier: str
    previous_delegate_identifier: str
    next_delegate_identifier: str
    switched_step: int
    reason: str


@dataclass(frozen=True, slots=True)
class CountermodelRejection:
    countermodel: str
    reason: str
