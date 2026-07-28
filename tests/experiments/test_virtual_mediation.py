from __future__ import annotations

import ast
import subprocess
from dataclasses import replace
from pathlib import Path

import experiments.virtual_mediation.composition as composition_module
import experiments.virtual_mediation.mediation as mediation_module
import experiments.virtual_mediation.observation as observation_module
import experiments.virtual_mediation.source_model as source_model_module
import experiments.virtual_mediation.symmetry as symmetry_module
from experiments.virtual_mediation.composition import (
    correlated_image,
    forget_relationship,
    independent,
    pair_channels,
    product_image,
    shared,
    twisted,
)
from experiments.virtual_mediation.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.virtual_mediation.mediation import (
    ENDPOINT_REACHED,
    THROUGH_ALPHA,
    MediationRecord,
    VariableAssessment,
    assess,
    lift_aggregate,
    lift_signatures,
    make_interaction,
    mediate,
)
from experiments.virtual_mediation.observation import (
    EvidenceConflict,
    Identification,
    IdentifiedPair,
    PartiallyIdentified,
    RejectedObservation,
    identify,
    identify_correlated,
    identify_independent_first,
    signature_observation,
)
from experiments.virtual_mediation.source_model import (
    Accepted,
    Breakdown,
    Channel,
    Denied,
    Intervention,
    Observation,
    ObservationKind,
    Permission,
    Situation,
)
from experiments.virtual_mediation.symmetry import (
    CHANNELS,
    ROTATIONS,
    assess_default,
    check_cyclic_action,
    choose_listed_first,
    image,
    rotate,
)


def make_records() -> tuple[Situation, MediationRecord, MediationRecord]:
    situation = Situation(frozenset({Permission.MEDIATE_TRANSFER}))
    first = mediate(
        Intervention(make_interaction("first", "stress-a", "event-a", 7)),
        situation,
    )
    second = mediate(
        Intervention(make_interaction("second", "stress-b", "event-b", 7)),
        situation,
    )
    assert isinstance(first, MediationRecord)
    assert isinstance(second, MediationRecord)
    return situation, first, second


def test_01_neutral_mechanism_works_without_foundation_types() -> None:
    _, first, _ = make_records()
    forbidden = {"Potential", "Point", "Spell", "Cast", "Effect", "Will", "Witness"}
    neutral_modules = (
        source_model_module,
        symmetry_module,
        mediation_module,
        observation_module,
        composition_module,
    )

    assert first.outcome.reached
    assert first.outcome.transfer.units == 7
    assert all(
        name not in module.__dict__ for module in neutral_modules for name in forbidden
    )


def test_02_cyclic_action_is_lawful_free_and_transitive() -> None:
    report = check_cyclic_action()

    assert report.closed
    assert report.identity_holds
    assert report.composition_holds
    assert report.inverses_hold
    assert report.free
    assert report.transitive


def test_03_each_trace_varies_equivariantly() -> None:
    _, first, _ = make_records()

    assert first.traces.law.holds
    assert first.traces.law.checked_pairs == 9
    assert all(
        assignment.coordinate is assignment.value.mediator.channel
        for assignment in first.traces.assignments
    )


def test_04_aggregate_lifts_uniformly_and_becomes_invariant() -> None:
    _, first, _ = make_records()

    aggregate = lift_aggregate(first.traces)

    assert aggregate.transfer == first.outcome.transfer
    assert aggregate.checked_channels == CHANNELS
    assert aggregate.source_family is first.traces
    assert aggregate.transfer_family.law.holds
    assert len(image(aggregate.transfer_family)) == 1
    assert len(first.traces.assignments) == 3


def test_05_signature_lift_remains_an_unresolved_family() -> None:
    _, first, _ = make_records()

    signatures = lift_signatures(first.traces)

    assert signatures.law.holds
    assert len(signatures.assignments) == 3
    assert {signature.channel for signature in image(signatures)} == CHANNELS


def test_06_shared_composition_has_three_correlated_results() -> None:
    _, first, second = make_records()

    result = shared(first.traces, second.traces)

    assert result.joint.law.holds
    assert len(correlated_image(result)) == 3
    assert all(a is b for a, b in map(pair_channels, correlated_image(result)))


