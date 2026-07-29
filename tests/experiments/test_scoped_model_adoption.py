from __future__ import annotations

import ast
import subprocess
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import experiments.scoped_model_adoption.records as records_module
from experiments.scoped_model_adoption.activation import activate
from experiments.scoped_model_adoption.adoption import (
    adopt,
    commit_operationally,
    reconcile_adoptions,
)
from experiments.scoped_model_adoption.assessment import (
    assess_model,
    compare_assessments,
)
from experiments.scoped_model_adoption.countermodels import (
    reject_adoption_as_truth,
    reject_assessment_as_authority,
    reject_commitment_as_confidence,
    reject_confidence_as_commitment,
    reject_first_adoption_wins,
    reject_global_current_model,
    reject_implicit_revocation_policy,
    reject_local_as_universal,
    reject_model_as_adoption,
    reject_post_hoc_scope,
    reject_revocation_erases_history,
    reject_same_policy_as_same_origin,
    reject_self_fulfillment_as_validation,
    reject_silent_switching,
    reject_success_proves_model,
)
from experiments.scoped_model_adoption.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.scoped_model_adoption.models import (
    cooperation_model,
    model_action,
    model_x,
    model_y,
)
from experiments.scoped_model_adoption.observation import (
    assert_truth,
    observe_outcome,
    select_scope_post_hoc,
)
from experiments.scoped_model_adoption.policies import (
    act_on_case,
    derive_artifact,
    predict_case,
)
from experiments.scoped_model_adoption.records import (
    Action,
    ActionRecord,
    Activation,
    Adoption,
    AdoptionConflict,
    ArtifactUnavailable,
    CoexistingAdoptions,
    CountermodelRejection,
    DerivedPolicy,
    EpistemicAmbiguity,
    InvalidActivation,
    OperationalCommitment,
    Prediction,
    PredictionRule,
    ResolutionKind,
    ResolutionPolicy,
    ResolvedAdoption,
    Revocation,
    RevocationPolicy,
    Scope,
    TruthAssertion,
    UnspecifiedRevocationPolicy,
    UnsupportedUse,
    UseMode,
)
from experiments.scoped_model_adoption.revocation import record_switch, revoke
from experiments.scoped_model_adoption.scenarios import (
    execute_scoped_composite,
    scoped_control_adoptions,
    standard_assessments,
)
from experiments.scoped_model_adoption.world import (
    AMBER_CASES,
    CASES,
    SELF_FULFILLING_CASE,
    VIOLET_CASES,
    cooperative_response,
    evaluate_action,
)


def make_adoption(
    identifier: str,
    *,
    model=None,
    scope: Scope = Scope.AMBER,
    use_mode: UseMode = UseMode.CONTROL,
    authority: int = 5,
    revocation_policy: RevocationPolicy = RevocationPolicy.LIVE_LINKED,
    adopted_order: int = 20,
) -> Adoption:
    chosen = model or model_x()
    return adopt(
        identifier,
        chosen,
        purpose="choose-required-action",
        use_mode=use_mode,
        scopes=frozenset({scope}),
        authority=authority,
        revocation_policy=revocation_policy,
        adopted_order=adopted_order,
        provenance=(f"assessment:{chosen.identifier}",),
    )


def require_activation(result: object) -> Activation:
    assert isinstance(result, Activation)
    return result


def require_policy(result: object) -> DerivedPolicy:
    assert isinstance(result, DerivedPolicy)
    return result


def derive_control(
    adoption: Adoption,
    *,
    model=None,
    revocations: tuple[Revocation, ...] = (),
    snapshot_duration: int | None = None,
) -> tuple[Activation, DerivedPolicy]:
    chosen = model or model_x()
    activation = require_activation(activate(adoption, activated_order=30))
    policy = require_policy(
        derive_artifact(
            activation,
            chosen,
            UseMode.CONTROL,
            derived_order=40,
            revocations=revocations,
            snapshot_duration=snapshot_duration,
        )
    )
    return activation, policy


def test_01_model_can_exist_without_being_adopted() -> None:
    model = model_x()

    assert model.identifier == "model-x"
    assert not hasattr(model, "authority")
    assert not hasattr(model, "activation_state")


def test_02_highly_assessed_model_can_remain_inactive() -> None:
    assessment = assess_model(model_x(), CASES, confidence=95)

    amber = next(item for item in assessment.scores if item.scope is Scope.AMBER)
    assert amber.accepted_count == 6
    assert assessment.confidence == 95
    assert not hasattr(assessment, "activation")


