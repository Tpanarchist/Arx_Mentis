"""Owned rejections for hostile delegation reductions."""

from __future__ import annotations

from .records import CountermodelRejection


def reject_role_grants_authority() -> CountermodelRejection:
    return _reject(
        "role-grants-authority", "readable control instructions are not permission"
    )


def reject_compiled_as_unrestricted() -> CountermodelRejection:
    return _reject(
        "compiled-means-unrestricted", "source independence leaves other dependencies"
    )


def reject_authority_as_instruction_data() -> CountermodelRejection:
    return _reject(
        "authority-stored-as-instruction-data", "copying instructions copies no grant"
    )


def reject_scope_as_consequence_boundary() -> CountermodelRejection:
    return _reject(
        "scope-means-consequence-boundary",
        "indirect consequences may cross direct write scope",
    )


def reject_revocation_erases_history() -> CountermodelRejection:
    return _reject(
        "revocation-erases-history", "past actions retain their then-current authority"
    )


def reject_revocation_always_cascades() -> CountermodelRejection:
    return _reject(
        "source-revocation-always-cascades", "declared snapshots survive to expiry"
    )


def reject_revocation_never_cascades() -> CountermodelRejection:
    return _reject(
        "source-revocation-never-cascades", "declared live links stop immediately"
    )


def reject_child_amplification() -> CountermodelRejection:
    return _reject(
        "child-delegation-amplifies-power",
        "child authority must not exceed parent authority",
    )


def reject_activation_only_lease_check() -> CountermodelRejection:
    return _reject(
        "lease-checked-only-at-activation", "every action rechecks its lease"
    )


def reject_post_mutation_budget_check() -> CountermodelRejection:
    return _reject(
        "budget-checked-after-mutation",
        "exhaustion is determined before state transition",
    )


def reject_success_justifies_excess() -> CountermodelRejection:
    return _reject(
        "success-justifies-excess-authority",
        "usefulness cannot repair unauthorized action",
    )


def reject_compensation_deletes_harm() -> CountermodelRejection:
    return _reject("compensation-deletes-harm", "repair appends to the causal record")


def reject_principal_only_causation() -> CountermodelRejection:
    return _reject(
        "principal-only-causation",
        "delegate action and environment mechanics remain causal",
    )


def reject_delegate_only_causation() -> CountermodelRejection:
    return _reject(
        "delegate-only-causation", "source derivation and authority remain in lineage"
    )


def reject_same_artifact_same_authority() -> CountermodelRejection:
    return _reject(
        "same-artifact-means-same-authority",
        "equal local instructions do not erase lineage",
    )


def _reject(countermodel: str, reason: str) -> CountermodelRejection:
    return CountermodelRejection(countermodel, reason)
