from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import experiments.probability_bias.outcomes as outcomes_module
from experiments.probability_bias.comparison import (
    assess_sample,
    compare_distributions,
    compare_kernels,
    compare_trial,
    distribution,
)
from experiments.probability_bias.countermodels import (
    command,
    reject_command_as_bias,
    reject_hidden_mixture_as_one_cause,
    reject_hidden_optional_stopping,
    reject_match_as_bias,
    reject_order_based_resolution,
    reject_post_hoc_intention,
    reject_probability_as_potential,
    reject_report_as_stream,
    reject_sample_as_kernel,
    reject_seed_only_causation,
    report_option_bag_loss,
)
from experiments.probability_bias.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.probability_bias.interventions import (
    apply_intervention,
    bias_intervention,
    compose_interventions,
)
from experiments.probability_bias.kernels import (
    OUTCOME_ORDER,
    baseline_kernel,
    build_kernel,
    kernel_mass,
    outcome_for_seed,
    support,
)
from experiments.probability_bias.observation import (
    attribute_from_observation,
    hide_context,
    observe,
    select_post_hoc_target,
)
from experiments.probability_bias.outcomes import (
    CountermodelRejection,
    EventStream,
    InterventionConflict,
    InvalidPlan,
    InvalidSeed,
    InvalidWeights,
    Kernel,
    KernelTransformation,
    MechanismKind,
    ObservationWindow,
    Outcome,
    ReportKind,
    SampleCriterion,
    StoppingKind,
    UnchangedKernel,
    Weight,
)
from experiments.probability_bias.reporting import make_report
from experiments.probability_bias.scenarios import (
    baseline_plan,
    biased_plan,
    mixture_scenario,
    optional_stopping_plan,
    public_baseline,
    public_bias,
    selective_plan,
)
from experiments.probability_bias.trials import (
    execute_mixture,
    execute_plan,
    make_plan,
)


def require_kernel(result: object) -> Kernel:
    assert isinstance(result, Kernel)
    return result


def require_stream(result: object) -> EventStream:
    assert isinstance(result, EventStream)
    return result


def baseline_stream(*, window: ObservationWindow | None = None) -> EventStream:
    kernel, context = public_baseline()
    return require_stream(
        execute_plan(
            baseline_plan(window=window),
            kernel,
            context,
            mechanism=MechanismKind.BASELINE,
        )
    )


def biased_stream() -> EventStream:
    transformation, context = public_bias()
    return require_stream(
        execute_plan(
            biased_plan(),
            transformation.after,
            context,
            mechanism=MechanismKind.INTERVENED,
        )
    )


def hidden_mixture_stream() -> EventStream:
    plan, contexts, schedule = mixture_scenario()
    return require_stream(execute_mixture(plan, contexts, schedule))


def test_01_baseline_weights_are_exact_and_normalized() -> None:
    kernel = baseline_kernel()

    assert kernel.denominator == 60
    assert tuple(item.mass for item in kernel.weights) == (10, 10, 10, 10, 10, 10)
    assert sum(item.mass for item in kernel.weights) == 60
    assert support(kernel) == frozenset(Outcome)


def test_02_declared_bias_changes_weights_without_removing_outcomes() -> None:
    transformation, _ = public_bias()

    assert kernel_mass(transformation.before, Outcome.A) == 10
    assert kernel_mass(transformation.after, Outcome.A) == 20
    assert tuple(item.mass for item in transformation.after.weights) == (
        20,
        8,
        8,
        8,
        8,
        8,
    )
    assert support(transformation.before) == support(transformation.after)


def test_03_support_and_weight_are_independently_observable() -> None:
    transformation, _ = public_bias()

    comparison = compare_kernels(transformation.before, transformation.after)

    assert comparison.same_support
    assert len(comparison.weight_changes) == 6
    assert all(change.before != change.after for change in comparison.weight_changes)


def test_04_direct_command_is_not_bias() -> None:
    baseline = baseline_kernel()
    direct = command(Outcome.A)
    rejection = reject_command_as_bias(Outcome.A)

    assert support(baseline) == frozenset(Outcome)
    assert direct.installed_support == frozenset({Outcome.A})
    assert direct.causal_record.mechanism is MechanismKind.DIRECT_COMMAND
    assert rejection.countermodel == "target-coded-command"


def test_05_target_can_fail_to_occur_on_a_biased_trial() -> None:
    transformation, _ = public_bias()

    result = outcome_for_seed(transformation.after, 20)

    assert result is Outcome.B
    assert result is not transformation.intervention.target


