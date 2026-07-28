from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import experiments.omen_attribution.attribution as attribution_module
import experiments.omen_attribution.baseline as baseline_module
import experiments.omen_attribution.causation as causation_module
import experiments.omen_attribution.intervention as intervention_module
import experiments.omen_attribution.source_model as source_model_module
import experiments.omen_attribution.symmetry_attempt as symmetry_module
from experiments.omen_attribution.attribution import (
    AttributionReport,
    EvidenceConflict,
    attribute,
    make_hypotheses,
    score,
)
from experiments.omen_attribution.baseline import (
    assess_surprise,
    compare,
    greater,
    make_chance_scenario,
    rate,
    report_only_matches,
)
from experiments.omen_attribution.causation import (
    make_behavioral_scenario,
    observer_view,
    same_observable_different_causes,
)
from experiments.omen_attribution.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.omen_attribution.intervention import block_operator_behavior
from experiments.omen_attribution.source_model import (
    CauseChannel,
    Correspondence,
    Evidence,
    EvidenceKind,
    HypothesisKind,
    MatchRule,
    ObservedEvent,
    Rate,
)
from experiments.omen_attribution.symmetry_attempt import attempt_transitive_frame


def initial_attribution() -> tuple[object, Correspondence, AttributionReport]:
    scenario = make_chance_scenario()
    event = scenario.matching_world_event.event
    correspondence = compare(scenario.aim, event, scenario.rule)
    result = attribute(event, correspondence, make_hypotheses())
    assert isinstance(result, AttributionReport)
    return scenario, correspondence, result


def test_01_recorded_aim_precedes_every_event() -> None:
    scenario = make_chance_scenario()

    assert all(
        scenario.aim.recorded_order < item.event.occurred_order
        for item in scenario.stream.events
    )


def test_02_event_occurrence_is_separate_from_correspondence() -> None:
    scenario = make_chance_scenario()
    nonmatching = scenario.stream.events[0].event
    result = compare(scenario.aim, nonmatching, scenario.rule)

    assert nonmatching.occurred_order > scenario.aim.recorded_order
    assert not result.matches
    assert isinstance(result, Correspondence)


def test_03_correspondence_is_separate_from_causal_attribution() -> None:
    _, correspondence, report = initial_attribution()

    assert correspondence.matches
    assert report.correspondence is correspondence
    assert report.selected is None
    assert report.underdetermined


def test_04_ordinary_chance_can_produce_a_real_match() -> None:
    scenario, correspondence, report = initial_attribution()

    assert correspondence.matches
    assert scenario.matching_world_event.definite_cause is CauseChannel.ORDINARY_CHANCE
    assert score(report, HypothesisKind.CHANCE) > 0
    assert score(report, HypothesisKind.ANOMALOUS) == 0


def test_05_selective_reporting_raises_apparent_rate_without_new_events() -> None:
    scenario = make_chance_scenario()

    report = report_only_matches(scenario)

    assert report.source_stream is scenario.stream
    assert report.generator_unchanged
    assert report.raw_rate == Rate(1, 6)
    assert report.reported_rate == Rate(1, 1)
    assert greater(report.reported_rate, report.raw_rate)


def test_06_behavioral_mediation_has_an_inspectable_causal_chain() -> None:
    scenario = make_behavioral_scenario()

    assert scenario.account.hypothesis is HypothesisKind.BEHAVIOR
    assert scenario.account.result.definite_cause is CauseChannel.OPERATOR_BEHAVIOR
    assert tuple(link.relation for link in scenario.account.links) == (
        "changes",
        "changes",
        "changes",
        "produces",
    )
    assert scenario.account.links[-1].target == scenario.observed.event.identifier


def test_07_same_observable_event_can_have_different_definite_causes() -> None:
    scenario = make_behavioral_scenario()

    worlds = same_observable_different_causes(scenario.observed.event)

    assert len(worlds) == 4
    assert all(item.event is scenario.observed.event for item in worlds)
    assert len({item.definite_cause for item in worlds}) == 4


