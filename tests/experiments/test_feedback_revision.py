from __future__ import annotations

import ast
import subprocess
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import experiments.feedback_revision.records as records_module
from experiments.feedback_revision.assessment import (
    admit_evidence,
    apply_correction,
    assess,
    exact_rule,
    outcome_defined_rule,
    reassess_from_evidence,
    report_assessment,
)
from experiments.feedback_revision.cases import (
    CALIBRATION_CASES,
    CALIBRATION_IDS,
    CASES,
    HOLDOUT_CASES,
    HOLDOUT_IDS,
    SEALED_HOLDOUT,
    case_inputs,
)
from experiments.feedback_revision.countermodels import (
    reject_contradiction_erasure,
    reject_current_version_identity,
    reject_evidence_leakage,
    reject_failure_deletion,
    reject_model_as_truth,
    reject_one_event_validation,
    reject_outcome_defined_success,
    reject_overfit_as_improvement,
    reject_prediction_rewriting,
    reject_replay_as_history,
    reject_revision_order_tie_breaking,
    reject_self_fulfillment,
)
from experiments.feedback_revision.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.feedback_revision.models import (
    initial_model_a,
    initial_model_b,
    initial_version,
    predict,
)
from experiments.feedback_revision.observations import (
    attribute_observation,
    correct_observation,
    record_erroneous_observation,
)
from experiments.feedback_revision.records import (
    Assessment,
    AssessmentKind,
    CountermodelRejection,
    EvidenceLeakage,
    EvidenceSet,
    Intervention,
    InvalidPlan,
    MechanismKind,
    ModelVersion,
    NoRevision,
    Observation,
    Outcome,
    ReportKind,
    Revision,
    RevisionConflict,
    RevisionKind,
    SelectedRevision,
    SelectionKind,
    SelectionPolicy,
    Split,
)
from experiments.feedback_revision.replay import replay
from experiments.feedback_revision.revision import (
    decline_revision,
    revise,
    revision_rule,
    scored_revision,
    select_revision,
)
from experiments.feedback_revision.scenarios import (
    assess_bundle,
    calibration_evidence,
    run_cases,
)
from experiments.feedback_revision.trials import (
    commit_predictions,
    derive_intervention,
    make_plan,
    produce_outcomes,
)


def version_zero() -> ModelVersion:
    return initial_version(initial_model_a(), "V0")


def require_revision(result: object) -> Revision:
    assert isinstance(result, Revision)
    return result


def require_assessment(result: object) -> Assessment:
    assert isinstance(result, Assessment)
    return result


def require_evidence(result: object) -> EvidenceSet:
    assert isinstance(result, EvidenceSet)
    return result


def make_revision(kind: RevisionKind, identifier: str) -> Revision:
    source = version_zero()
    _, _, evidence = calibration_evidence(source)
    return require_revision(revise(source, evidence, revision_rule(identifier, kind)))


def assessments_for(
    version: ModelVersion, prefix: str
) -> tuple[Assessment, Assessment]:
    calibration = assess_bundle(
        f"assessment:{prefix}:calibration",
        run_cases(
            f"{prefix}:calibration",
            version,
            CALIBRATION_CASES,
            Split.CALIBRATION,
        ),
    )
    holdout = assess_bundle(
        f"assessment:{prefix}:holdout",
        run_cases(
            f"{prefix}:holdout",
            version,
            HOLDOUT_CASES,
            Split.HOLDOUT,
        ),
    )
    return calibration, holdout


def test_01_predictions_are_committed_before_outcomes_are_exposed() -> None:
    bundle = run_cases(
        "commit-order",
        version_zero(),
        CALIBRATION_CASES,
        Split.CALIBRATION,
    )

    assert not bundle.plan.outcomes_exposed_at_commit
    assert max(item.committed_order for item in bundle.predictions) < min(
        item.occurred_order for item in bundle.occurrences
    )