def test_03_adoption_declares_required_scope_and_authority_fields() -> None:
    adoption = make_adoption("adoption:x:amber")

    assert adoption.model_identifier == "model-x"
    assert adoption.purpose == "choose-required-action"
    assert adoption.scopes == frozenset({Scope.AMBER})
    assert adoption.authority == 5
    assert adoption.start_condition == "explicit activation"
    assert adoption.end_condition == "declared revocation or expiry"
    assert adoption.activation_state.value == "inactive"
    assert adoption.revocation_policy is RevocationPolicy.LIVE_LINKED
    assert adoption.provenance == ("assessment:model-x",)


def test_04_activation_is_separate_from_adoption() -> None:
    adoption = make_adoption("adoption:x:amber")

    activation = require_activation(activate(adoption, activated_order=30))

    assert activation.adoption is adoption
    assert activation.identifier != adoption.identifier
    assert activation.state.value == "active"
    assert adoption.activation_state.value == "inactive"


def test_05_predictive_and_control_uses_derive_distinct_artifacts() -> None:
    model = model_x()
    predictive_adoption = make_adoption(
        "adoption:x:predict",
        model=model,
        use_mode=UseMode.PREDICTIVE,
    )
    control_adoption = make_adoption(
        "adoption:x:control",
        model=model,
        use_mode=UseMode.CONTROL,
    )
    predictive_activation = require_activation(
        activate(predictive_adoption, activated_order=30)
    )
    control_activation = require_activation(
        activate(control_adoption, activated_order=30)
    )
    prediction_rule = derive_artifact(
        predictive_activation,
        model,
        UseMode.PREDICTIVE,
        derived_order=40,
    )
    action_policy = derive_artifact(
        control_activation,
        model,
        UseMode.CONTROL,
        derived_order=40,
    )

    assert isinstance(prediction_rule, PredictionRule)
    assert isinstance(action_policy, DerivedPolicy)
    prediction = predict_case(prediction_rule, AMBER_CASES[0], recorded_order=50)
    refused_action = act_on_case(prediction_rule, AMBER_CASES[0], produced_order=50)
    refused_prediction = predict_case(action_policy, AMBER_CASES[0], recorded_order=50)
    assert isinstance(prediction, Prediction)
    assert isinstance(refused_action, ArtifactUnavailable)
    assert isinstance(refused_prediction, ArtifactUnavailable)


def test_06_model_contains_neither_use_as_nominal_essence() -> None:
    model = model_x()

    assert not hasattr(model, "use_mode")
    assert not hasattr(model, "predictive")
    assert not hasattr(model, "control")


def test_07_disjoint_incompatible_adoptions_coexist_lawfully() -> None:
    x_adoption, y_adoption = scoped_control_adoptions()

    result = reconcile_adoptions((x_adoption, y_adoption))

    assert isinstance(result, CoexistingAdoptions)
    assert result.adoptions == frozenset({x_adoption, y_adoption})


def test_08_overlapping_equal_authority_adoptions_return_conflict() -> None:
    x_adoption = make_adoption("overlap-x")
    y_adoption = make_adoption("overlap-y", model=model_y())

    result = reconcile_adoptions((x_adoption, y_adoption))

    assert isinstance(result, AdoptionConflict)
    assert result.adoption_identifiers == frozenset({"overlap-x", "overlap-y"})
    assert result.conflicting_scopes == frozenset({Scope.AMBER})


def test_09_reversing_overlap_storage_preserves_conflict() -> None:
    x_adoption = make_adoption("overlap-x")
    y_adoption = make_adoption("overlap-y", model=model_y())

    forward = reconcile_adoptions((x_adoption, y_adoption))
    reversed_result = reconcile_adoptions((y_adoption, x_adoption))

    assert isinstance(forward, AdoptionConflict)
    assert forward == reversed_result


def test_10_declared_preferred_model_policy_resolves_overlap() -> None:
    x_adoption = make_adoption("overlap-x")
    y_adoption = make_adoption("overlap-y", model=model_y())
    policy = ResolutionPolicy(
        "prefer-y-for-trial",
        ResolutionKind.PREFERRED_MODEL,
        preferred_model_identifier="model-y",
    )

    result = reconcile_adoptions((x_adoption, y_adoption), policy)

    assert isinstance(result, ResolvedAdoption)
    assert result.adoption is y_adoption
    assert result.policy is policy


