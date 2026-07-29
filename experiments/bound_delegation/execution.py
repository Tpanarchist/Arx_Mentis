"""Per-action admission, authority, scope, resource, budget, and lease checks."""

from __future__ import annotations

from dataclasses import replace

from .derivation import admit_artifact
from .leases import lease_active
from .records import (
    Action,
    ActionKind,
    ActionSpec,
    Activation,
    AuditView,
    Capability,
    ControlView,
    Delegate,
    DerivationRegistry,
    Environment,
    ExecutionResult,
    InadmissibleArtifact,
    Refusal,
    RefusalKind,
    Revocation,
    RevocationMode,
    Trace,
    UnspecifiedRevocation,
)
from .world import compartment_state, replace_compartment

EMPTY_TRACE = Trace((), (), ())


def activate_delegate(
    delegate: Delegate,
    registry: DerivationRegistry,
    *,
    step: int,
    revocations: tuple[Revocation, ...] = (),
) -> Activation | InadmissibleArtifact | Refusal | UnspecifiedRevocation:
    admission = admit_artifact(delegate, registry)
    if isinstance(admission, InadmissibleArtifact):
        return admission
    if delegate.authority.revocation_mode is RevocationMode.UNSPECIFIED:
        return UnspecifiedRevocation(
            delegate.identifier,
            "live-linked versus snapshot lifecycle was not declared",
        )
    if not lease_active(delegate.authority.lease, step):
        return Refusal(
            delegate.identifier,
            RefusalKind.LEASE_INACTIVE,
            "delegate lease is inactive at activation",
            _placeholder_environment(),
            EMPTY_TRACE,
        )
    if _revoked(delegate, revocations, step):
        return Refusal(
            delegate.identifier,
            RefusalKind.REVOKED,
            "live-linked principal authority was revoked",
            _placeholder_environment(),
            EMPTY_TRACE,
        )
    return Activation(
        f"activation:{delegate.identifier}:{step}", delegate.identifier, step
    )


def execute_action(
    view: AuditView | ControlView,
    delegate: Delegate,
    activation: Activation,
    spec: ActionSpec,
    environment: Environment,
    trace: Trace,
    registry: DerivationRegistry,
    *,
    step: int,
    revocations: tuple[Revocation, ...] = (),
) -> ExecutionResult | Refusal | InadmissibleArtifact | UnspecifiedRevocation:
    if not isinstance(view, ControlView):
        return Refusal(
            delegate.identifier,
            RefusalKind.ROLE_UNAUTHORIZED,
            "audit interpretation carries no control authority",
            environment,
            trace,
        )
    admission = admit_artifact(delegate, registry)
    if isinstance(admission, InadmissibleArtifact):
        return admission
    if activation.delegate_identifier != delegate.identifier:
        return Refusal(
            delegate.identifier,
            RefusalKind.INADMISSIBLE,
            "activation belongs to another delegate",
            environment,
            trace,
        )
    authority = view.authority
    if authority is None or view.lineage is None:
        return Refusal(
            delegate.identifier,
            RefusalKind.ROLE_UNAUTHORIZED,
            "control reading lacks authority or admitted lineage",
            environment,
            trace,
        )
    if authority.revocation_mode is RevocationMode.UNSPECIFIED:
        return UnspecifiedRevocation(
            delegate.identifier,
            "live-linked versus snapshot lifecycle was not declared",
        )
    if not lease_active(authority.lease, step):
        return _refuse(
            delegate,
            RefusalKind.LEASE_INACTIVE,
            "lease is inactive for this action",
            environment,
            trace,
        )
    if _revoked(delegate, revocations, step):
        return _refuse(
            delegate,
            RefusalKind.REVOKED,
            "live-linked principal authority was revoked",
            environment,
            trace,
        )
    used = sum(
        item.delegate_identifier == delegate.identifier for item in trace.actions
    )
    if used >= authority.budget.maximum_actions:
        return _refuse(
            delegate,
            RefusalKind.BUDGET_EXHAUSTED,
            "action budget is exhausted",
            environment,
            trace,
        )
    required = _required_capability(spec.kind)
    if required not in authority.capabilities:
        return _refuse(
            delegate,
            RefusalKind.MISSING_CAPABILITY,
            f"authority lacks {required.value}",
            environment,
            trace,
        )
    direct_scopes = frozenset(
        item for item in (spec.source, spec.target) if item is not None
    )
    if not direct_scopes <= authority.scopes:
        return _refuse(
            delegate,
            RefusalKind.SCOPE_ESCAPE,
            "action addresses a compartment outside delegated scope",
            environment,
            trace,
        )
    if spec.units > authority.maximum_transfer_units:
        return _refuse(
            delegate,
            RefusalKind.TRANSFER_LIMIT,
            "action exceeds the per-action transfer limit",
            environment,
            trace,
        )
    if not _resources_available(spec, environment):
        return _refuse(
            delegate,
            RefusalKind.RESOURCE_UNAVAILABLE,
            "required environment resource is unavailable",
            environment,
            trace,
        )

    action = Action(
        f"action:{delegate.identifier}:{step}:{len(trace.actions)}",
        delegate.identifier,
        spec.kind,
        spec.source,
        spec.target,
        spec.units,
        direct_scopes,
        authority.identifier,
        step,
    )
    updated = _apply(spec, environment, action)
    return ExecutionResult(
        updated, action, replace(trace, actions=(*trace.actions, action))
    )


