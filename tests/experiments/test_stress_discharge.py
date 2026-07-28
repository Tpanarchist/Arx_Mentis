from __future__ import annotations

import ast
import inspect
import subprocess
from pathlib import Path

import experiments.stress_discharge.source_model as source_model_module
from experiments.stress_discharge.assessment import (
    assess_acceptance,
    assess_progress,
    assess_resolution,
)
from experiments.stress_discharge.countermodels import (
    collapse_to_scalar,
    reject_capacity_as_symmetric_potential,
    reject_history_erasure,
    reject_stress_as_progress,
    reject_target_coded_discharge,
    reject_trigger_only_causation,
    report_blocked_alternative,
    report_scalar_loss,
)
from experiments.stress_discharge.discharge import discharge, oscillate
from experiments.stress_discharge.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.stress_discharge.loading import (
    empty_state,
    field_from,
    load_at,
    load_suddenly,
    total_stress,
)
from experiments.stress_discharge.network import capacity_profile, default_network
from experiments.stress_discharge.scenarios import (
    B_TRIGGER,
    BLOCK_BOTH,
    BLOCK_NORTH,
    C_RELEASE_ONLY,
    C_TRIGGER,
    DELIVERY_ACCEPTANCE,
    DELIVERY_PROGRESS,
    FORCE_DISSIPATION,
    OPEN,
    SAFE_RESOLUTION,
    SOURCE_ONLY,
    SOURCE_TRIGGER,
    dissipation_load,
    gradual_source_load,
    north_obstructed_distribution,
    oscillation_law,
    oscillation_load,
    south_obstructed_distribution,
    sudden_source_load,
)
from experiments.stress_discharge.source_model import (
    AmbiguousDischarge,
    ConstrainedNetwork,
    ConstraintSet,
    CountermodelRejection,
    Discharge,
    DormantTrigger,
    IncompleteCausalAccount,
    Link,
    LinkKind,
    LoadingMode,
    NoDischargePath,
    Site,
    TransferKind,
)


def require_discharge(result: object) -> Discharge:
    assert isinstance(result, Discharge)
    return result


def first_path(result: Discharge) -> str:
    return result.trace.steps[0].link.identifier


def test_01_stress_is_a_distributed_field_not_a_scalar() -> None:
    field = field_from(a=3, b=2, c=1)

    assert len(field.loads) == 3
    assert load_at(field, Site.A) == 3
    assert collapse_to_scalar(field).total == 6
    assert field != field_from(a=6)


