"""Deterministic baseline, correspondence, surprise, and selection scenarios."""

from __future__ import annotations

from dataclasses import dataclass

from .source_model import (
    Baseline,
    CauseChannel,
    Correspondence,
    Event,
    EventStream,
    MatchRule,
    Observation,
    Rate,
    RecordedAim,
    WorldEvent,
)


def compare(aim: RecordedAim, event: Event, rule: MatchRule) -> Correspondence:
    return Correspondence(
        aim,
        event,
        rule,
        event.occurred_order > aim.recorded_order
        and rule.required_feature == aim.desired_feature
        and rule.required_feature in event.features,
    )


def rate(correspondences: tuple[Correspondence, ...]) -> Rate:
    return Rate(
        sum(item.matches for item in correspondences),
        len(correspondences),
    )


def greater(first: Rate, second: Rate) -> bool:
    return first.matches * second.trials > second.matches * first.trials


@dataclass(frozen=True, slots=True)
class SurpriseAssessment:
    correspondence: Correspondence
    observed_rate: Rate
    baseline_rate: Rate
    unusual: bool


def assess_surprise(
    correspondence: Correspondence,
    observed_rate: Rate,
    baseline: Baseline,
) -> SurpriseAssessment:
    return SurpriseAssessment(
        correspondence,
        observed_rate,
        baseline.expected_rate,
        greater(observed_rate, baseline.expected_rate),
    )


@dataclass(frozen=True, slots=True)
class ChanceScenario:
    aim: RecordedAim
    rule: MatchRule
    stream: EventStream
    correspondences: tuple[Correspondence, ...]
    matching_world_event: WorldEvent


def make_chance_scenario() -> ChanceScenario:
    aim = RecordedAim("aim-red-feather", 0, "red-feather")
    rule = MatchRule("exact recorded feature", "red-feather")
    features = (
        frozenset({"rain"}),
        frozenset({"blue-thread"}),
        frozenset({"red-feather"}),
        frozenset({"traffic"}),
        frozenset({"birdsong"}),
        frozenset({"plain-stone"}),
    )
    events = tuple(
        WorldEvent(
            Event(
                f"baseline-{index}",
                index,
                event_features,
                f"baseline event {index}",
            ),
            CauseChannel.ORDINARY_CHANCE,
        )
        for index, event_features in enumerate(features, start=1)
    )
    stream = EventStream(Baseline("ordinary baseline", Rate(1, 6)), events)
    correspondences = tuple(compare(aim, item.event, rule) for item in events)
    matching = next(
        item
        for item, correspondence in zip(events, correspondences, strict=True)
        if correspondence.matches
    )
    return ChanceScenario(aim, rule, stream, correspondences, matching)


@dataclass(frozen=True, slots=True)
class SelectionReport:
    source_stream: EventStream
    all_correspondences: tuple[Correspondence, ...]
    reported: tuple[Observation, ...]
    raw_rate: Rate
    reported_rate: Rate
    generator_unchanged: bool


def report_only_matches(scenario: ChanceScenario) -> SelectionReport:
    reported = tuple(
        Observation("selective observer", correspondence.event, index)
        for index, correspondence in enumerate(scenario.correspondences, start=1)
        if correspondence.matches
    )
    reported_correspondences = tuple(
        compare(scenario.aim, item.event, scenario.rule) for item in reported
    )
    return SelectionReport(
        scenario.stream,
        scenario.correspondences,
        reported,
        rate(scenario.correspondences),
        rate(reported_correspondences),
        generator_unchanged=True,
    )