def test_11_scoped_adoption_does_not_leak_to_other_scope() -> None:
    adoption = make_adoption("adoption:x:amber")
    _, policy = derive_control(adoption)

    amber = act_on_case(policy, AMBER_CASES[0], produced_order=50)
    violet = act_on_case(policy, VIOLET_CASES[0], produced_order=51)

    assert isinstance(amber, ActionRecord)
    assert isinstance(violet, ArtifactUnavailable)
    assert "violet" in violet.reason


def test_12_local_models_are_not_globally_adequate() -> None:
    assessment_x, assessment_y = standard_assessments()

    assert tuple(item.accepted_count for item in assessment_x.scores) == (6, 2)
    assert tuple(item.accepted_count for item in assessment_y.scores) == (2, 6)
    assert assessment_x.global_accepted_count == 8
    assert assessment_y.global_accepted_count == 8
    assert assessment_x.global_accepted_count < assessment_x.global_total_count


def test_13_scoped_composite_outperforms_either_global_model() -> None:
    _, outcomes = execute_scoped_composite()

    assert len(outcomes) == 12
    assert sum(item.successful for item in outcomes) == 12
    assert sum(item.successful for item in outcomes) > 8


def test_14_scoped_success_does_not_assert_universal_truth() -> None:
    _, outcomes = execute_scoped_composite()

    assert all(item.successful for item in outcomes)
    assert all(not hasattr(item, "truth_assertion") for item in outcomes)
    assert reject_local_as_universal().countermodel == (
        "local-usefulness-is-universal-validity"
    )


def test_15_adoption_and_truth_assertion_are_separate_operations() -> None:
    model = model_x()
    adoption = make_adoption("adoption:x:amber", model=model)
    truth = assert_truth(model, "signal X describes the world", asserted_order=90)

    assert isinstance(truth, TruthAssertion)
    assert truth.model_identifier == adoption.model_identifier
    assert not hasattr(adoption, "claim")
    assert truth.identifier != adoption.identifier


def test_16_confidence_remains_separate_from_authority() -> None:
    assessment = assess_model(model_y(), CASES, confidence=12)
    adoption = make_adoption("experimental-y", model=model_y(), authority=9)

    assert assessment.confidence == 12
    assert adoption.authority == 9
    assert not hasattr(assessment, "authority")
    assert not hasattr(adoption, "confidence")


def test_17_weakly_assessed_model_can_be_adopted_for_controlled_trial() -> None:
    model = model_y()
    assessment = assess_model(model, CASES, confidence=5)
    adoption = make_adoption("experimental-y", model=model, authority=4)
    _, policy = derive_control(adoption, model=model)

    action = act_on_case(policy, AMBER_CASES[0], produced_order=50)

    assert assessment.confidence == 5
    assert isinstance(action, ActionRecord)
    assert not hasattr(adoption, "truth")


def test_18_epistemic_ambiguity_can_coexist_with_operational_commitment() -> None:
    assessment_x, assessment_y = standard_assessments()
    ambiguity = compare_assessments((assessment_x, assessment_y))
    trial_adoption = make_adoption("limited-trial-x", authority=3)

    commitment = commit_operationally(
        ambiguity,
        trial_adoption,
        selection_policy_identifier="limited-amber-trial",
    )

    assert isinstance(ambiguity, EpistemicAmbiguity)
    assert isinstance(commitment, OperationalCommitment)
    assert commitment.epistemic_state is ambiguity
    assert ambiguity.model_identifiers == frozenset({"model-x", "model-y"})


def test_19_same_successful_action_can_derive_from_different_models() -> None:
    x_adoption = make_adoption("action-x", model=model_x())
    y_adoption = make_adoption("action-y", model=model_y())
    _, x_policy = derive_control(x_adoption, model=model_x())
    _, y_policy = derive_control(y_adoption, model=model_y())

    x_action = act_on_case(x_policy, AMBER_CASES[0], produced_order=50)
    y_action = act_on_case(y_policy, AMBER_CASES[0], produced_order=50)

    assert isinstance(x_action, ActionRecord)
    assert isinstance(y_action, ActionRecord)
    assert x_action.action is y_action.action is Action.LEFT
    assert x_action.lineage.model_identifier != y_action.lineage.model_identifier


