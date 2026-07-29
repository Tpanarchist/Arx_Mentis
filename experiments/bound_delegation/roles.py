"""Inspectable roles that do not manufacture authority."""

from __future__ import annotations

from .records import AuditView, ControlView, Delegate, DelegateCopy, Role


def read_as(
    artifact: Delegate | DelegateCopy,
    role: Role,
) -> AuditView | ControlView:
    if role is Role.AUDIT:
        return AuditView(
            artifact.identifier,
            artifact.instructions,
            tuple(
                f"{item.kind.value}:{item.source.value}:"
                f"{item.target.value if item.target else '-'}:{item.units}"
                for item in artifact.instructions
            ),
        )
    return ControlView(
        artifact.identifier,
        artifact.instructions,
        artifact.authority,
        artifact.lineage,
    )
