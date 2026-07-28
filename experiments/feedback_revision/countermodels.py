"""Owned rejections for hostile feedback and revision reductions."""

from __future__ import annotations

from .records import CountermodelRejection


def reject_prediction_rewriting() -> CountermodelRejection:
    return _reject(
        "prediction-rewriting", "later outcomes cannot alter committed predictions"
    )


def reject_failure_deletion() -> CountermodelRejection:
    return _reject(
        "failure-deletion", "a filtered report cannot delete historical trials"
    )


def reject_outcome_defined_success() -> CountermodelRejection:
    return _reject(
        "outcome-defined-success",
        "a later rule creates a new assessment rather than repairing an old prediction",
    )


def reject_evidence_leakage() -> CountermodelRejection:
    return _reject("evidence-leakage", "holdout outcomes are unavailable to revision")


def reject_one_event_validation() -> CountermodelRejection:
    return _reject(
        "one-event-validation", "one match is compatible with multiple models"
    )


def reject_overfit_as_improvement() -> CountermodelRejection:
    return _reject(
        "overfit-equals-improvement",
        "calibration fit does not establish performance outside revision evidence",
    )


def reject_current_version_identity() -> CountermodelRejection:
    return _reject(
        "current-version-identity",
        "equal model behavior does not erase distinct version lineage",
    )


def reject_replay_as_history() -> CountermodelRejection:
    return _reject(
        "replay-equals-history",
        "counterfactual replay records would-predict, not did-predict",
    )


def reject_self_fulfillment() -> CountermodelRejection:
    return _reject(
        "self-fulfillment-equals-prediction",
        "intervention-caused outcomes are not passive confirmation",
    )


def reject_revision_order_tie_breaking() -> CountermodelRejection:
    return _reject(
        "revision-order-tie-breaking",
        "equal scores do not declare list, call, or storage order as a policy",
    )


def reject_contradiction_erasure() -> CountermodelRejection:
    return _reject(
        "contradiction-erasure",
        "correction adds records and reassessment instead of deleting prior evidence",
    )


def reject_model_as_truth() -> CountermodelRejection:
    return _reject(
        "model-is-truth",
        "a selected working model is not the world's declared causal structure",
    )


def _reject(countermodel: str, reason: str) -> CountermodelRejection:
    return CountermodelRejection(countermodel, reason)