def test_06_non_target_outcomes_remain_possible_under_bias() -> None:
    transformation, _ = public_bias()

    assert support(transformation.after) == frozenset(Outcome)
    assert all(
        kernel_mass(transformation.after, outcome) > 0
        for outcome in Outcome
        if outcome is not Outcome.A
    )


def test_07_same_seed_under_different_kernels_may_change_outcome() -> None:
    baseline = baseline_kernel()
    transformation, _ = public_bias()

    assert outcome_for_seed(baseline, 15) is Outcome.B
    assert outcome_for_seed(transformation.after, 15) is Outcome.A


def test_08_same_kernel_and_seed_are_reproducible() -> None:
    kernel = baseline_kernel()

    assert outcome_for_seed(kernel, 47) is outcome_for_seed(kernel, 47)
    assert baseline_stream() == baseline_stream()


def test_09_finite_sample_remains_distinct_from_kernel() -> None:
    stream = baseline_stream(window=ObservationWindow(0, 3))

    sample = observe(stream)

    assert sample.source_stream is stream
    assert len(sample.trials) == 3
    assert all(trial.outcome is Outcome.A for trial in sample.trials)
    assert stream.causal_record.kernel_identifiers == (baseline_kernel().identifier,)


def test_10_short_window_variation_does_not_rewrite_baseline() -> None:
    kernel, context = public_baseline()
    snapshot = baseline_kernel()
    plan = baseline_plan(window=ObservationWindow(0, 3))
    stream = require_stream(
        execute_plan(plan, kernel, context, mechanism=MechanismKind.BASELINE)
    )

    sample = observe(stream)

    assert [trial.outcome for trial in sample.trials] == [Outcome.A] * 3
    assert kernel == snapshot
    assert tuple(item.mass for item in kernel.weights) == (10,) * 6


def test_11_selective_reporting_changes_report_not_stream() -> None:
    kernel, context = public_baseline()
    plan = selective_plan()
    stream = require_stream(
        execute_plan(plan, kernel, context, mechanism=MechanismKind.BASELINE)
    )

    report = make_report(stream)

    assert report.source_stream is stream
    assert len(stream.trials) == 60
    assert len(report.trials) == 10
    assert all(trial.outcome is Outcome.A for trial in report.trials)


def test_12_post_hoc_target_selection_is_explicit() -> None:
    stream = biased_stream()

    result = select_post_hoc_target(stream)

    assert result.selected is Outcome.A
    assert result.selected_after_order == stream.trials[-1].order
    assert not result.precommitted
    assert reject_post_hoc_intention().countermodel == "post-hoc-target"


def test_13_optional_stopping_is_precommitted_in_trial_plan() -> None:
    kernel, context = public_baseline()
    plan = optional_stopping_plan()

    stream = require_stream(
        execute_plan(plan, kernel, context, mechanism=MechanismKind.BASELINE)
    )

    assert plan.stopping_rule.kind is StoppingKind.FAVORABLE_RUN
    assert plan.stopping_rule.favorable_run_length == 2
    assert len(stream.trials) == 2
    assert all(trial.outcome is Outcome.A for trial in stream.trials)


def test_14_hidden_context_mixture_imitates_fixed_biased_distribution() -> None:
    fixed = biased_stream()
    mixture = hidden_mixture_stream()

    comparison = compare_distributions(fixed, mixture)

    assert comparison.same_public_distribution
    assert tuple(item.count for item in comparison.left.frequencies) == (
        20,
        8,
        8,
        8,
        8,
        8,
    )


def test_15_equal_public_distribution_retains_different_causal_records() -> None:
    fixed = biased_stream()
    mixture = hidden_mixture_stream()

    assert distribution(fixed) == distribution(mixture)
    assert fixed.causal_record.mechanism is MechanismKind.INTERVENED
    assert mixture.causal_record.mechanism is MechanismKind.CONTEXT_MIXTURE
    assert fixed.causal_record != mixture.causal_record


def test_16_relevant_intervention_changes_the_kernel() -> None:
    baseline, context = public_baseline()
    intervention = bias_intervention(Outcome.A)

    result = apply_intervention(baseline, intervention, context)

    assert isinstance(result, KernelTransformation)
    assert result.before is baseline
    assert result.after is not baseline
    assert result.changes


def test_17_irrelevant_intervention_preserves_the_same_kernel() -> None:
    baseline, context = public_baseline()
    intervention = bias_intervention(
        Outcome.A,
        identifier="other-context-bias",
        context_identifier="other-context",
    )

    result = apply_intervention(baseline, intervention, context)

    assert isinstance(result, UnchangedKernel)
    assert result.kernel is baseline


