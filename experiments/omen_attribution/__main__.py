"""Run the human-readable State Zero Experiment 006 witness."""

from .attribution import AttributionReport, attribute, make_hypotheses, score
from .baseline import compare, make_chance_scenario, report_only_matches
from .causation import make_behavioral_scenario, observer_view
from .foundation_mapping import attempt_mapping
from .intervention import block_operator_behavior
from .source_model import HypothesisKind, MatchRule
from .symmetry_attempt import attempt_transitive_frame


def main() -> None:
    chance = make_chance_scenario()
    matching = chance.matching_world_event
    correspondence = compare(chance.aim, matching.event, chance.rule)
    selection = report_only_matches(chance)
    hypotheses = make_hypotheses()
    initial = attribute(matching.event, correspondence, hypotheses)
    intervention = block_operator_behavior(chance.aim, matching.event.identifier)
    updated = attribute(
        matching.event,
        correspondence,
        hypotheses,
        frozenset({intervention.evidence}),
    )
    symmetry = attempt_transitive_frame(hypotheses)
    behavior = make_behavioral_scenario()
    observed = observer_view(behavior.account.result)
    behavior_correspondence = compare(
        behavior.aim,
        observed.event,
        MatchRule("behavioral match", "conversation"),
    )
    behavior_attribution = attribute(
        observed.event,
        behavior_correspondence,
        hypotheses,
    )
    if not isinstance(initial, AttributionReport) or not isinstance(
        updated,
        AttributionReport,
    ):
        print("attribution evidence conflicted")
        return
    if not isinstance(behavior_attribution, AttributionReport):
        print("behavioral attribution evidence conflicted")
        return
    mapping = attempt_mapping(
        behavior.account.result,
        observed,
        behavior_correspondence,
        behavior_attribution,
        symmetry,
    )
    print(
        "chance correspondence: "
        f"occurred={matching.event.identifier}, matched={correspondence.matches}"
    )
    print(
        "selection rates: "
        f"raw={selection.raw_rate.matches}/{selection.raw_rate.trials}, "
        f"reported={selection.reported_rate.matches}/"
        f"{selection.reported_rate.trials}"
    )
    print(
        "intervention support: "
        f"behavior {score(initial, HypothesisKind.BEHAVIOR)} -> "
        f"{score(updated, HypothesisKind.BEHAVIOR)}"
    )
    print(
        "forced symmetry: "
        f"preserves={symmetry.proposed_cycle_preserves_structure}, "
        f"lawful-orbits={len(symmetry.lawful_orbits)}"
    )
    print(f"scope boundary: {mapping.boundary.candidate_scope}")


if __name__ == "__main__":
    main()
