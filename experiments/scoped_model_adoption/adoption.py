"""Explicit scope-bound adoption and order-independent overlap handling."""

from __future__ import annotations

from .records import (
    ActivationState,
    Adoption,
    AdoptionConflict,
    CoexistingAdoptions,
    EpistemicAmbiguity,
    Model,
    OperationalCommitment,
    ResolutionKind,
    ResolutionPolicy,
    ResolvedAdoption,
    RevocationPolicy,
    Scope,
    UseMode,
)


def adopt(
    identifier: str,
    model: Model,
    *,
    purpose: str,
    use_mode: UseMode,
    scopes: frozenset[Scope],
    authority: int,
    revocation_policy: RevocationPolicy,
    adopted_order: int = 20,
    start_condition: str = "explicit activation",
    end_condition: str = "declared revocation or expiry",
    provenance: tuple[str, ...] = (),
) -> Adoption:
    return Adoption(
        identifier,
        model.identifier,
        purpose,
        use_mode,
        scopes,
        authority,
        start_condition,
        end_condition,
        ActivationState.INACTIVE,
        revocation_policy,
        provenance,
        adopted_order,
    )


def reconcile_adoptions(
    adoptions: tuple[Adoption, ...],
    policy: ResolutionPolicy | None = None,
) -> CoexistingAdoptions | AdoptionConflict | ResolvedAdoption:
    overlap = _overlap(adoptions)
    if not overlap:
        return CoexistingAdoptions(
            frozenset(adoptions),
            "adoptions do not compete over one scoped operation",
        )
    purpose = adoptions[0].purpose
    authority = max(item.authority for item in adoptions)
    if policy is None:
        return AdoptionConflict(
            frozenset(item.identifier for item in adoptions),
            overlap,
            purpose,
            authority,
            "overlap has no declared resolution policy",
        )
    selected = _resolve(adoptions, policy)
    if selected is None:
        return AdoptionConflict(
            frozenset(item.identifier for item in adoptions),
            overlap,
            purpose,
            authority,
            "declared policy does not produce one admissible adoption",
        )
    return ResolvedAdoption(
        selected, policy, "declared semantic policy resolved overlap"
    )


def _overlap(adoptions: tuple[Adoption, ...]) -> frozenset[Scope]:
    if len(adoptions) < 2:
        return frozenset()
    first, *rest = adoptions
    scopes = set(first.scopes)
    for adoption in rest:
        if adoption.purpose != first.purpose or adoption.use_mode is not first.use_mode:
            return frozenset()
        scopes &= adoption.scopes
    return frozenset(scopes)


def _resolve(
    adoptions: tuple[Adoption, ...],
    policy: ResolutionPolicy,
) -> Adoption | None:
    if policy.kind is ResolutionKind.HIGHER_AUTHORITY:
        highest = max(item.authority for item in adoptions)
        leaders = tuple(item for item in adoptions if item.authority == highest)
        return leaders[0] if len(leaders) == 1 else None
    if policy.kind is ResolutionKind.PREFERRED_MODEL:
        leaders = tuple(
            item
            for item in adoptions
            if item.model_identifier == policy.preferred_model_identifier
        )
        return leaders[0] if len(leaders) == 1 else None
    raise AssertionError(f"unhandled resolution kind: {policy.kind}")


def commit_operationally(
    ambiguity: EpistemicAmbiguity,
    adoption: Adoption,
    *,
    selection_policy_identifier: str,
) -> OperationalCommitment:
    if adoption.model_identifier not in ambiguity.model_identifiers:
        raise ValueError("operational model is outside the epistemic alternatives")
    return OperationalCommitment(
        adoption,
        selection_policy_identifier,
        ambiguity,
    )