def test_07_twisted_composition_has_three_shifted_results() -> None:
    _, first, second = make_records()

    result = twisted(first.traces, second.traces)

    assert result.joint.law.holds
    assert len(correlated_image(result)) == 3
    assert all(
        rotate(first_channel, source_model_module.Rotation.ONE) is second_channel
        for first_channel, second_channel in map(
            pair_channels,
            correlated_image(result),
        )
    )


def test_08_independent_composition_has_nine_results() -> None:
    _, first, second = make_records()

    result = independent(first.traces, second.traces)

    assert len(product_image(result)) == 9
    assert {pair_channels(pair) for pair in product_image(result)} == {
        (first_channel, second_channel)
        for first_channel in CHANNELS
        for second_channel in CHANNELS
    }


def test_09_option_bag_countermodel_loses_all_three_relationships() -> None:
    _, first, second = make_records()
    shared_value = shared(first.traces, second.traces)
    twisted_value = twisted(first.traces, second.traces)
    independent_value = independent(first.traces, second.traces)

    shared_bag = forget_relationship(shared_value)
    twisted_bag = forget_relationship(twisted_value)
    independent_bag = forget_relationship(independent_value)

    assert shared_bag == twisted_bag == independent_bag
    assert len(shared_bag.first.options) == 3
    assert len(shared_bag.second.options) == 3


def test_10_later_evidence_identifies_shared_and_twisted_correlations() -> None:
    situation, first, second = make_records()
    shared_value = shared(first.traces, second.traces)
    twisted_value = twisted(first.traces, second.traces)
    prior_outcome = first.outcome
    later = replace(
        situation,
        observations=frozenset({signature_observation("first", Channel.BETA)}),
    )

    shared_result = identify_correlated(shared_value, later.observations)
    twisted_result = identify_correlated(twisted_value, later.observations)

    assert isinstance(shared_result, IdentifiedPair)
    shared_channels = pair_channels(
        composition_module.JointTrace(shared_result.first, shared_result.second)
    )
    assert shared_channels == (
        Channel.BETA,
        Channel.BETA,
    )
    assert isinstance(twisted_result, IdentifiedPair)
    assert pair_channels(
        composition_module.JointTrace(twisted_result.first, twisted_result.second)
    ) == (Channel.BETA, Channel.GAMMA)
    assert first.outcome is prior_outcome


def test_11_identifying_one_independent_frame_leaves_the_other_unchanged() -> None:
    situation, first, second = make_records()
    product = independent(first.traces, second.traces)
    later = replace(
        situation,
        observations=frozenset({signature_observation("first", Channel.BETA)}),
    )

    result = identify_independent_first(product, later.observations)

    assert isinstance(result, PartiallyIdentified)
    assert result.first.mediator.channel is Channel.BETA
    assert result.second is second.traces
    assert len(result.second.assignments) == 3


def test_12_irrelevant_and_insufficient_evidence_preserve_identity() -> None:
    _, first, _ = make_records()
    irrelevant = frozenset({signature_observation("other", Channel.BETA)})
    insufficient = frozenset(
        {Observation("first", ObservationKind.ENDPOINT, signature=None)}
    )

    assert identify(first.traces, irrelevant) is first.traces
    assert identify(first.traces, insufficient) is first.traces


def test_13_contradictory_evidence_is_explicit() -> None:
    _, first, _ = make_records()
    observations = frozenset(
        {
            signature_observation("first", Channel.ALPHA),
            signature_observation("first", Channel.BETA),
        }
    )

    result = identify(first.traces, observations)

    assert isinstance(result, EvidenceConflict)


def test_14_observation_outside_the_law_is_rejected() -> None:
    _, first, _ = make_records()
    undeclared = Observation("first", ObservationKind.UNDECLARED, signature=None)

    result = identify(first.traces, frozenset({undeclared}))

    assert isinstance(result, RejectedObservation)
    assert result.observation is undeclared


def test_15_invariant_criterion_accepts_without_identifying_channel() -> None:
    _, first, _ = make_records()

    result = assess(ENDPOINT_REACHED, first)

    assert isinstance(result, Accepted)
    assert result.checked_channels == CHANNELS
    assert len(first.traces.assignments) == 3