def test_20_successful_outcome_does_not_identify_explanation() -> None:
    x_adoption = make_adoption("outcome-x", model=model_x())
    y_adoption = make_adoption("outcome-y", model=model_y())
    _, x_policy = derive_control(x_adoption, model=model_x())
    _, y_policy = derive_control(y_adoption, model=model_y())
    x_action = act_on_case(x_policy, AMBER_CASES[0], produced_order=50)
    y_action = act_on_case(y_policy, AMBER_CASES[0], produced_order=50)
    assert isinstance(x_action, ActionRecord)
    assert isinstance(y_action, ActionRecord)

    x_outcome = evaluate_action(x_action, AMBER_CASES[0], order=60)
    y_outcome = evaluate_action(y_action, AMBER_CASES[0], order=60)

    assert x_outcome.successful and y_outcome.successful
    assert x_outcome.observed_result == y_outcome.observed_result
    assert (
        x_outcome.causal_record.model_identifier
        != y_outcome.causal_record.model_identifier
    )


def test_21_self_fulfilling_success_is_causally_marked() -> None:
    model = cooperation_model()
    adoption = make_adoption("cooperation-trial", model=model)
    _, policy = derive_control(adoption, model=model)
    action = act_on_case(policy, SELF_FULFILLING_CASE, produced_order=50)
    assert isinstance(action, ActionRecord)

    outcome = cooperative_response(action, order=60)
    observation = observe_outcome(outcome, available_order=70)

    assert outcome.successful
    assert observation.observed_result == "cooperative-response"
    assert outcome.causal_record.action_participated
    assert reject_self_fulfillment_as_validation().countermodel == (
        "self-fulfillment-is-validation"
    )


def test_22_live_linked_revocation_blocks_future_policy_use() -> None:
    adoption = make_adoption("live-x")
    _, policy = derive_control(adoption)
    revocation = revoke(adoption, reason="trial ended", revoked_order=60)
    assert isinstance(revocation, Revocation)

    before = act_on_case(policy, AMBER_CASES[0], produced_order=50)
    after = act_on_case(
        policy,
        AMBER_CASES[1],
        produced_order=70,
        revocations=(revocation,),
    )

    assert isinstance(before, ActionRecord)
    assert isinstance(after, ArtifactUnavailable)


def test_23_revocation_preserves_prior_adoption_and_action_history() -> None:
    adoption = make_adoption("live-x")
    _, policy = derive_control(adoption)
    action = act_on_case(policy, AMBER_CASES[0], produced_order=50)
    assert isinstance(action, ActionRecord)
    snapshot = (adoption, action)

    revocation = revoke(adoption, reason="trial ended", revoked_order=60)

    assert isinstance(revocation, Revocation)
    assert snapshot == (adoption, action)
    assert action.lineage.adoption_identifier == adoption.identifier


def test_24_live_linked_and_snapshot_revocation_remain_distinct() -> None:
    live = make_adoption("live-x", revocation_policy=RevocationPolicy.LIVE_LINKED)
    snapshot = make_adoption(
        "snapshot-x",
        revocation_policy=RevocationPolicy.SNAPSHOT,
    )
    _, live_policy = derive_control(live)
    _, snapshot_policy = derive_control(snapshot, snapshot_duration=100)
    live_revocation = revoke(live, reason="source revoked", revoked_order=60)
    snapshot_revocation = revoke(snapshot, reason="source revoked", revoked_order=60)
    assert isinstance(live_revocation, Revocation)
    assert isinstance(snapshot_revocation, Revocation)

    live_result = act_on_case(
        live_policy,
        AMBER_CASES[0],
        produced_order=70,
        revocations=(live_revocation,),
    )
    snapshot_result = act_on_case(
        snapshot_policy,
        AMBER_CASES[0],
        produced_order=70,
        revocations=(snapshot_revocation,),
    )

    assert isinstance(live_result, ArtifactUnavailable)
    assert isinstance(snapshot_result, ActionRecord)


def test_25_unspecified_revocation_semantics_are_not_guessed() -> None:
    adoption = make_adoption(
        "unspecified-x",
        revocation_policy=RevocationPolicy.UNSPECIFIED,
    )
    activation = require_activation(activate(adoption, activated_order=30))

    derived = derive_artifact(
        activation,
        model_x(),
        UseMode.CONTROL,
        derived_order=40,
    )
    revoked = revoke(adoption, reason="unknown behavior", revoked_order=60)

    assert isinstance(derived, UnspecifiedRevocationPolicy)
    assert isinstance(revoked, UnspecifiedRevocationPolicy)