def test_02_outcomes_do_not_mutate_committed_predictions() -> None:
    version = version_zero()
    inputs = case_inputs(CALIBRATION_CASES)
    plan = make_plan("plan:immutable", version, inputs, Split.CALIBRATION)
    predictions = commit_predictions(plan, version, inputs)
    assert not isinstance(predictions, InvalidPlan)
    snapshot = tuple(predictions)

    occurrences = produce_outcomes(plan, predictions, CALIBRATION_CASES)

    assert not isinstance(occurrences, InvalidPlan)
    assert predictions == snapshot
    assert predictions[1].outcome is Outcome.NEGATIVE
    assert occurrences[1].outcome is Outcome.POSITIVE


def test_03_observation_assessment_and_revision_are_separate_records() -> None:
    source = version_zero()
    bundle, assessment, evidence = calibration_evidence(source)
    result = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")

    assert isinstance(bundle.observations[0], Observation)
    assert isinstance(assessment, Assessment)
    assert isinstance(result, Revision)
    assert bundle.observations[0].identifier != assessment.identifier
    assert assessment.identifier != result.identifier
    assert evidence.source_assessment_identifier == assessment.identifier


def test_04_revision_produces_a_new_persistent_model_version() -> None:
    source = version_zero()
    _, _, evidence = calibration_evidence(source)

    result = require_revision(
        revise(
            source,
            evidence,
            revision_rule("generalize", RevisionKind.GENERALIZE_XOR),
        )
    )

    assert result.source_version is source
    assert result.result_version is not source
    assert result.result_version.ordinal == source.ordinal + 1
    assert source.ordinal == 0
    assert source.lineage is None


def test_05_old_model_remains_replayable_after_revision() -> None:
    source = version_zero()
    bundle, _, evidence = calibration_evidence(source)
    require_revision(
        revise(
            source, evidence, revision_rule("generalize", RevisionKind.GENERALIZE_XOR)
        )
    )

    result = replay(
        "replay:V0",
        source,
        case_inputs(CALIBRATION_CASES),
        bundle.history,
    )

    assert result.model_version is source
    assert tuple(item.would_predict for item in result.predictions) == tuple(
        item.prediction.outcome for item in bundle.history
    )


def test_06_historical_prediction_is_distinct_from_later_replay() -> None:
    source = version_zero()
    bundle, _, evidence = calibration_evidence(source)
    revision = require_revision(
        revise(
            source, evidence, revision_rule("generalize", RevisionKind.GENERALIZE_XOR)
        )
    )

    later = replay(
        "replay:V1",
        revision.result_version,
        case_inputs(CALIBRATION_CASES),
        bundle.history,
    )

    assert bundle.history[1].prediction.outcome is Outcome.NEGATIVE
    assert later.predictions[1].would_predict is Outcome.POSITIVE
    assert (
        later.historical_prediction_identifiers[1]
        == bundle.history[1].prediction.identifier
    )


def test_07_revision_lineage_names_source_evidence_rule_and_result() -> None:
    source = version_zero()
    _, _, evidence = calibration_evidence(source)
    rule = revision_rule("generalize", RevisionKind.GENERALIZE_XOR)

    result = require_revision(revise(source, evidence, rule))
    lineage = result.result_version.lineage

    assert lineage is not None
    assert lineage.source_version_identifier == source.identifier
    assert lineage.evidence_set_identifier == evidence.identifier
    assert lineage.revision_rule_identifier == rule.identifier
    assert result.result_version.identifier == f"{source.identifier}->{rule.identifier}"
    assert result.created_order == lineage.created_order


def test_08_no_revision_after_failure_is_an_explicit_result() -> None:
    source = version_zero()
    _, assessment, _ = calibration_evidence(source)

    result = decline_revision(source, assessment)

    assert isinstance(result, NoRevision)
    assert result.source_version is source
    assert not result.evidence_evaluated
    assert assessment.accepted_count == 3