def test_16_channel_specific_criterion_produces_nonconstant_truth_family() -> None:
    _, first, _ = make_records()

    result = assess(THROUGH_ALPHA, first)

    assert isinstance(result, VariableAssessment)
    assert result.truths.law.holds
    assert {truth.holds for truth in image(result.truths)} == {True, False}
    assert {truth.channel for truth in image(result.truths) if truth.holds} == {
        Channel.ALPHA
    }


def test_17_no_channel_or_list_position_supplies_a_default() -> None:
    reports = tuple(assess_default(channel) for channel in CHANNELS)
    forward = choose_listed_first((Channel.ALPHA, Channel.BETA, Channel.GAMMA))
    reversed_order = choose_listed_first((Channel.GAMMA, Channel.BETA, Channel.ALPHA))

    assert all(not report.fixed_by_all_rotations for report in reports)
    assert all(not report.legitimate for report in reports)
    assert forward.candidate is not reversed_order.candidate
    assert not forward.legitimate
    assert not reversed_order.legitimate


def test_18_source_interaction_remains_unchanged() -> None:
    situation = Situation(frozenset({Permission.MEDIATE_TRANSFER}))
    interaction = make_interaction("first", "stress-a", "event-a", 7)
    original = replace(interaction)

    result = mediate(Intervention(interaction), situation)

    assert isinstance(result, MediationRecord)
    assert result.source is interaction
    assert interaction == original


def test_19_results_are_owned_and_provenance_is_inspectable() -> None:
    _, first, _ = make_records()

    assert first.outcome is not first.source
    assert first.traces is not first.source
    assert len(first.provenance) == 2
    assert all(
        trace.provenance.operation == "mediate-transfer"
        for trace in image(first.traces)
    )
    assert all(trace.provenance.sources for trace in image(first.traces))


def test_20_experiment_imports_no_existing_model_or_package() -> None:
    experiment_root = Path(mediation_module.__file__).parent
    forbidden_prefixes = (
        "arx_mentis",
        "experiments.euclid_i_1",
        "experiments.ars_astronomica_settlement",
        "experiments.ars_grammatica_reading",
        "experiments.ars_dialectica_verification",
    )

    imported: set[str] = set()
    for path in experiment_root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)

    assert not any(
        name.startswith(prefix) for name in imported for prefix in forbidden_prefixes
    )


def test_21_installable_package_worktree_is_untouched() -> None:
    repository = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [
            "git",
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--",
            "src/arx_mentis",
        ],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout == ""


def test_22_mapping_records_virtuality_and_dual_result_pressure() -> None:
    _, first, _ = make_records()
    assessment = assess(ENDPOINT_REACHED, first)
    assert isinstance(assessment, Accepted)

    report = attempt_mapping(first, assessment)

    assert report.virtuality.operationally_definite_per_coordinate
    assert not report.virtuality.mediator_directly_observed
    assert report.virtuality.locating_coordinate_unresolved
    assert report.result_shape.public_outcome_settled
    assert report.result_shape.internal_mediation_unresolved
    assert report.result_shape.retained_together
    assert any(mapping.status is MappingStatus.PRESSURE for mapping in report.mappings)
    assert {mapping.provisional_reading for mapping in report.mappings} >= {
        "Refusal candidate",
        "Failure candidate",
    }


def test_23_denied_and_broken_transfers_remain_distinct_neutral_results() -> None:
    interaction = make_interaction("first", "stress-a", "event-a", 7)
    denied = mediate(Intervention(interaction), Situation(frozenset()))
    broken = mediate(
        Intervention(replace(interaction, broken=True)),
        Situation(frozenset({Permission.MEDIATE_TRANSFER})),
    )

    assert isinstance(denied, Denied)
    assert isinstance(broken, Breakdown)


def test_24_identified_trace_remains_indirectly_observed() -> None:
    _, first, _ = make_records()
    observation = signature_observation("first", Channel.GAMMA)

    result = identify(first.traces, frozenset({observation}))

    assert isinstance(result, Identification)
    assert result.channel is Channel.GAMMA
    assert result.value.mediator.channel is Channel.GAMMA
    assert not result.value.mediator.directly_observed


def test_25_all_rotations_act_on_all_channels() -> None:
    assert len(ROTATIONS) == 3
    assert {
        rotate(channel, rotation) for channel in CHANNELS for rotation in ROTATIONS
    } == CHANNELS