def _required_capability(kind: ActionKind) -> Capability:
    return {
        ActionKind.READ: Capability.READ_INVENTORY,
        ActionKind.TRANSFER: Capability.TRANSFER,
        ActionKind.WRITE_OPERATION: Capability.WRITE_OPERATION,
        ActionKind.CONSUME_SHARED: Capability.CONSUME_SHARED,
        ActionKind.ALTER_PROTECTED: Capability.ALTER_PROTECTED,
    }[kind]


def _resources_available(spec: ActionSpec, environment: Environment) -> bool:
    if spec.kind is ActionKind.TRANSFER:
        return compartment_state(environment, spec.source).resource_units >= spec.units
    if spec.kind is ActionKind.CONSUME_SHARED:
        return environment.shared_resource_units >= spec.units
    return True


def _apply(spec: ActionSpec, environment: Environment, action: Action) -> Environment:
    if spec.kind is ActionKind.TRANSFER:
        assert spec.target is not None
        source = compartment_state(environment, spec.source)
        target = compartment_state(environment, spec.target)
        updated = replace_compartment(
            environment,
            replace(source, resource_units=source.resource_units - spec.units),
        )
        return replace_compartment(
            updated,
            replace(
                target,
                resource_units=target.resource_units + spec.units,
                writable_records=(*target.writable_records, action.identifier),
            ),
        )
    if spec.kind is ActionKind.CONSUME_SHARED:
        source = compartment_state(environment, spec.source)
        updated = replace_compartment(
            environment,
            replace(
                source, writable_records=(*source.writable_records, action.identifier)
            ),
        )
        return replace(
            updated,
            shared_resource_units=updated.shared_resource_units - spec.units,
        )
    state = compartment_state(environment, spec.source)
    if spec.kind is ActionKind.WRITE_OPERATION:
        state = replace(
            state,
            writable_records=(*state.writable_records, action.identifier),
        )
    elif spec.kind is ActionKind.ALTER_PROTECTED:
        state = replace(
            state,
            protected_records=(*state.protected_records, action.identifier),
        )
    return replace_compartment(environment, state)


def _revoked(
    delegate: Delegate,
    revocations: tuple[Revocation, ...],
    step: int,
) -> bool:
    if delegate.authority.revocation_mode is RevocationMode.SNAPSHOT:
        return False
    return any(
        item.principal_identifier == delegate.lineage.principal_identifier
        and item.revoked_step <= step
        for item in revocations
    )


def _refuse(
    delegate: Delegate,
    kind: RefusalKind,
    reason: str,
    environment: Environment,
    trace: Trace,
) -> Refusal:
    return Refusal(delegate.identifier, kind, reason, environment, trace)


def _placeholder_environment() -> Environment:
    return Environment((), 0, 0)