def test_26_model_switch_creates_prospective_record() -> None:
    previous = make_adoption("switch-x")
    next_adoption = make_adoption("switch-y", model=model_y(), adopted_order=70)

    switch = record_switch(
        previous,
        next_adoption,
        reason="new evidence favors local trial",
        switched_order=80,
    )

    assert switch.previous_adoption_identifier == previous.identifier
    assert switch.next_adoption_identifier == next_adoption.identifier
    assert switch.switched_order == 80


def test_27_switching_does_not_rewrite_earlier_actions() -> None:
    previous = make_adoption("switch-x")
    _, policy = derive_control(previous)
    earlier = act_on_case(policy, AMBER_CASES[0], produced_order=50)
    assert isinstance(earlier, ActionRecord)
    next_adoption = make_adoption("switch-y", model=model_y(), adopted_order=70)

    record_switch(previous, next_adoption, reason="switch", switched_order=80)

    assert earlier.lineage.adoption_identifier == previous.identifier
    assert earlier.lineage.model_identifier == "model-x"
    assert earlier.produced_order == 50


def test_28_equal_local_actions_preserve_different_model_lineage() -> None:
    x_adoption = make_adoption("lineage-x", model=model_x())
    y_adoption = make_adoption("lineage-y", model=model_y())
    _, x_policy = derive_control(x_adoption, model=model_x())
    _, y_policy = derive_control(y_adoption, model=model_y())
    x_action = act_on_case(x_policy, AMBER_CASES[1], produced_order=50)
    y_action = act_on_case(y_policy, AMBER_CASES[1], produced_order=50)

    assert isinstance(x_action, ActionRecord)
    assert isinstance(y_action, ActionRecord)
    assert x_action.action == y_action.action
    assert x_action.lineage != y_action.lineage


def test_29_post_hoc_scope_selection_is_explicit() -> None:
    _, outcomes = execute_scoped_composite()

    result = select_scope_post_hoc(model_x(), Scope.AMBER, outcomes)

    assert result.selected_scope is Scope.AMBER
    assert result.selected_after_outcome_identifiers == tuple(
        item.identifier for item in outcomes
    )
    assert not result.precommitted
    assert reject_post_hoc_scope().countermodel == "post-hoc-scope"