def test_02_equal_scalar_totals_can_discharge_through_different_paths() -> None:
    network = default_network()
    north = require_discharge(
        discharge(
            north_obstructed_distribution(),
            network,
            SOURCE_ONLY,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )
    south = require_discharge(
        discharge(
            south_obstructed_distribution(),
            network,
            SOURCE_ONLY,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    assert total_stress(north.before.field) == total_stress(south.before.field) == 10
    assert first_path(north) == "a-c"
    assert first_path(south) == "a-b"


def test_03_gradual_and_sudden_loading_reach_equal_fields_with_distinct_history() -> (
    None
):
    gradual = gradual_source_load()
    sudden = sudden_source_load()

    assert gradual.field == sudden.field
    assert len(gradual.history.events) == 3
    assert len(sudden.history.events) == 1
    assert {event.mode for event in gradual.history.events} == {LoadingMode.GRADUAL}
    assert sudden.history.events[0].mode is LoadingMode.SUDDEN


def test_04_trigger_without_load_remains_dormant() -> None:
    result = discharge(
        empty_state(),
        default_network(),
        OPEN,
        SOURCE_TRIGGER,
    )

    assert isinstance(result, DormantTrigger)
    assert result.observed_load == 0
    assert result.required_load == SOURCE_TRIGGER.threshold


def test_05_trigger_is_only_one_antecedent_in_the_causal_trace() -> None:
    result = require_discharge(
        discharge(
            gradual_source_load(),
            default_network(),
            OPEN,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    assert result.trace.trigger is SOURCE_TRIGGER
    assert result.trace.network_identifier == default_network().identifier
    assert result.trace.constraint_identifier == OPEN.identifier
    assert result.trace.initial_field == result.before.field
    assert result.trace.loading_history == result.before.history


def test_06_discharge_does_not_imply_resolution() -> None:
    partial = require_discharge(
        discharge(
            gradual_source_load(),
            default_network(),
            OPEN,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    resolution = assess_resolution(partial.after, SAFE_RESOLUTION)

    assert partial.trace.steps
    assert not resolution.resolved
    assert partial is not resolution


def test_07_resolution_does_not_imply_acceptance() -> None:
    result = require_discharge(
        discharge(
            dissipation_load(),
            default_network(),
            FORCE_DISSIPATION,
            C_TRIGGER,
        )
    )

    resolution = assess_resolution(result.after, SAFE_RESOLUTION)
    acceptance = assess_acceptance(result.after, DELIVERY_ACCEPTANCE)

    assert resolution.resolved
    assert not acceptance.accepted


def test_08_stress_reduction_does_not_imply_progress() -> None:
    before = dissipation_load()
    result = require_discharge(
        discharge(
            before,
            default_network(),
            FORCE_DISSIPATION,
            C_TRIGGER,
        )
    )

    progress = assess_progress(result.after, DELIVERY_PROGRESS)
    rejection = reject_stress_as_progress()

    assert total_stress(result.after.field) < total_stress(before.field)
    assert result.after.delivered == before.delivered == 0
    assert not progress.progressed
    assert rejection.countermodel == "stress-equals-progress"


def test_09_displacement_preserves_total_load_without_release() -> None:
    before = gradual_source_load()
    result = require_discharge(
        discharge(
            before,
            default_network(),
            OPEN,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    step = result.trace.steps[0]
    assert step.kind is TransferKind.DISPLACEMENT
    assert total_stress(result.after.field) == total_stress(before.field)
    assert result.after.delivered == 0
    assert result.after.dissipated == 0


def test_10_partial_release_leaves_residual_stress() -> None:
    state = load_suddenly(empty_state(), Site.C, 5)
    result = require_discharge(
        discharge(
            state,
            default_network(),
            C_RELEASE_ONLY,
            C_TRIGGER,
            maximum_steps=1,
        )
    )

    assert result.trace.steps[0].kind is TransferKind.RELEASE
    assert result.after.delivered == 3
    assert load_at(result.after.field, Site.C) == 2
    assert not assess_resolution(result.after, SAFE_RESOLUTION).resolved


def test_11_sudden_overload_can_rupture_a_declared_link() -> None:
    result = require_discharge(
        discharge(
            sudden_source_load(9),
            default_network(),
            OPEN,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    step = result.trace.steps[0]
    assert step.kind is TransferKind.RUPTURE
    assert step.link.identifier == "a-c"
    assert "a-c" in result.after.ruptured_links
    assert "a-c" in result.residue.ruptured_links


def test_12_dissipation_is_explicit_and_separate_from_delivery() -> None:
    result = require_discharge(
        discharge(
            dissipation_load(),
            default_network(),
            FORCE_DISSIPATION,
            C_TRIGGER,
        )
    )

    assert all(step.kind is TransferKind.DISSIPATION for step in result.trace.steps)
    assert result.after.dissipated == 4
    assert result.after.delivered == 0
    assert result.residue.dissipated_load == 4


def test_13_oscillation_records_reversals_without_losing_load() -> None:
    before = oscillation_load()
    result = require_discharge(
        oscillate(
            before,
            default_network(),
            OPEN,
            B_TRIGGER,
            oscillation_law(),
        )
    )

    assert tuple(step.link.identifier for step in result.trace.steps) == (
        "b-c",
        "c-b",
        "b-c",
        "c-b",
    )
    assert result.residue.oscillation_reversals == 3
    assert total_stress(result.after.field) == total_stress(before.field)


def test_14_equal_present_results_retain_gradual_or_sudden_history() -> None:
    network = default_network()
    gradual = require_discharge(
        discharge(gradual_source_load(), network, OPEN, SOURCE_TRIGGER)
    )
    sudden = require_discharge(
        discharge(sudden_source_load(), network, OPEN, SOURCE_TRIGGER)
    )

    assert gradual.after.field == sudden.after.field
    assert gradual.after.delivered == sudden.after.delivered == 6
    assert len(gradual.residue.loading_events) == 3
    assert len(sudden.residue.loading_events) == 1
    assert gradual.residue != sudden.residue


def test_15_blocking_one_path_exposes_a_mechanical_alternative() -> None:
    result = require_discharge(
        discharge(
            gradual_source_load(),
            default_network(),
            BLOCK_NORTH,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )
    report = report_blocked_alternative("a-b", first_path(result))

    assert first_path(result) == "a-c"
    assert report.alternative_used == "a-c"
    assert not report.no_path


def test_16_blocking_every_source_path_returns_no_path() -> None:
    result = discharge(
        gradual_source_load(),
        default_network(),
        BLOCK_BOTH,
        SOURCE_TRIGGER,
    )

    assert isinstance(result, NoDischargePath)
    assert result.state == gradual_source_load()


def test_17_single_number_countermodel_loses_path_information() -> None:
    network = default_network()
    left = require_discharge(
        discharge(
            north_obstructed_distribution(),
            network,
            SOURCE_ONLY,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )
    right = require_discharge(
        discharge(
            south_obstructed_distribution(),
            network,
            SOURCE_ONLY,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    report = report_scalar_loss(
        left.before.field,
        right.before.field,
        first_path(left),
        first_path(right),
    )

    assert report.scalar.total == 10
    assert report.fields_differ
    assert report.paths_differ


def test_18_target_coded_discharge_is_rejected() -> None:
    result = reject_target_coded_discharge("a-c")

    assert isinstance(result, CountermodelRejection)
    assert result.countermodel == "target-coded-discharge"
    assert "smuggled" in result.reason


def test_19_trigger_only_causation_is_incomplete() -> None:
    result = reject_trigger_only_causation(SOURCE_TRIGGER)

    assert isinstance(result, IncompleteCausalAccount)
    assert result.trigger is SOURCE_TRIGGER
    assert result.missing_antecedents == (
        "distributed field",
        "network topology",
        "constraints",
        "transfer law",
    )


def test_20_release_cannot_erase_historical_residue() -> None:
    result = require_discharge(
        discharge(
            gradual_source_load(),
            default_network(),
            OPEN,
            SOURCE_TRIGGER,
            maximum_steps=2,
        )
    )

    rejection = reject_history_erasure(result)

    assert result.residue.loading_events
    assert result.residue.displaced_load > 0
    assert result.residue.released_load > 0
    assert rejection.countermodel == "release-erases-history"


def test_21_stored_capacity_does_not_encode_the_discharge_path() -> None:
    network = default_network()
    profile = capacity_profile(network)
    left = require_discharge(
        discharge(
            north_obstructed_distribution(),
            network,
            SOURCE_ONLY,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )
    right = require_discharge(
        discharge(
            south_obstructed_distribution(),
            network,
            SOURCE_ONLY,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    boundary = reject_capacity_as_symmetric_potential(profile)

    assert boundary.profile is profile
    assert not boundary.path_encoded
    assert first_path(left) != first_path(right)


def test_22_capacity_is_not_a_transitive_family_of_candidate_results() -> None:
    boundary = reject_capacity_as_symmetric_potential(
        capacity_profile(default_network())
    )

    assert not boundary.transitive_alternatives
    assert "neither a candidate outcome" in boundary.reason


def test_23_discharge_preserves_its_source_and_creates_owned_states() -> None:
    source = gradual_source_load()
    snapshot = gradual_source_load()

    result = require_discharge(
        discharge(
            source,
            default_network(),
            OPEN,
            SOURCE_TRIGGER,
            maximum_steps=1,
        )
    )

    assert source == snapshot
    assert result.before is source
    assert result.after is not source
    assert result.trace.steps[0].before is source.field
    assert result.trace.steps[0].after is not source.field


def test_24_experiment_imports_no_package_or_other_experiment() -> None:
    experiment_root = Path(source_model_module.__file__).parent
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


def test_25_neutral_mechanics_define_no_foundation_named_classes() -> None:
    experiment_root = Path(source_model_module.__file__).parent
    forbidden = {"Form", "Will", "Spell", "Reader", "Cast", "Effect", "Potential"}
    defined: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        defined.update(
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

    assert defined.isdisjoint(forbidden)


def test_26_post_hoc_mapping_can_reject_or_leave_roles_unmapped() -> None:
    report = attempt_mapping()
    capacity = next(
        item for item in report.mappings if item.neutral_term == "CapacityProfile"
    )
    discharge_mapping = next(
        item
        for item in report.mappings
        if item.neutral_term == "Discharge and CausalTrace"
    )

    assert capacity.status is MappingStatus.REJECTED
    assert discharge_mapping.status is MappingStatus.UNMAPPED
    assert not report.finding.stress_is_scalar
    assert not report.finding.trigger_is_complete_cause


def test_27_package_source_remains_untouched() -> None:
    repository_root = Path(source_model_module.__file__).parents[2]
    result = subprocess.run(
        ["git", "status", "--short", "--", "src/arx_mentis"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert not result.stdout.strip()


def test_28_complete_release_can_resolve_and_independently_conform() -> None:
    result = require_discharge(
        discharge(
            gradual_source_load(),
            default_network(),
            OPEN,
            SOURCE_TRIGGER,
        )
    )

    resolution = assess_resolution(result.after, SAFE_RESOLUTION)
    acceptance = assess_acceptance(result.after, DELIVERY_ACCEPTANCE)

    assert result.after.delivered == 6
    assert resolution.resolved
    assert acceptance.accepted


def test_29_exact_mechanical_tie_does_not_select_by_storage_order() -> None:
    network = ConstrainedNetwork(
        "symmetric-test-network",
        (
            Link("first", Site.A, Site.B, 2, 1, 99, LinkKind.TRANSFER),
            Link("second", Site.A, Site.C, 2, 1, 99, LinkKind.TRANSFER),
        ),
    )
    state = load_suddenly(empty_state(), Site.A, 6)

    forward = discharge(
        state,
        network,
        ConstraintSet("open"),
        SOURCE_TRIGGER,
        maximum_steps=1,
    )
    reverse_network = ConstrainedNetwork(
        network.identifier, tuple(reversed(network.links))
    )
    reversed_result = discharge(
        state,
        reverse_network,
        ConstraintSet("open"),
        SOURCE_TRIGGER,
        maximum_steps=1,
    )

    assert isinstance(forward, AmbiguousDischarge)
    assert isinstance(reversed_result, AmbiguousDischarge)
    assert forward.candidates == reversed_result.candidates == ("first", "second")


def test_30_nominal_discharge_api_contains_no_target_or_acceptance_input() -> None:
    parameters = inspect.signature(discharge).parameters

    assert "target" not in parameters
    assert "preferred_path" not in parameters
    assert "acceptance" not in parameters
    assert tuple(parameters) == (
        "state",
        "network",
        "constraints",
        "trigger",
        "maximum_steps",
    )