def test_08_correspondence_alone_cannot_reveal_true_cause() -> None:
    scenario = make_behavioral_scenario()
    observed = observer_view(scenario.account.result)
    rule = MatchRule("behavioral match", "conversation")
    correspondence = compare(scenario.aim, observed.event, rule)

    report = attribute(observed.event, correspondence, make_hypotheses())

    assert isinstance(report, AttributionReport)
    assert report.selected is None
    assert report.underdetermined
    assert not observed.cause_available


def test_09_relevant_evidence_changes_attribution_support() -> None:
    scenario, correspondence, initial = initial_attribution()
    event = scenario.matching_world_event.event
    evidence = Evidence(
        "operator-action-log",
        event.identifier,
        EvidenceKind.ACTION_LOG,
        supports=frozenset({HypothesisKind.BEHAVIOR}),
        weakens=frozenset({HypothesisKind.CHANCE}),
        strength=2,
        note="operator action preceded the matching event",
    )

    updated = attribute(
        event,
        correspondence,
        make_hypotheses(),
        frozenset({evidence}),
    )

    assert isinstance(updated, AttributionReport)
    assert score(updated, HypothesisKind.BEHAVIOR) > score(
        initial,
        HypothesisKind.BEHAVIOR,
    )
    assert score(updated, HypothesisKind.CHANCE) < score(
        initial,
        HypothesisKind.CHANCE,
    )


def test_10_irrelevant_evidence_changes_nothing() -> None:
    scenario, correspondence, initial = initial_attribution()
    evidence = Evidence(
        "unrelated-action-log",
        "another-event",
        EvidenceKind.ACTION_LOG,
        supports=frozenset({HypothesisKind.BEHAVIOR}),
        weakens=frozenset(),
        strength=9,
        note="evidence concerns another event",
    )

    result = attribute(
        scenario.matching_world_event.event,
        correspondence,
        make_hypotheses(),
        frozenset({evidence}),
    )

    assert result == initial


def test_11_contradictory_evidence_remains_explicit() -> None:
    scenario, correspondence, _ = initial_attribution()
    event = scenario.matching_world_event.event
    supporting = Evidence(
        "action-log-a",
        event.identifier,
        EvidenceKind.ACTION_LOG,
        supports=frozenset({HypothesisKind.BEHAVIOR}),
        weakens=frozenset(),
        strength=2,
        note="records an action",
    )
    weakening = Evidence(
        "action-log-b",
        event.identifier,
        EvidenceKind.ACTION_LOG,
        supports=frozenset(),
        weakens=frozenset({HypothesisKind.BEHAVIOR}),
        strength=2,
        note="denies that action",
    )

    result = attribute(
        event,
        correspondence,
        make_hypotheses(),
        frozenset({supporting, weakening}),
    )

    assert isinstance(result, EvidenceConflict)
    assert result.hypothesis is HypothesisKind.BEHAVIOR


def test_12_intervention_distinguishes_operator_dependent_hypotheses() -> None:
    scenario, correspondence, initial = initial_attribution()
    event = scenario.matching_world_event.event
    intervention = block_operator_behavior(scenario.aim, event.identifier)

    updated = attribute(
        event,
        correspondence,
        make_hypotheses(),
        frozenset({intervention.evidence}),
    )

    assert isinstance(updated, AttributionReport)
    assert intervention.intervention.preserved_aim is scenario.aim
    assert intervention.before.matches > intervention.after.matches
    assert score(updated, HypothesisKind.BEHAVIOR) > score(
        initial,
        HypothesisKind.BEHAVIOR,
    )
    assert score(updated, HypothesisKind.SELF_ORGANIZATION) < score(
        initial,
        HypothesisKind.SELF_ORGANIZATION,
    )


def test_13_several_hypotheses_remain_supported_after_intervention() -> None:
    scenario, correspondence, _ = initial_attribution()
    event = scenario.matching_world_event.event
    intervention = block_operator_behavior(scenario.aim, event.identifier)

    result = attribute(
        event,
        correspondence,
        make_hypotheses(),
        frozenset({intervention.evidence}),
    )

    assert isinstance(result, AttributionReport)
    supported = tuple(item for item in result.support if item.score > 0)
    assert len(supported) == 5
    assert result.underdetermined
    assert result.selected is None


