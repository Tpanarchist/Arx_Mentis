"""Owned rejections for hostile scoped-adoption reductions."""

from __future__ import annotations

from .records import CountermodelRejection


def reject_model_as_adoption() -> CountermodelRejection:
    return _reject("model-is-adoption", "availability grants no operational authority")


def reject_assessment_as_authority() -> CountermodelRejection:
    return _reject("assessment-is-authority", "score does not activate a model")


def reject_adoption_as_truth() -> CountermodelRejection:
    return _reject("adoption-is-truth", "operational authorization is not ontology")


def reject_global_current_model() -> CountermodelRejection:
    return _reject("global-current-model", "authority is attached to declared scopes")


def reject_local_as_universal() -> CountermodelRejection:
    return _reject(
        "local-usefulness-is-universal-validity", "local score does not widen scope"
    )


def reject_post_hoc_scope() -> CountermodelRejection:
    return _reject(
        "post-hoc-scope", "scope selected after outcomes is not precommitted"
    )


def reject_silent_switching() -> CountermodelRejection:
    return _reject("silent-switching", "model transitions require prospective records")


def reject_first_adoption_wins() -> CountermodelRejection:
    return _reject("first-adoption-wins", "incidental storage order is not a policy")


def reject_success_proves_model() -> CountermodelRejection:
    return _reject("success-proves-model", "one action can follow from several models")


def reject_revocation_erases_history() -> CountermodelRejection:
    return _reject(
        "revocation-erases-history", "revocation changes future authority only"
    )


def reject_implicit_revocation_policy() -> CountermodelRejection:
    return _reject(
        "implicit-revocation-policy", "cascade versus snapshot must be declared"
    )


def reject_confidence_as_commitment() -> CountermodelRejection:
    return _reject(
        "confidence-is-commitment", "epistemic support grants no action authority"
    )


def reject_commitment_as_confidence() -> CountermodelRejection:
    return _reject(
        "commitment-is-confidence", "operational necessity does not raise support"
    )


def reject_self_fulfillment_as_validation() -> CountermodelRejection:
    return _reject(
        "self-fulfillment-is-validation", "model-guided action participated in success"
    )


def reject_same_policy_as_same_origin() -> CountermodelRejection:
    return _reject(
        "same-policy-is-same-origin", "equal action does not erase model lineage"
    )


def _reject(countermodel: str, reason: str) -> CountermodelRejection:
    return CountermodelRejection(countermodel, reason)
