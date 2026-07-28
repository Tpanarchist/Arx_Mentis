from __future__ import annotations

import ast
import subprocess
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import experiments.actualization.source_model as source_model_module
from experiments.actualization.acceptance import derive_acceptance, evaluate
from experiments.actualization.attribution import attribute_from_state
from experiments.actualization.control import (
    compile_controller,
    derive_hidden_weighting,
    derive_policy,
    reject_direct_assignment,
    run_controller,
    run_criterion_only,
    run_hidden_bias,
)
from experiments.actualization.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.actualization.scenarios import (
    fully_blocked,
    partially_blocked_safe_path,
    safe_target,
    shortest_target,
    strict_target,
)
from experiments.actualization.source_model import (
    AcceptanceRule,
    Mechanism,
    Outcome,
    Position,
    RejectedMechanism,
    Unreachable,
    WorldState,
)
from experiments.actualization.world import initial_world


def require_outcome(result: Outcome | Unreachable) -> Outcome:
    assert isinstance(result, Outcome)
    return result


def path(result: Outcome | Unreachable) -> tuple[str, ...]:
    return tuple(step.transition.identifier for step in result.trace.steps)


def test_01_target_exists_before_execution() -> None:
    target = shortest_target()
    result = require_outcome(
        run_controller(initial_world(), compile_controller(target, sustained=True))
    )

    assert result.trace.steps
    assert target.recorded_order < result.trace.steps[0].index


def test_02_target_cannot_directly_mutate_the_world() -> None:
    source = initial_world()
    target = shortest_target()

    rejected = reject_direct_assignment(source, target)

    assert isinstance(rejected, RejectedMechanism)
    assert rejected.source is source
    assert source == WorldState(Position.A, resources=2)
    with pytest.raises(FrozenInstanceError):
        target.minimum_resources = 0  # type: ignore[misc]


def test_03_criterion_only_target_does_not_alter_choices() -> None:
    source = initial_world()

    shortest = require_outcome(run_criterion_only(source, shortest_target()))
    safe = require_outcome(run_criterion_only(source, safe_target()))

    assert path(shortest) == path(safe) == ("short-a-b", "unsafe-b-d")
    assert shortest.trace.target_identifier is None
    assert safe.trace.target_identifier is None


def test_04_policy_guidance_has_an_inspectable_trace() -> None:
    target = safe_target()
    controller = compile_controller(target, sustained=True)

    result = require_outcome(run_controller(initial_world(), controller))

    assert path(result) == ("safe-a-c", "safe-c-e", "safe-e-d")
    assert result.trace.mechanism is Mechanism.POLICY_GUIDANCE
    assert result.trace.policy_identifier == controller.policy.identifier
    assert result.trace.target_identifier == target.identifier


def test_05_hidden_bias_is_explicit_and_distinct() -> None:
    target = shortest_target()
    weighting = derive_hidden_weighting(target)

    result = require_outcome(run_hidden_bias(initial_world(), weighting))

    assert weighting.weights
    assert weighting.derived_from == target.identifier
    assert result.trace.mechanism is Mechanism.HIDDEN_BIAS
    assert result.trace.weighting_identifier == weighting.identifier
    assert result.trace.policy_identifier is None


def test_06_direct_assignment_is_rejected_as_circular() -> None:
    source = initial_world()

    result = reject_direct_assignment(source, shortest_target())

    assert result.mechanism is Mechanism.DIRECT_ASSIGNMENT
    assert result.proposed_state.position is Position.D
    assert "no transition or causal account" in result.reason


def test_07_three_mechanisms_can_reach_the_same_outcome() -> None:
    source = initial_world()
    target = shortest_target()
    criterion = require_outcome(run_criterion_only(source, target))
    guided = require_outcome(
        run_controller(source, compile_controller(target, sustained=True))
    )
    hidden = require_outcome(run_hidden_bias(source, derive_hidden_weighting(target)))

    assert criterion.state == guided.state == hidden.state


def test_08_equal_outcomes_retain_distinct_causal_traces() -> None:
    source = initial_world()
    target = shortest_target()
    results = (
        require_outcome(run_criterion_only(source, target)),
        require_outcome(
            run_controller(source, compile_controller(target, sustained=True))
        ),
        require_outcome(run_hidden_bias(source, derive_hidden_weighting(target))),
    )

    assert len({result.trace.mechanism for result in results}) == 3
    assert len({result.trace for result in results}) == 3


def test_09_conformity_does_not_prove_a_mechanism() -> None:
    target = shortest_target()
    result = require_outcome(run_criterion_only(initial_world(), target))

    acceptance = evaluate(derive_acceptance(target), result.state)
    attribution = attribute_from_state(result.state)

    assert acceptance.conforms
    assert attribution.selected is None
    assert len(attribution.candidates) == 3


def test_10_one_target_can_guide_and_evaluate_through_separate_records() -> None:
    target = safe_target()

    policy = derive_policy(target)
    rule = derive_acceptance(target)
    outcome = require_outcome(
        run_controller(initial_world(), compile_controller(target, sustained=True))
    )

    assert policy.derived_from == target.identifier
    assert isinstance(rule, AcceptanceRule)
    assert evaluate(rule, outcome.state).conforms
    assert policy is not rule


def test_11_partial_progress_can_disagree_with_strict_acceptance() -> None:
    target = safe_target()

    result = run_controller(
        initial_world(),
        compile_controller(target, sustained=True),
        partially_blocked_safe_path(),
    )

    assert isinstance(result, Unreachable)
    assert path(result) == ("safe-a-c", "safe-c-e")
    assert result.state.position is Position.E
    assert not evaluate(derive_acceptance(target), result.state).conforms


