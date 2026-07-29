"""Order-independent authority overlap and declared resolution."""

from __future__ import annotations

from .records import (
    AuthorityConflict,
    Delegate,
    ResolutionKind,
    ResolutionPolicy,
    ResolvedDelegate,
)


def reconcile_delegates(
    delegates: tuple[Delegate, ...],
    policy: ResolutionPolicy | None = None,
) -> AuthorityConflict | ResolvedDelegate:
    scopes = frozenset.intersection(*(item.authority.scopes for item in delegates))
    if policy is None:
        return AuthorityConflict(
            frozenset(item.identifier for item in delegates),
            scopes,
            "overlapping delegates have no declared resolution policy",
        )
    selected = _resolve(delegates, policy)
    if selected is None:
        return AuthorityConflict(
            frozenset(item.identifier for item in delegates),
            scopes,
            "declared policy does not produce a unique delegate",
        )
    return ResolvedDelegate(
        selected, policy, "declared semantic policy resolved overlap"
    )


def _resolve(
    delegates: tuple[Delegate, ...],
    policy: ResolutionPolicy,
) -> Delegate | None:
    if policy.kind is ResolutionKind.HIGHER_PRIORITY:
        maximum = max(item.authority.priority for item in delegates)
        leaders = tuple(
            item for item in delegates if item.authority.priority == maximum
        )
        return leaders[0] if len(leaders) == 1 else None
    leaders = tuple(
        item
        for item in delegates
        if item.identifier == policy.preferred_delegate_identifier
    )
    return leaders[0] if len(leaders) == 1 else None