def test_09_calibration_and_holdout_remain_separate() -> None:
    source = version_zero()
    _, _, evidence = calibration_evidence(source)

    assert CALIBRATION_IDS.isdisjoint(HOLDOUT_IDS)
    assert {entry.case_identifier for entry in evidence.entries} == CALIBRATION_IDS
    assert SEALED_HOLDOUT.case_identifiers == HOLDOUT_IDS
    assert SEALED_HOLDOUT.sealed


def test_10_overfit_revision_improves_calibration_and_worsens_holdout() -> None:
    source = version_zero()
    initial_calibration, initial_holdout = assessments_for(source, "V0")
    overfit = make_revision(RevisionKind.OVERFIT_MEMORIZE, "memorize")
    fit_calibration, fit_holdout = assessments_for(overfit.result_version, "overfit")

    assert (initial_calibration.accepted_count, initial_holdout.accepted_count) == (
        3,
        4,
    )
    assert (fit_calibration.accepted_count, fit_holdout.accepted_count) == (6, 2)


def test_11_generalizing_revision_improves_calibration_and_holdout() -> None:
    source = version_zero()
    initial_calibration, initial_holdout = assessments_for(source, "V0")
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    new_calibration, new_holdout = assessments_for(general.result_version, "general")

    assert new_calibration.accepted_count > initial_calibration.accepted_count
    assert new_holdout.accepted_count > initial_holdout.accepted_count
    assert (new_calibration.accepted_count, new_holdout.accepted_count) == (6, 6)


def test_12_perfect_calibration_fit_does_not_establish_general_validity() -> None:
    overfit = make_revision(RevisionKind.OVERFIT_MEMORIZE, "memorize")
    calibration, holdout = assessments_for(overfit.result_version, "overfit")

    rejection = reject_overfit_as_improvement()

    assert calibration.accepted_count == calibration.total_count
    assert holdout.accepted_count == 2
    assert rejection.countermodel == "overfit-equals-improvement"


def test_13_structurally_different_revisions_can_have_equal_scores() -> None:
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    lookup = make_revision(RevisionKind.EQUIVALENT_LOOKUP, "lookup")
    general_scores = assessments_for(general.result_version, "general")
    lookup_scores = assessments_for(lookup.result_version, "lookup")

    assert general.result_version.model != lookup.result_version.model
    assert tuple(item.accepted_count for item in general_scores) == (6, 6)
    assert tuple(item.accepted_count for item in lookup_scores) == (6, 6)


def test_14_equal_scores_preserve_order_independent_revision_conflict() -> None:
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    lookup = make_revision(RevisionKind.EQUIVALENT_LOOKUP, "lookup")
    general_assessments = assessments_for(general.result_version, "general")
    lookup_assessments = assessments_for(lookup.result_version, "lookup")
    candidates = (
        scored_revision(general, *general_assessments),
        scored_revision(lookup, *lookup_assessments),
    )

    forward = select_revision(candidates)
    reversed_result = select_revision(tuple(reversed(candidates)))

    assert isinstance(forward, RevisionConflict)
    assert forward == reversed_result
    assert forward.candidate_revision_identifiers == frozenset(
        {general.identifier, lookup.identifier}
    )


def test_15_declared_secondary_policy_may_select_an_equal_score_model() -> None:
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    lookup = make_revision(RevisionKind.EQUIVALENT_LOOKUP, "lookup")
    candidates = (
        scored_revision(general, *assessments_for(general.result_version, "general")),
        scored_revision(lookup, *assessments_for(lookup.result_version, "lookup")),
    )
    policy = SelectionPolicy("prefer-lower-complexity", SelectionKind.LOWER_COMPLEXITY)

    result = select_revision(candidates, policy)

    assert isinstance(result, SelectedRevision)
    assert result.candidate.revision == general
    assert result.policy is policy


def test_16_failure_filter_changes_report_not_historical_trials() -> None:
    bundle, assessment, _ = calibration_evidence(version_zero())
    snapshot = bundle.history

    report = report_assessment(assessment, ReportKind.SUCCESSES_ONLY)

    assert len(report.included_case_identifiers) == 3
    assert report.source_assessment is assessment
    assert bundle.history == snapshot
    assert len(bundle.history) == 6