def test_12_released_policy_continues_without_target_availability() -> None:
    target = safe_target()
    controller = compile_controller(target, sustained=False)

    result = require_outcome(run_controller(initial_world(), controller))

    assert controller.live_target is None
    assert path(result) == ("safe-a-c", "safe-c-e", "safe-e-d")
    assert not result.trace.target_available_during_run
    assert result.trace.target_identifier == target.identifier
    assert not result.trace.feedback


def test_13_removing_the_causal_channel_restores_the_baseline_path() -> None:
    source = initial_world()
    target = safe_target()

    no_channel = require_outcome(run_criterion_only(source, target))
    guided = require_outcome(
        run_controller(source, compile_controller(target, sustained=True))
    )

    assert path(no_channel) == ("short-a-b", "unsafe-b-d")
    assert path(guided) == ("safe-a-c", "safe-c-e", "safe-e-d")


def test_14_constraints_can_make_the_target_unreachable() -> None:
    result = run_controller(
        initial_world(),
        compile_controller(shortest_target(), sustained=True),
        fully_blocked(),
    )

    assert isinstance(result, Unreachable)
    assert not result.trace.steps
    assert result.state == initial_world()


def test_15_unreachable_run_does_not_hide_mutation_or_report_success() -> None:
    source = initial_world()
    target = shortest_target()

    result = run_controller(
        source,
        compile_controller(target, sustained=True),
        fully_blocked(),
    )

    assert isinstance(result, Unreachable)
    assert result.state is source
    assert source.position is Position.A
    assert not evaluate(derive_acceptance(target), result.state).conforms


def test_16_partial_progress_is_not_conformity() -> None:
    target = safe_target()
    result = run_controller(
        initial_world(),
        compile_controller(target, sustained=True),
        partially_blocked_safe_path(),
    )

    assert isinstance(result, Unreachable)
    assert len(result.trace.steps) == 2
    assert result.state.resources > initial_world().resources
    assert not evaluate(derive_acceptance(target), result.state).conforms


def test_17_execution_preserves_the_target_record() -> None:
    target = safe_target()
    snapshot = safe_target()

    run_controller(initial_world(), compile_controller(target, sustained=True))

    assert target == snapshot


def test_18_production_creates_a_separately_owned_world() -> None:
    source = initial_world()

    outcome = require_outcome(run_criterion_only(source, shortest_target()))

    assert outcome.state is not source
    assert source == initial_world()
    assert outcome.state.position is Position.D


def test_19_observer_attribution_is_distinct_from_actual_trace() -> None:
    target = shortest_target()
    actual = require_outcome(
        run_hidden_bias(initial_world(), derive_hidden_weighting(target))
    )

    observer = attribute_from_state(actual.state)

    assert actual.trace.mechanism is Mechanism.HIDDEN_BIAS
    assert observer.selected is None
    assert observer.observed_state is actual.state


def test_20_experiment_imports_no_foundation_package_or_other_experiment() -> None:
    experiment_root = Path(source_model_module.__file__).parent
    forbidden_prefixes = (
        "arx_mentis",
        "experiments.euclid_i_1",
        "experiments.ars_astronomica_settlement",
        "experiments.ars_grammatica_reading",
        "experiments.ars_dialectica_verification",
        "experiments.virtual_mediation",
        "experiments.omen_attribution",
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


def test_21_same_acceptance_can_have_different_guidance() -> None:
    shortest = shortest_target()
    safe = safe_target()

    assert derive_acceptance(shortest) == derive_acceptance(safe)
    assert (
        derive_policy(shortest).transition_order != derive_policy(safe).transition_order
    )


def test_22_same_guidance_can_have_different_acceptance_thresholds() -> None:
    ordinary = shortest_target()
    strict = strict_target()
    state = require_outcome(run_criterion_only(initial_world(), ordinary)).state

    assert (
        derive_policy(ordinary).transition_order
        == derive_policy(strict).transition_order
    )
    assert evaluate(derive_acceptance(ordinary), state).conforms
    assert not evaluate(derive_acceptance(strict), state).conforms


def test_23_sustained_and_released_control_have_distinct_feedback() -> None:
    target = safe_target()
    sustained = require_outcome(
        run_controller(initial_world(), compile_controller(target, sustained=True))
    )
    released = require_outcome(
        run_controller(initial_world(), compile_controller(target, sustained=False))
    )

    assert sustained.trace.target_available_during_run
    assert sustained.trace.feedback
    assert all(item.target_consulted for item in sustained.trace.feedback)
    assert all(item.target_consulted for item in sustained.trace.steps)
    assert not released.trace.feedback
    assert all(not item.target_consulted for item in released.trace.steps)


def test_24_neutral_layer_defines_no_foundation_named_classes() -> None:
    experiment_root = Path(source_model_module.__file__).parent
    forbidden = {"Form", "Will", "Spell", "Cast", "Effect", "Potential", "Witness"}
    defined: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        defined.update(
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

    assert defined.isdisjoint(forbidden)


def test_25_foundation_mapping_keeps_will_identity_open() -> None:
    report = attempt_mapping()

    acceptance = next(
        item for item in report.mappings if item.neutral_term == "AcceptanceRule"
    )
    target = next(item for item in report.mappings if item.neutral_term == "TargetForm")
    assert acceptance.status is MappingStatus.CANDIDATE
    assert target.status is MappingStatus.PRESSURE
    assert report.finding.acceptance_and_guidance_distinct
    assert report.finding.one_target_can_derive_both
    assert not report.finding.conformity_identifies_mechanism


def test_26_package_source_remains_untouched() -> None:
    repository_root = Path(source_model_module.__file__).parents[2]
    result = subprocess.run(
        ["git", "status", "--short", "--", "src/arx_mentis"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert not result.stdout.strip()
