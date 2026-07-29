"""Activation as a distinct prospective authorization step."""

from __future__ import annotations

from .records import (
    Activation,
    ActivationState,
    Adoption,
    InvalidActivation,
    Revocation,
)


def activate(
    adoption: Adoption,
    *,
    activated_order: int,
    revocations: tuple[Revocation, ...] = (),
) -> Activation | InvalidActivation:
    if activated_order <= adoption.adopted_order:
        return InvalidActivation(
            adoption.identifier,
            "activation must occur after adoption",
        )
    if any(
        item.adoption_identifier == adoption.identifier
        and item.revoked_order <= activated_order
        for item in revocations
    ):
        return InvalidActivation(
            adoption.identifier,
            "revoked adoption cannot be activated prospectively",
        )
    return Activation(
        f"activation:{adoption.identifier}:{activated_order}",
        adoption,
        ActivationState.ACTIVE,
        activated_order,
    )
