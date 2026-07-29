"""Declared revocation policies and prospective switching."""

from __future__ import annotations

from .records import (
    Adoption,
    Revocation,
    RevocationPolicy,
    SwitchRecord,
    UnspecifiedRevocationPolicy,
)


def revoke(
    adoption: Adoption,
    *,
    reason: str,
    revoked_order: int,
) -> Revocation | UnspecifiedRevocationPolicy:
    if adoption.revocation_policy is RevocationPolicy.UNSPECIFIED:
        return UnspecifiedRevocationPolicy(
            adoption.identifier,
            "revocation cannot guess live-linked or snapshot behavior",
        )
    return Revocation(
        f"revocation:{adoption.identifier}:{revoked_order}",
        adoption.identifier,
        adoption.revocation_policy,
        reason,
        revoked_order,
    )


def record_switch(
    previous: Adoption,
    next_adoption: Adoption,
    *,
    reason: str,
    switched_order: int,
) -> SwitchRecord:
    return SwitchRecord(
        f"switch:{previous.identifier}:{next_adoption.identifier}:{switched_order}",
        previous.identifier,
        next_adoption.identifier,
        reason,
        switched_order,
    )
