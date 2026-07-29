"""Prospective principal revocation and delegate switching."""

from __future__ import annotations

from .records import Delegate, Principal, Revocation, SwitchRecord


def revoke_principal(
    principal: Principal,
    *,
    reason: str,
    revoked_step: int,
) -> Revocation:
    return Revocation(
        f"revocation:{principal.identifier}:{revoked_step}",
        principal.identifier,
        revoked_step,
        reason,
    )


def record_switch(
    previous: Delegate,
    next_delegate: Delegate,
    *,
    switched_step: int,
    reason: str,
) -> SwitchRecord:
    return SwitchRecord(
        f"switch:{previous.identifier}:{next_delegate.identifier}:{switched_step}",
        previous.identifier,
        next_delegate.identifier,
        switched_step,
        reason,
    )
