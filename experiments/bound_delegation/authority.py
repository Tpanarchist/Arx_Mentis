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