def test_30_neutral_mechanics_define_no_foundation_named_classes() -> None:
    experiment_root = Path(records_module.__file__).parent
    forbidden = {"Form", "Will", "Ars", "Spell", "Cast", "Effect", "Demonstration"}
    defined: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        defined.update(
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

    assert defined.isdisjoint(forbidden)


def test_31_foundation_mapping_follows_neutral_probe() -> None:
    report = attempt_mapping()
    adoption = next(item for item in report.mappings if item.neutral_term == "Adoption")
    truth = next(
        item
        for item in report.mappings
        if item.neutral_term == "Scoped adoption as truth"
    )

    assert adoption.status is MappingStatus.PRESSURE
    assert truth.status is MappingStatus.REJECTED
    assert not report.finding.scoped_use_is_truth
    assert report.finding.contextual_roles_recur
    assert report.finding.snapshot_independence_recurs
    assert report.finding.adoption_is_cast is None


def test_32_package_source_remains_untouched() -> None:
    repository_root = Path(records_module.__file__).parents[2]
    result = subprocess.run(
        ["git", "status", "--short", "--", "src/arx_mentis"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert not result.stdout.strip()


def test_33_declared_higher_authority_policy_resolves_overlap() -> None:
    lower = make_adoption("lower", authority=3)
    higher = make_adoption("higher", model=model_y(), authority=8)
    policy = ResolutionPolicy("higher-wins", ResolutionKind.HIGHER_AUTHORITY)

    result = reconcile_adoptions((lower, higher), policy)

    assert isinstance(result, ResolvedAdoption)
    assert result.adoption is higher


def test_34_no_new_artifact_derives_after_revocation() -> None:
    adoption = make_adoption("revoked-x")
    activation = require_activation(activate(adoption, activated_order=30))
    revocation = revoke(adoption, reason="ended", revoked_order=60)
    assert isinstance(revocation, Revocation)

    result = derive_artifact(
        activation,
        model_x(),
        UseMode.CONTROL,
        derived_order=70,
        revocations=(revocation,),
    )

    assert isinstance(result, ArtifactUnavailable)


def test_35_snapshot_artifact_expires_at_declared_boundary() -> None:
    adoption = make_adoption(
        "snapshot-x",
        revocation_policy=RevocationPolicy.SNAPSHOT,
    )
    _, policy = derive_control(adoption, snapshot_duration=20)

    at_expiry = act_on_case(policy, AMBER_CASES[0], produced_order=60)
    after_expiry = act_on_case(policy, AMBER_CASES[0], produced_order=61)

    assert isinstance(at_expiry, ActionRecord)
    assert isinstance(after_expiry, ArtifactUnavailable)


def test_36_unsupported_or_mismatched_use_is_owned() -> None:
    adoption = make_adoption("control-x", use_mode=UseMode.CONTROL)
    activation = require_activation(activate(adoption, activated_order=30))

    predictive = derive_artifact(
        activation,
        model_x(),
        UseMode.PREDICTIVE,
        derived_order=40,
    )
    audit = derive_artifact(
        activation,
        model_x(),
        UseMode.AUDIT,
        derived_order=40,
    )

    assert isinstance(predictive, UnsupportedUse)
    assert isinstance(audit, UnsupportedUse)


def test_37_all_hostile_countermodels_are_owned() -> None:
    rejections = (
        reject_model_as_adoption(),
        reject_assessment_as_authority(),
        reject_adoption_as_truth(),
        reject_global_current_model(),
        reject_local_as_universal(),
        reject_post_hoc_scope(),
        reject_silent_switching(),
        reject_first_adoption_wins(),
        reject_success_proves_model(),
        reject_revocation_erases_history(),
        reject_implicit_revocation_policy(),
        reject_confidence_as_commitment(),
        reject_commitment_as_confidence(),
        reject_self_fulfillment_as_validation(),
        reject_same_policy_as_same_origin(),
    )

    assert all(isinstance(item, CountermodelRejection) for item in rejections)
    assert len({item.countermodel for item in rejections}) == 15


def test_38_experiment_imports_no_package_or_previous_experiment() -> None:
    experiment_root = Path(records_module.__file__).parent
    forbidden_prefixes = (
        "arx_mentis",
        "experiments.euclid_i_1",
        "experiments.ars_astronomica_settlement",
        "experiments.ars_grammatica_reading",
        "experiments.ars_dialectica_verification",
        "experiments.virtual_mediation",
        "experiments.omen_attribution",
        "experiments.actualization",
        "experiments.symbolic_release",
        "experiments.stress_discharge",
        "experiments.probability_bias",
        "experiments.feedback_revision",
    )
    imported: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)

    assert not any(
        name.startswith(prefix) for name in imported for prefix in forbidden_prefixes
    )


def test_39_adoption_and_action_history_are_immutable() -> None:
    adoption = make_adoption("immutable-x")
    _, policy = derive_control(adoption)
    action = act_on_case(policy, AMBER_CASES[0], produced_order=50)
    assert isinstance(action, ActionRecord)

    with pytest.raises(FrozenInstanceError):
        adoption.authority = 9  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        action.action = Action.RIGHT  # type: ignore[misc]


def test_40_revoked_adoption_cannot_be_reactivated() -> None:
    adoption = make_adoption("reactivation-x")
    revocation = revoke(adoption, reason="ended", revoked_order=60)
    assert isinstance(revocation, Revocation)

    result = activate(
        adoption,
        activated_order=70,
        revocations=(revocation,),
    )

    assert isinstance(result, InvalidActivation)


def test_41_models_are_incompatible_outside_their_strong_scopes() -> None:
    x_disagreements = sum(
        model_action(model_x(), case) is not model_action(model_y(), case)
        for case in AMBER_CASES
    )
    y_disagreements = sum(
        model_action(model_x(), case) is not model_action(model_y(), case)
        for case in VIOLET_CASES
    )

    assert x_disagreements == 4
    assert y_disagreements == 4


def test_42_observation_does_not_create_truth_assertion() -> None:
    adoption = make_adoption("observe-x")
    _, policy = derive_control(adoption)
    action = act_on_case(policy, AMBER_CASES[0], produced_order=50)
    assert isinstance(action, ActionRecord)
    outcome = evaluate_action(action, AMBER_CASES[0], order=60)

    observation = observe_outcome(outcome, available_order=70)

    assert observation.successful
    assert not isinstance(observation, TruthAssertion)