def test_14_causal_hypotheses_fail_a_structure_preserving_transitive_action() -> None:
    result = attempt_transitive_frame(make_hypotheses())

    assert result.proposed_cycle_transitive
    assert not result.proposed_cycle_preserves_structure
    assert not result.lawful_relation_transitive
    assert len(result.lawful_orbits) == 6
    assert len(result.failures) == 6


def test_15_hidden_definite_cause_is_distinct_from_unresolved_attribution() -> None:
    scenario = make_behavioral_scenario()
    world = scenario.account.result
    observed = observer_view(world)
    correspondence = compare(
        scenario.aim,
        observed.event,
        MatchRule("behavioral match", "conversation"),
    )
    result = attribute(observed.event, correspondence, make_hypotheses())

    assert world.definite_cause is CauseChannel.OPERATOR_BEHAVIOR
    assert not observed.cause_available
    assert isinstance(result, AttributionReport)
    assert result.underdetermined


def test_16_observed_outcome_is_settled_while_attribution_remains_unresolved() -> None:
    scenario = make_behavioral_scenario()
    event = scenario.observed.event
    correspondence = compare(
        scenario.aim,
        event,
        MatchRule("behavioral match", "conversation"),
    )
    result = attribute(event, correspondence, make_hypotheses())

    assert event.identifier == "conversation-event"
    assert correspondence.matches
    assert isinstance(result, AttributionReport)
    assert result.underdetermined


def test_17_experiment_imports_no_existing_model_or_package() -> None:
    experiment_root = Path(attribution_module.__file__).parent
    forbidden_prefixes = (
        "arx_mentis",
        "experiments.euclid_i_1",
        "experiments.ars_astronomica_settlement",
        "experiments.ars_grammatica_reading",
        "experiments.ars_dialectica_verification",
        "experiments.virtual_mediation",
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


def test_18_installable_package_worktree_remains_untouched() -> None:
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


def test_19_surprise_is_separate_from_correspondence() -> None:
    scenario = make_chance_scenario()
    correspondence = next(item for item in scenario.correspondences if item.matches)
    raw = rate(scenario.correspondences)
    selected = report_only_matches(scenario)

    ordinary = assess_surprise(correspondence, raw, scenario.stream.baseline)
    apparent = assess_surprise(
        correspondence,
        selected.reported_rate,
        scenario.stream.baseline,
    )

    assert correspondence.matches
    assert not ordinary.unusual
    assert apparent.unusual


def test_20_foundation_mapping_rejects_universal_symmetric_unresolvedness() -> None:
    scenario = make_behavioral_scenario()
    observed = observer_view(scenario.account.result)
    correspondence = compare(
        scenario.aim,
        observed.event,
        MatchRule("behavioral match", "conversation"),
    )
    attribution = attribute(observed.event, correspondence, make_hypotheses())
    symmetry = attempt_transitive_frame(make_hypotheses())
    assert isinstance(attribution, AttributionReport)

    report = attempt_mapping(
        scenario.account.result,
        observed,
        correspondence,
        attribution,
        symmetry,
    )

    assert report.split.world_cause_definite
    assert not report.split.cause_available_to_observer
    assert report.split.attribution_underdetermined
    assert report.split.outcome_occurred
    assert report.split.correspondence_established
    assert not report.split.causal_explanation_verified
    assert report.boundary.symmetric_construction_law_retained
    assert report.boundary.universal_unresolved_algebra_rejected
    assert any(mapping.status is MappingStatus.REJECTED for mapping in report.mappings)


def test_21_neutral_modules_define_no_foundation_classes() -> None:
    forbidden = {"Potential", "Point", "Spell", "Cast", "Effect", "Will", "Witness"}
    neutral_modules = (
        source_model_module,
        baseline_module,
        causation_module,
        attribution_module,
        intervention_module,
        symmetry_module,
    )

    assert all(
        name not in module.__dict__ for module in neutral_modules for name in forbidden
    )


def test_22_observer_view_cannot_expose_world_cause() -> None:
    scenario = make_behavioral_scenario()

    observed = observer_view(scenario.account.result)

    assert isinstance(observed, ObservedEvent)
    assert not observed.cause_available
    assert not hasattr(observed, "definite_cause")
    assert scenario.account.result.definite_cause is CauseChannel.OPERATOR_BEHAVIOR