def test_17_changing_assessment_rule_creates_a_new_assessment() -> None:
    bundle, original, _ = calibration_evidence(version_zero())
    later_rule = outcome_defined_rule(declared_order=350)

    later = require_assessment(
        assess(
            "assessment:redefined-success",
            bundle.predictions,
            bundle.observations,
            later_rule,
            created_order=360,
        )
    )

    assert original.rule.kind is AssessmentKind.EXACT
    assert original.accepted_count == 3
    assert later.rule.kind is AssessmentKind.ALWAYS_SUCCESS
    assert later.accepted_count == 6
    assert later is not original


def test_18_invalidated_evidence_adds_correction_and_new_assessment() -> None:
    source = version_zero()
    bundle = run_cases("correction", source, CALIBRATION_CASES, Split.CALIBRATION)
    erroneous = record_erroneous_observation(
        bundle.occurrences[1],
        Outcome.NEGATIVE,
        available_order=250,
    )
    original = require_assessment(
        assess(
            "assessment:erroneous", (bundle.predictions[1],), (erroneous,), exact_rule()
        )
    )
    evidence = require_evidence(
        admit_evidence(
            "evidence:erroneous",
            original,
            (erroneous,),
            admitted_case_identifiers=frozenset({"C01"}),
        )
    )
    correction = correct_observation(
        erroneous,
        Outcome.POSITIVE,
        reason="measurement record invalidated",
        recorded_order=450,
    )
    corrected = require_evidence(
        apply_correction(
            evidence,
            correction,
            identifier="evidence:corrected",
            admitted_order=460,
        )
    )
    reassessment = require_assessment(
        reassess_from_evidence(
            "assessment:corrected",
            bundle.predictions,
            corrected,
            exact_rule(),
            created_order=470,
        )
    )
    revised = require_revision(
        revise(
            source,
            corrected,
            revision_rule("corrected-generalize", RevisionKind.GENERALIZE_XOR),
            created_order=500,
        )
    )

    assert original.accepted_count == 1
    assert evidence.entries[0].effective_outcome is Outcome.NEGATIVE
    assert corrected.previous_evidence_set_identifier == evidence.identifier
    assert corrected.entries[0].source_record_identifiers == (
        erroneous.identifier,
        correction.identifier,
    )
    assert reassessment.accepted_count == 0
    assert revised.result_version.lineage is not None
    assert (
        revised.result_version.lineage.evidence_set_identifier == corrected.identifier
    )


def test_19_equal_current_model_behavior_can_retain_distinct_lineage() -> None:
    first = make_revision(RevisionKind.GENERALIZE_XOR, "generalize-first")
    second = make_revision(RevisionKind.GENERALIZE_XOR, "generalize-second")

    assert first.result_version.model == second.result_version.model
    assert first.result_version.identifier != second.result_version.identifier
    assert first.result_version.lineage != second.result_version.lineage


def test_20_revised_model_can_change_future_intervention_and_outcomes() -> None:
    overfit = make_revision(RevisionKind.OVERFIT_MEMORIZE, "memorize")
    passive = run_cases(
        "passive-overfit",
        overfit.result_version,
        HOLDOUT_CASES,
        Split.HOLDOUT,
    )
    intervention = derive_intervention(overfit.result_version)
    adaptive = run_cases(
        "adaptive-overfit",
        overfit.result_version,
        HOLDOUT_CASES,
        Split.ADAPTIVE,
        intervention=intervention,
    )

    assert isinstance(intervention, Intervention)
    assert tuple(item.outcome for item in passive.occurrences) != tuple(
        item.outcome for item in adaptive.occurrences
    )
    assert all(
        item.causal_record.mechanism is MechanismKind.ADAPTIVE_INTERVENTION
        for item in adaptive.occurrences
    )


