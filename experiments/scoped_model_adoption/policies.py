"""Role-sensitive artifact derivation and scoped use."""

from __future__ import annotations

from .models import model_action
from .records import (
    ActionRecord,
    Activation,
    ArtifactUnavailable,
    DerivedPolicy,
    Lineage,
    Model,
    Prediction,
    PredictionRule,
    Revocation,
    RevocationPolicy,
    UnspecifiedRevocationPolicy,
    UnsupportedUse,
    UseMode,
    WorldCase,
)


def derive_artifact(
    activation: Activation,
    model: Model,
    requested_use: UseMode,
    *,
    derived_order: int,
    revocations: tuple[Revocation, ...] = (),
    snapshot_duration: int | None = None,
) -> (
    PredictionRule
    | DerivedPolicy
    | ArtifactUnavailable
    | UnspecifiedRevocationPolicy
    | UnsupportedUse
):
    adoption = activation.adoption
    if adoption.model_identifier != model.identifier:
        return ArtifactUnavailable(
            activation.identifier,
            "activation and supplied model differ",
        )
    if requested_use is UseMode.AUDIT or requested_use is not adoption.use_mode:
        return UnsupportedUse(
            adoption.identifier,
            requested_use,
            "requested role is unsupported by this adoption",
        )
    if any(
        item.adoption_identifier == adoption.identifier
        and item.revoked_order <= derived_order
        for item in revocations
    ):
        return ArtifactUnavailable(
            activation.identifier,
            "no new artifact may derive after revocation",
        )
    if adoption.revocation_policy is RevocationPolicy.UNSPECIFIED:
        return UnspecifiedRevocationPolicy(
            adoption.identifier,
            "live-linked versus snapshot authority was not declared",
        )
    expires = None
    if adoption.revocation_policy is RevocationPolicy.SNAPSHOT:
        if snapshot_duration is None or snapshot_duration <= 0:
            return UnspecifiedRevocationPolicy(
                adoption.identifier,
                "snapshot adoption requires a declared positive duration",
            )
        expires = derived_order + snapshot_duration
    lineage = Lineage(
        model.identifier,
        adoption.identifier,
        activation.identifier,
        derived_order,
    )
    if requested_use is UseMode.PREDICTIVE:
        return PredictionRule(
            f"prediction-rule:{adoption.identifier}:{derived_order}",
            model,
            adoption.scopes,
            lineage,
            adoption.revocation_policy,
            expires,
        )
    return DerivedPolicy(
        f"action-policy:{adoption.identifier}:{derived_order}",
        model,
        adoption.scopes,
        lineage,
        adoption.revocation_policy,
        expires,
    )


def predict_case(
    rule: PredictionRule | DerivedPolicy,
    case: WorldCase,
    *,
    recorded_order: int,
    revocations: tuple[Revocation, ...] = (),
) -> Prediction | ArtifactUnavailable:
    if not isinstance(rule, PredictionRule):
        return ArtifactUnavailable(
            rule.identifier,
            "control policy does not perform predictive reading",
        )
    unavailable = _unavailable(rule, case, recorded_order, revocations)
    if unavailable:
        return unavailable
    return Prediction(
        f"prediction:{rule.identifier}:{case.identifier}",
        rule.identifier,
        case.identifier,
        model_action(rule.model, case),
        recorded_order,
    )


def act_on_case(
    policy: DerivedPolicy | PredictionRule,
    case: WorldCase,
    *,
    produced_order: int,
    revocations: tuple[Revocation, ...] = (),
) -> ActionRecord | ArtifactUnavailable:
    if not isinstance(policy, DerivedPolicy):
        return ArtifactUnavailable(
            policy.identifier,
            "prediction rule does not authorize action",
        )
    unavailable = _unavailable(policy, case, produced_order, revocations)
    if unavailable:
        return unavailable
    return ActionRecord(
        f"action:{policy.identifier}:{case.identifier}:{produced_order}",
        policy.identifier,
        case.identifier,
        model_action(policy.model, case),
        policy.lineage,
        produced_order,
    )


def _unavailable(
    artifact: PredictionRule | DerivedPolicy,
    case: WorldCase,
    current_order: int,
    revocations: tuple[Revocation, ...],
) -> ArtifactUnavailable | None:
    if case.scope not in artifact.scopes:
        return ArtifactUnavailable(
            artifact.identifier,
            f"artifact has no authority in {case.scope.value}",
        )
    revocation = next(
        (
            item
            for item in revocations
            if item.adoption_identifier == artifact.lineage.adoption_identifier
            and item.revoked_order <= current_order
        ),
        None,
    )
    if revocation and artifact.revocation_policy is RevocationPolicy.LIVE_LINKED:
        return ArtifactUnavailable(
            artifact.identifier,
            "live-linked artifact lost authority when adoption was revoked",
        )
    if artifact.expires_order is not None and current_order > artifact.expires_order:
        return ArtifactUnavailable(
            artifact.identifier,
            "snapshot authority expired",
        )
    return None
