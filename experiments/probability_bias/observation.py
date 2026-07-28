"""Observation windows, post-hoc targets, and observer-relative attribution."""

from __future__ import annotations

from .outcomes import (
    EventStream,
    MechanismKind,
    ObservedSample,
    ObservedTrial,
    ObserverAttribution,
    Outcome,
    PostHocTarget,
    Sample,
)


def observe(stream: EventStream) -> Sample:
    window = stream.plan.observation_window
    trials = stream.trials[window.start : window.stop]
    return Sample(stream, window, trials)


def hide_context(sample: Sample) -> ObservedSample:
    return ObservedSample(
        sample,
        tuple(
            ObservedTrial(trial.order, trial.outcome, False) for trial in sample.trials
        ),
    )


def select_post_hoc_target(stream: EventStream) -> PostHocTarget:
    counts = {outcome: 0 for outcome in Outcome}
    for trial in stream.trials:
        counts[trial.outcome] += 1
    maximum = max(counts.values())
    leaders = tuple(outcome for outcome in Outcome if counts[outcome] == maximum)
    if len(leaders) != 1:
        raise ValueError(
            "post-hoc target witness requires a unique most frequent outcome"
        )
    return PostHocTarget(
        leaders[0],
        selected_after_order=stream.trials[-1].order,
        precommitted=False,
    )


def attribute_from_observation(observed: ObservedSample) -> ObserverAttribution:
    return ObserverAttribution(
        observed,
        frozenset({MechanismKind.INTERVENED, MechanismKind.CONTEXT_MIXTURE}),
        selected=None,
        world_record_available=False,
    )
