"""Declared authority and dependency profiles."""

from __future__ import annotations

from .records import (
    Authority,
    Budget,
    Capability,
    Compartment,
    DependencyValue,
    IndependenceProfile,
    Lease,
    RevocationMode,
)


def contained_authority(
    *,
    revocation_mode: RevocationMode = RevocationMode.LIVE_LINKED,
    priority: int = 5,
) -> Authority:
    return Authority(
        f"authority:contained:{revocation_mode.value}:{priority}",
        frozenset(
            {
                Capability.READ_INVENTORY,
                Capability.TRANSFER,
                Capability.WRITE_OPERATION,
            }
        ),
        frozenset({Compartment.NORTH, Compartment.CENTER}),
        maximum_transfer_units=2,
        lease=Lease(2, 5),
        budget=Budget(3),
        revocation_mode=revocation_mode,
        priority=priority,
    )


def delegating_authority() -> Authority:
    parent = contained_authority()
    return Authority(
        "authority:delegating",
        parent.capabilities | frozenset({Capability.DERIVE_DELEGATE}),
        parent.scopes,
        parent.maximum_transfer_units,
        parent.lease,
        parent.budget,
        parent.revocation_mode,
        parent.priority,
    )


def pressure_authority() -> Authority:
    return Authority(
        "authority:shared-pressure",
        frozenset({Capability.CONSUME_SHARED, Capability.WRITE_OPERATION}),
        frozenset({Compartment.NORTH}),
        maximum_transfer_units=2,
        lease=Lease(2, 5),
        budget=Budget(2),
        revocation_mode=RevocationMode.LIVE_LINKED,
        priority=4,
    )


def attenuated_authority(parent: Authority) -> Authority:
    return Authority(
        "authority:attenuated-child",
        frozenset({Capability.READ_INVENTORY, Capability.TRANSFER}),
        parent.scopes,
        maximum_transfer_units=1,
        lease=Lease(3, 4),
        budget=Budget(1),
        revocation_mode=parent.revocation_mode,
        priority=parent.priority - 1,
    )


def amplified_authority(parent: Authority) -> Authority:
    return Authority(
        "authority:amplified-child",
        parent.capabilities | frozenset({Capability.ALTER_PROTECTED}),
        parent.scopes | frozenset({Compartment.SOUTH}),
        maximum_transfer_units=parent.maximum_transfer_units + 1,
        lease=Lease(parent.lease.start_step, parent.lease.end_step + 1),
        budget=Budget(parent.budget.maximum_actions + 1),
        revocation_mode=parent.revocation_mode,
        priority=parent.priority + 1,
    )


def dependency_profile() -> IndependenceProfile:
    return IndependenceProfile(
        source_content=DependencyValue.INDEPENDENT,
        authority=DependencyValue.LEASE_DEPENDENT,
        resources=DependencyValue.ENVIRONMENT_DEPENDENT,
        scope=DependencyValue.FIXED,
        lifecycle=DependencyValue.REVOCABLE,
        interpretation=DependencyValue.COMPILED,
        provenance=DependencyValue.RETAINED,
    )
