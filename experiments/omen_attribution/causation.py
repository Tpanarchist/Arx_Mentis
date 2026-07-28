"""Causal chains and the separation of hidden world state from observer records."""

from __future__ import annotations

from dataclasses import dataclass

from .source_model import (
    CausalAccount,
    CausalLink,
    CauseChannel,
    Event,
    HypothesisKind,
    ObservedEvent,
    RecordedAim,
    WorldEvent,
)


@dataclass(frozen=True, slots=True)
class BehavioralScenario:
    aim: RecordedAim
    account: CausalAccount
    observed: ObservedEvent


def make_behavioral_scenario() -> BehavioralScenario:
    aim = RecordedAim("aim-open-conversation", 0, "conversation")
    event = Event(
        "conversation-event",
        4,
        frozenset({"conversation", "reply"}),
        "another person begins the anticipated conversation",
    )
    world_event = WorldEvent(event, CauseChannel.OPERATOR_BEHAVIOR)
    account = CausalAccount(
        hypothesis=HypothesisKind.BEHAVIOR,
        links=(
            CausalLink(aim.identifier, "changes", "operator-attention"),
            CausalLink("operator-attention", "changes", "operator-action"),
            CausalLink("operator-action", "changes", "environment"),
            CausalLink("environment", "produces", event.identifier),
        ),
        result=world_event,
    )
    return BehavioralScenario(aim, account, ObservedEvent(event))


def observer_view(world_event: WorldEvent) -> ObservedEvent:
    return ObservedEvent(world_event.event, cause_available=False)


def same_observable_different_causes(event: Event) -> tuple[WorldEvent, ...]:
    return tuple(
        WorldEvent(event, cause)
        for cause in (
            CauseChannel.ORDINARY_CHANCE,
            CauseChannel.OPERATOR_BEHAVIOR,
            CauseChannel.SOCIAL_RESPONSE,
            CauseChannel.SELF_ORGANIZATION,
        )
    )
