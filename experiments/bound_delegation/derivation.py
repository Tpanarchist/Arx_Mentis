"""Source-preserving derivation, admission, copying, and attenuation."""

from __future__ import annotations

from .records import (
    Admission,
    Authority,
    AuthorityAmplification,
    Capability,
    Delegate,
    DelegateCopy,
    Derivation,
    DerivationRegistry,
    InadmissibleArtifact,
    Lineage,
    Principal,
    Revocation,
    SourceAvailability,
    SourcePlan,
)


def derive_delegate(
    plan: SourcePlan,
    principal: Principal,
    authority: Authority,
    *,
    identifier: str = "delegate:rebalance",
    derived_step: int = 1,
    revocations: tuple[Revocation, ...] = (),
) -> Derivation | InadmissibleArtifact:
    if any(
        item.principal_identifier == principal.identifier
        and item.revoked_step <= derived_step
        for item in revocations
    ):
        return InadmissibleArtifact(
            identifier,
            "principal revocation blocks new delegate derivation",
        )
    lineage = Lineage(
        f"lineage:{identifier}",
        plan.identifier,
        principal.identifier,
        parent_delegate_identifier=None,
        derived_step=derived_step,
    )
    delegate = Delegate(
        identifier,
        plan.instructions,
        authority,
        lineage,
        compiled=True,
    )
    return Derivation(
        plan,
        delegate,
        DerivationRegistry(frozenset({lineage.identifier})),
    )


def release_source(plan: SourcePlan, *, changed_step: int) -> SourceAvailability:
    return SourceAvailability(
        plan.identifier, available=False, changed_step=changed_step
    )


def copy_delegate(
    delegate: Delegate,
    *,
    identifier: str,
    include_authority: bool,
    include_lineage: bool,
) -> DelegateCopy:
    return DelegateCopy(
        identifier,
        delegate.instructions,
        delegate.authority if include_authority else None,
        delegate.lineage if include_lineage else None,
        delegate.compiled,
    )


def admit_artifact(
    artifact: Delegate | DelegateCopy,
    registry: DerivationRegistry,
) -> Admission | InadmissibleArtifact:
    if artifact.authority is None:
        return InadmissibleArtifact(
            artifact.identifier,
            "instruction copy carries no authority",
        )
    if artifact.lineage is None:
        return InadmissibleArtifact(
            artifact.identifier,
            "artifact carries no derivation lineage",
        )
    if artifact.lineage.identifier not in registry.admitted_lineage_identifiers:
        return InadmissibleArtifact(
            artifact.identifier,
            "lineage is not admitted by the derivation registry",
        )
    return Admission(artifact.identifier, artifact.lineage.identifier, admitted=True)


def derive_child(
    parent: Delegate,
    requested_authority: Authority,
    registry: DerivationRegistry,
    *,
    identifier: str,
    derived_step: int,
) -> Derivation | AuthorityAmplification | InadmissibleArtifact:
    admission = admit_artifact(parent, registry)
    if isinstance(admission, InadmissibleArtifact):
        return admission
    if Capability.DERIVE_DELEGATE not in parent.authority.capabilities:
        return AuthorityAmplification(
            parent.identifier,
            requested_authority,
            frozenset({Capability.DERIVE_DELEGATE}),
            frozenset(),
            "parent has no capability to derive another delegate",
        )
    excess_capabilities = (
        requested_authority.capabilities - parent.authority.capabilities
    )
    excess_scopes = requested_authority.scopes - parent.authority.scopes
    quantitative_excess = (
        requested_authority.maximum_transfer_units
        > parent.authority.maximum_transfer_units
        or requested_authority.budget.maximum_actions
        > parent.authority.budget.maximum_actions
        or requested_authority.lease.start_step < parent.authority.lease.start_step
        or requested_authority.lease.end_step > parent.authority.lease.end_step
    )
    if excess_capabilities or excess_scopes or quantitative_excess:
        return AuthorityAmplification(
            parent.identifier,
            requested_authority,
            frozenset(excess_capabilities),
            frozenset(excess_scopes),
            "child authority must be a subset of parent authority",
        )
    lineage = Lineage(
        f"lineage:{identifier}",
        parent.lineage.source_plan_identifier,
        parent.lineage.principal_identifier,
        parent.identifier,
        derived_step,
    )
    child = Delegate(
        identifier,
        parent.instructions,
        requested_authority,
        lineage,
        compiled=True,
    )
    child_registry = DerivationRegistry(
        registry.admitted_lineage_identifiers | frozenset({lineage.identifier})
    )
    return Derivation(
        SourcePlan(
            parent.lineage.source_plan_identifier,
            parent.lineage.principal_identifier,
            "attenuated child delegation",
            parent.instructions,
        ),
        child,
        child_registry,
    )