def test_21_self_fulfilled_accuracy_is_not_passive_improvement() -> None:
    overfit = make_revision(RevisionKind.OVERFIT_MEMORIZE, "memorize")
    passive = run_cases(
        "passive-overfit",
        overfit.result_version,
        HOLDOUT_CASES,
        Split.HOLDOUT,
    )
    intervention = derive_intervention(overfit.result_version)
    adaptive = run_cases(
        "adaptive-overfit",
        overfit.result_version,
        HOLDOUT_CASES,
        Split.ADAPTIVE,
        intervention=intervention,
    )

    assert assess_bundle("assessment:passive", passive).accepted_count == 2
    assert assess_bundle("assessment:adaptive", adaptive).accepted_count == 6
    assert (
        reject_self_fulfillment().countermodel == "self-fulfillment-equals-prediction"
    )


def test_22_one_outcome_remains_compatible_with_multiple_models() -> None:
    source_a = version_zero()
    source_b = initial_version(initial_model_b(), "V0-B")
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    bundle = run_cases("attribution", source_a, (CASES[0],), Split.CALIBRATION)

    attribution = attribute_observation(
        bundle.observations[0],
        case_inputs((CASES[0],))[0],
        (source_a, source_b, general.result_version),
    )

    assert attribution.candidate_model_version_identifiers == frozenset(
        {source_a.identifier, source_b.identifier, general.result_version.identifier}
    )
    assert attribution.selected_model_version_identifier is None


def test_23_contradictory_correction_weakens_without_unique_replacement() -> None:
    source = version_zero()
    source_b = initial_version(initial_model_b(), "V0-B")
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    bundle = run_cases("contradiction", source, (CASES[1],), Split.CALIBRATION)
    erroneous = record_erroneous_observation(
        bundle.occurrences[0],
        Outcome.NEGATIVE,
        available_order=250,
    )
    initial = require_assessment(
        assess(
            "assessment:contradiction:old",
            bundle.predictions,
            (erroneous,),
            exact_rule(),
        )
    )
    evidence = require_evidence(
        admit_evidence(
            "evidence:contradiction:old",
            initial,
            (erroneous,),
            admitted_case_identifiers=frozenset({"C01"}),
        )
    )
    correction = correct_observation(
        erroneous,
        Outcome.POSITIVE,
        reason="contrary record admitted",
        recorded_order=450,
    )
    corrected = require_evidence(
        apply_correction(
            evidence,
            correction,
            identifier="evidence:contradiction:new",
            admitted_order=460,
        )
    )
    reassessment = require_assessment(
        reassess_from_evidence(
            "assessment:contradiction:new",
            bundle.predictions,
            corrected,
            exact_rule(),
            created_order=470,
        )
    )
    case = case_inputs((CASES[1],))[0]
    compatible_replacements = frozenset(
        version.identifier
        for version in (source_b, general.result_version)
        if predict(version.model, case) is correction.corrected_outcome
    )

    assert initial.accepted_count == 1
    assert reassessment.accepted_count == 0
    assert compatible_replacements == frozenset(
        {source_b.identifier, general.result_version.identifier}
    )


def test_24_observer_confidence_remains_separate_from_world_cause() -> None:
    source = version_zero()
    source_b = initial_version(initial_model_b(), "V0-B")
    bundle = run_cases("confidence", source, (CASES[0],), Split.CALIBRATION)
    confidence = ((source.identifier, 9), (source_b.identifier, 4))

    attribution = attribute_observation(
        bundle.observations[0],
        case_inputs((CASES[0],))[0],
        (source, source_b),
        confidence=confidence,
    )

    assert attribution.confidence == confidence
    assert not attribution.world_cause_available
    assert bundle.occurrences[0].causal_record.mechanism is MechanismKind.PASSIVE


def test_25_selected_working_model_is_not_declared_world_truth() -> None:
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    lookup = make_revision(RevisionKind.EQUIVALENT_LOOKUP, "lookup")
    candidates = (
        scored_revision(general, *assessments_for(general.result_version, "general")),
        scored_revision(lookup, *assessments_for(lookup.result_version, "lookup")),
    )
    result = select_revision(
        candidates,
        SelectionPolicy("prefer-lower-complexity", SelectionKind.LOWER_COMPLEXITY),
    )

    assert isinstance(result, SelectedRevision)
    assert not hasattr(result, "world_truth")
    assert reject_model_as_truth().countermodel == "model-is-truth"