def test_18_invalid_weights_are_owned_and_rejected() -> None:
    result = build_kernel(
        "invalid-total",
        tuple(
            Weight(outcome, 9 if outcome is Outcome.F else 10)
            for outcome in OUTCOME_ORDER
        ),
    )

    assert isinstance(result, InvalidWeights)
    assert "normalize" in result.reason


def test_19_equal_priority_incompatible_interventions_remain_ambiguous() -> None:
    baseline, context = public_baseline()
    a = bias_intervention(Outcome.A, identifier="favor-a", priority=5)
    b = bias_intervention(Outcome.B, identifier="favor-b", priority=5)

    result = compose_interventions(baseline, (a, b), context)

    assert isinstance(result, InterventionConflict)
    assert result.priority == 5
    assert result.intervention_identifiers == frozenset({"favor-a", "favor-b"})


def test_20_reversing_intervention_storage_preserves_the_conflict() -> None:
    baseline, context = public_baseline()
    a = bias_intervention(Outcome.A, identifier="favor-a", priority=5)
    b = bias_intervention(Outcome.B, identifier="favor-b", priority=5)

    forward = compose_interventions(baseline, (a, b), context)
    reversed_result = compose_interventions(baseline, (b, a), context)

    assert isinstance(forward, InterventionConflict)
    assert isinstance(reversed_result, InterventionConflict)
    assert forward == reversed_result


def test_equivalent_equal_priority_interventions_do_not_create_an_implicit_policy() -> (
    None
):
    baseline, context = public_baseline()
    first = bias_intervention(Outcome.A, identifier="first-a", priority=5)
    second = bias_intervention(Outcome.A, identifier="second-a", priority=5)

    forward = compose_interventions(baseline, (first, second), context)
    reversed_result = compose_interventions(baseline, (second, first), context)

    assert isinstance(forward, InterventionConflict)
    assert forward == reversed_result
    assert forward.intervention_identifiers == frozenset({"first-a", "second-a"})


def test_21_plain_option_bag_loses_weighted_behavior() -> None:
    transformation, _ = public_bias()

    result = report_option_bag_loss(transformation.before, transformation.after)

    assert result.baseline_bag == result.biased_bag
    assert result.kernels_differ
    assert result.behavior_lost


def test_22_outcome_correspondence_does_not_prove_causal_bias() -> None:
    stream = baseline_stream()
    matching = stream.trials[0]

    correspondence = compare_trial(matching, Outcome.A)
    rejection = reject_match_as_bias()

    assert correspondence.matches
    assert stream.causal_record.mechanism is MechanismKind.BASELINE
    assert rejection.countermodel == "match-implies-bias"


def test_23_sample_acceptance_does_not_identify_production_mechanism() -> None:
    fixed = observe(biased_stream())
    mixture = observe(hidden_mixture_stream())
    criterion = SampleCriterion(Outcome.A, minimum_count=20)

    fixed_acceptance = assess_sample(fixed, criterion)
    mixture_acceptance = assess_sample(mixture, criterion)

    assert fixed_acceptance.accepted
    assert mixture_acceptance.accepted
    assert (
        fixed.source_stream.causal_record.mechanism
        is not mixture.source_stream.causal_record.mechanism
    )


def test_24_probability_is_not_automatically_potential() -> None:
    transformation, _ = public_bias()

    boundary = reject_probability_as_potential(transformation.after)

    assert boundary.weighted
    assert boundary.unequal_mass
    assert not boundary.transitive_frame_declared
    assert not boundary.settlement_operation_declared


def test_25_observer_attribution_is_separate_from_world_causal_record() -> None:
    stream = hidden_mixture_stream()
    observed = hide_context(observe(stream))

    attribution = attribute_from_observation(observed)

    assert stream.causal_record.mechanism is MechanismKind.CONTEXT_MIXTURE
    assert all(not trial.context_available for trial in observed.trials)
    assert attribution.selected is None
    assert not attribution.world_record_available
    assert MechanismKind.CONTEXT_MIXTURE in attribution.candidate_mechanisms