def test_26_neutral_mechanics_define_no_foundation_named_classes() -> None:
    experiment_root = Path(records_module.__file__).parent
    forbidden = {"Form", "Will", "Ars", "Spell", "Cast", "Effect", "Demonstration"}
    defined: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        defined.update(
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

    assert defined.isdisjoint(forbidden)


def test_27_foundation_mapping_occurs_only_after_neutral_mechanics() -> None:
    report = attempt_mapping()
    model = next(item for item in report.mappings if item.neutral_term == "Model")
    truth = next(
        item for item in report.mappings if item.neutral_term == "Model as world truth"
    )

    assert model.status is MappingStatus.UNMAPPED
    assert truth.status is MappingStatus.REJECTED
    assert report.finding.prospective_not_retroactive
    assert report.finding.revision_is_cast is None


def test_28_package_source_remains_untouched() -> None:
    repository_root = Path(records_module.__file__).parents[2]
    result = subprocess.run(
        ["git", "status", "--short", "--", "src/arx_mentis"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert not result.stdout.strip()


def test_29_holdout_evidence_leakage_is_an_owned_result() -> None:
    source = version_zero()
    bundle = run_cases("holdout", source, HOLDOUT_CASES, Split.HOLDOUT)
    assessment = assess_bundle("assessment:holdout", bundle)
    evidence = require_evidence(
        admit_evidence(
            "evidence:holdout",
            assessment,
            bundle.observations,
            admitted_case_identifiers=HOLDOUT_IDS,
        )
    )

    result = revise(
        source,
        evidence,
        revision_rule("leaky-generalize", RevisionKind.GENERALIZE_XOR),
    )

    assert isinstance(result, EvidenceLeakage)
    assert result.forbidden_case_identifiers == HOLDOUT_IDS


def test_30_no_op_revision_is_explicit_and_preserves_source() -> None:
    source = version_zero()
    _, _, evidence = calibration_evidence(source)

    result = revise(
        source,
        evidence,
        revision_rule("inspect-only", RevisionKind.NO_OP),
    )

    assert isinstance(result, NoRevision)
    assert result.source_version is source
    assert result.evidence_evaluated
    assert result.evidence_set_identifier == evidence.identifier


def test_31_failed_assessment_does_not_dictate_one_revision() -> None:
    source = version_zero()
    _, assessment, evidence = calibration_evidence(source)
    results = tuple(
        revise(source, evidence, revision_rule(identifier, kind))
        for identifier, kind in (
            ("generalize", RevisionKind.GENERALIZE_XOR),
            ("lookup", RevisionKind.EQUIVALENT_LOOKUP),
            ("memorize", RevisionKind.OVERFIT_MEMORIZE),
        )
    )

    assert assessment.accepted_count == 3
    assert all(isinstance(item, Revision) for item in results)
    assert (
        len(
            {
                item.result_version.model.kind
                for item in results
                if isinstance(item, Revision)
            }
        )
        == 3
    )


def test_32_predictions_and_versions_are_frozen() -> None:
    source = version_zero()
    bundle, _, _ = calibration_evidence(source)

    with pytest.raises(FrozenInstanceError):
        bundle.predictions[1].outcome = Outcome.POSITIVE  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        source.ordinal = 1  # type: ignore[misc]


def test_33_plan_claiming_prior_outcome_exposure_is_refused() -> None:
    source = version_zero()
    inputs = case_inputs(CALIBRATION_CASES)
    ordinary = make_plan("plan:invalid-exposure", source, inputs, Split.CALIBRATION)
    invalid = ordinary.__class__(
        ordinary.identifier,
        ordinary.model_version_identifier,
        ordinary.case_identifiers,
        ordinary.split,
        ordinary.assessment_rule_identifier,
        ordinary.intervention_identifier,
        ordinary.committed_order,
        outcomes_exposed_at_commit=True,
    )

    result = commit_predictions(invalid, source, inputs)

    assert isinstance(result, InvalidPlan)
    assert "before outcomes" in result.reason


def test_34_all_hostile_countermodels_are_owned() -> None:
    rejections = (
        reject_prediction_rewriting(),
        reject_failure_deletion(),
        reject_outcome_defined_success(),
        reject_evidence_leakage(),
        reject_one_event_validation(),
        reject_overfit_as_improvement(),
        reject_current_version_identity(),
        reject_replay_as_history(),
        reject_self_fulfillment(),
        reject_revision_order_tie_breaking(),
        reject_contradiction_erasure(),
        reject_model_as_truth(),
    )

    assert all(isinstance(item, CountermodelRejection) for item in rejections)
    assert len({item.countermodel for item in rejections}) == 12


def test_35_experiment_imports_no_package_or_previous_experiment() -> None:
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


def test_36_revision_uses_only_admitted_evidence_values() -> None:
    source = version_zero()
    _, _, evidence = calibration_evidence(source)
    overfit = require_revision(
        revise(
            source,
            evidence,
            revision_rule("memorize", RevisionKind.OVERFIT_MEMORIZE),
        )
    )

    assert dict(overfit.result_version.model.parameters) == {
        entry.case_identifier: entry.effective_outcome for entry in evidence.entries
    }
    assert not HOLDOUT_IDS & dict(overfit.result_version.model.parameters).keys()


def test_37_original_trial_record_survives_replay_and_reporting() -> None:
    source = version_zero()
    bundle, assessment, evidence = calibration_evidence(source)
    original = bundle.history
    general = require_revision(
        revise(
            source, evidence, revision_rule("generalize", RevisionKind.GENERALIZE_XOR)
        )
    )

    report_assessment(assessment, ReportKind.SUCCESSES_ONLY)
    replay(
        "replay:general",
        general.result_version,
        case_inputs(CALIBRATION_CASES),
        bundle.history,
    )

    assert bundle.history == original


def test_38_declared_primary_score_selects_a_unique_better_revision() -> None:
    general = make_revision(RevisionKind.GENERALIZE_XOR, "generalize")
    overfit = make_revision(RevisionKind.OVERFIT_MEMORIZE, "memorize")
    candidates = (
        scored_revision(overfit, *assessments_for(overfit.result_version, "overfit")),
        scored_revision(general, *assessments_for(general.result_version, "general")),
    )

    result = select_revision(candidates)

    assert isinstance(result, SelectedRevision)
    assert result.candidate.revision == general
    assert result.policy.kind is SelectionKind.HIGHER_HOLDOUT_SCORE


def test_39_model_b_is_independent_of_model_a() -> None:
    model_a = initial_model_a()
    model_b = initial_model_b()
    inputs = case_inputs(CALIBRATION_CASES)

    assert model_a.kind != model_b.kind
    assert [predict(model_a, case) for case in inputs] != [
        predict(model_b, case) for case in inputs
    ]


def test_40_exact_world_has_six_calibration_and_six_holdout_cases() -> None:
    assert tuple(case.identifier for case in CASES) == tuple(
        f"C{index:02d}" for index in range(12)
    )
    assert len(CALIBRATION_CASES) == 6
    assert len(HOLDOUT_CASES) == 6
    assert tuple(case.outcome for case in CASES) == (
        Outcome.NEGATIVE,
        Outcome.POSITIVE,
        Outcome.POSITIVE,
        Outcome.NEGATIVE,
        Outcome.NEGATIVE,
        Outcome.NEGATIVE,
        Outcome.NEGATIVE,
        Outcome.POSITIVE,
        Outcome.NEGATIVE,
        Outcome.POSITIVE,
        Outcome.POSITIVE,
        Outcome.NEGATIVE,
    )