def test_26_neutral_layer_defines_no_foundation_named_classes() -> None:
    experiment_root = Path(outcomes_module.__file__).parent
    forbidden = {"Form", "Will", "Spell", "Reader", "Cast", "Effect", "Potential"}
    defined: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        defined.update(
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

    assert defined.isdisjoint(forbidden)


def test_27_post_hoc_foundation_mapping_may_reject_or_remain_unmapped() -> None:
    report = attempt_mapping()
    kernel = next(item for item in report.mappings if item.neutral_term == "Kernel")
    weighted = next(
        item for item in report.mappings if item.neutral_term == "weighted Kernel"
    )

    assert kernel.status is MappingStatus.UNMAPPED
    assert weighted.status is MappingStatus.REJECTED
    assert not report.finding.bias_is_command
    assert not report.finding.probability_is_potential


def test_28_package_source_remains_untouched() -> None:
    repository_root = Path(outcomes_module.__file__).parents[2]
    result = subprocess.run(
        ["git", "status", "--short", "--", "src/arx_mentis"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert not result.stdout.strip()


def test_29_precommitment_is_complete_and_precedes_every_trial() -> None:
    plan = biased_plan()
    stream = biased_stream()

    assert plan.outcome_space.outcomes == frozenset(Outcome)
    assert plan.target is Outcome.A
    assert plan.kernel_identifier
    assert plan.intervention_identifiers
    assert plan.trial_count == 60
    assert plan.seeds == tuple(range(60))
    assert plan.context_identifiers == ("public",)
    assert plan.observation_window == ObservationWindow(0, 60)
    assert plan.report_policy.kind is ReportKind.ALL
    assert plan.stopping_rule.kind is StoppingKind.FIXED
    assert plan.comparison_rule.expected_kernel == plan.kernel_identifier
    assert all(plan.recorded_order < trial.order for trial in stream.trials)


def test_30_acceptance_is_not_implicit_in_target_or_sample() -> None:
    stream = biased_stream()
    sample = observe(stream)

    assert stream.plan.target is Outcome.A
    assert not hasattr(sample, "accepted")
    accepted = assess_sample(sample, SampleCriterion(Outcome.A, 20))
    rejected = assess_sample(sample, SampleCriterion(Outcome.A, 21))
    assert accepted.accepted
    assert not rejected.accepted


def test_31_seed_only_causation_is_rejected() -> None:
    result = reject_seed_only_causation()

    assert isinstance(result, CountermodelRejection)
    assert result.countermodel == "seed-only-causation"
    assert "kernel" in result.reason


def test_32_hidden_mixture_cannot_replace_the_world_causal_record() -> None:
    stream = hidden_mixture_stream()

    rejection = reject_hidden_mixture_as_one_cause(stream)

    assert stream.causal_record.context_identifiers == ("context-x", "context-y")
    assert rejection.countermodel == "hidden-mixture-as-one-kernel"


def test_33_report_is_not_the_event_stream() -> None:
    kernel, context = public_baseline()
    plan = selective_plan()
    stream = require_stream(
        execute_plan(plan, kernel, context, mechanism=MechanismKind.BASELINE)
    )
    report = make_report(stream)

    rejection = reject_report_as_stream(report)

    assert rejection.countermodel == "report-is-stream"
    assert len(report.trials) < len(stream.trials)


def test_34_sample_is_not_its_kernel() -> None:
    sample = observe(baseline_stream(window=ObservationWindow(0, 3)))

    rejection = reject_sample_as_kernel(sample)

    assert rejection.countermodel == "sample-is-kernel"
    assert "3 observed trials" in rejection.reason


def test_35_hidden_optional_stopping_is_rejected() -> None:
    rejection = reject_hidden_optional_stopping()

    assert rejection.countermodel == "hidden-optional-stopping"
    assert "TrialPlan" in rejection.reason


def test_36_order_based_intervention_resolution_is_rejected() -> None:
    rejection = reject_order_based_resolution()

    assert rejection.countermodel == "order-based-intervention-resolution"
    assert "not a declared" in rejection.reason


def test_37_invalid_seed_is_an_owned_result() -> None:
    result = outcome_for_seed(baseline_kernel(), 60)

    assert isinstance(result, InvalidSeed)
    assert result.seed == 60


def test_38_plan_kernel_mismatch_is_an_owned_result() -> None:
    kernel, context = public_baseline()
    plan = make_plan("wrong-kernel-plan", "another-kernel", target=None)

    result = execute_plan(plan, kernel, context, mechanism=MechanismKind.BASELINE)

    assert isinstance(result, InvalidPlan)
    assert "identifiers differ" in result.reason


def test_39_experiment_imports_no_package_or_other_experiment() -> None:
    experiment_root = Path(outcomes_module.__file__).parent
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


def test_40_kernel_construction_canonicalizes_weight_storage_order() -> None:
    supplied = tuple(reversed(tuple(Weight(outcome, 10) for outcome in Outcome)))

    result = require_kernel(build_kernel("reversed-baseline", supplied))

    assert tuple(item.outcome for item in result.weights) == OUTCOME_ORDER
    assert tuple(item.mass for item in result.weights) == (10,) * 6
