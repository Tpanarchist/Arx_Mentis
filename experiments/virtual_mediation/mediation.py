"""Executable neutral mechanics for mediated transfer and uniform lifts."""

from __future__ import annotations

from dataclasses import dataclass

from .source_model import (
    Accepted,
    Breakdown,
    Channel,
    Criterion,
    CriterionTruth,
    Denied,
    Interaction,
    Intervention,
    Mediator,
    Outcome,
    Permission,
    Provenance,
    Rejected,
    Signature,
    Situation,
    Stress,
    Trace,
    Transfer,
)
from .symmetry import (
    CHANNELS,
    ChannelFamily,
    build_family,
    image,
    map_family,
    rotate_signature,
    rotate_trace,
    rotate_truth,
)

ENDPOINT_REACHED = Criterion("the transfer reaches the endpoint")
THROUGH_ALPHA = Criterion("the transfer passes through channel alpha")


@dataclass(frozen=True, slots=True)
class MediationRecord:
    source: Interaction
    intervention: Intervention
    traces: ChannelFamily[Trace]
    outcome: Outcome
    provenance: tuple[Provenance, ...]


type MediationResult = MediationRecord | Denied | Breakdown


def mediate(intervention: Intervention, situation: Situation) -> MediationResult:
    interaction = intervention.interaction
    if Permission.MEDIATE_TRANSFER not in situation.permissions:
        return Denied(
            Permission.MEDIATE_TRANSFER,
            "the situation does not permit mediated transfer",
        )
    if not interaction.direct_transfer_prohibited:
        return Breakdown(
            interaction,
            "this mechanism requires direct transfer to remain prohibited",
        )
    if interaction.broken:
        return Breakdown(interaction, "the permitted mediated transfer broke down")

    transfer = Transfer(interaction.stress.units)

    def build_trace(channel: Channel) -> Trace:
        return Trace(
            interaction.name,
            Mediator(channel, directly_observed=False),
            transfer,
            Provenance(
                "mediate-transfer",
                (interaction.name, channel.value, str(interaction.stress.units)),
            ),
        )

    traces = build_family(
        interaction.name,
        build_trace,
        rotate_trace,
        "rotating a channel rotates the definite mediation trace",
    )
    outcome = Outcome(interaction.name, interaction.endpoint, transfer, reached=True)
    provenance = (
        Provenance("begin-interaction", (interaction.name, interaction.source)),
        Provenance("observe-endpoint", (interaction.endpoint, str(transfer.units))),
    )
    return MediationRecord(interaction, intervention, traces, outcome, provenance)


def signature_of(trace: Trace) -> Signature:
    channel = trace.mediator.channel
    return Signature(
        trace.interaction_name,
        channel,
        f"signature-{channel.value}",
    )


def lift_signatures(traces: ChannelFamily[Trace]) -> ChannelFamily[Signature]:
    return map_family(
        traces,
        signature_of,
        rotate_signature,
        "signature construction commutes with channel rotation",
    )


@dataclass(frozen=True, slots=True)
class AggregateTransfer:
    transfer: Transfer
    source_family: ChannelFamily[Trace]
    transfer_family: ChannelFamily[Transfer]
    checked_channels: frozenset[Channel]


def lift_aggregate(traces: ChannelFamily[Trace]) -> AggregateTransfer:
    transfer_family = map_family(
        traces,
        lambda trace: trace.transfer,
        lambda transfer, _rotation: transfer,
        "aggregate transfer is invariant under channel rotation",
    )
    transfers = image(transfer_family)
    if len(transfers) != 1:
        raise ValueError("aggregate transfer is not invariant across the family")
    return AggregateTransfer(
        next(iter(transfers)),
        traces,
        transfer_family,
        CHANNELS,
    )


@dataclass(frozen=True, slots=True)
class VariableAssessment:
    criterion: Criterion
    truths: ChannelFamily[CriterionTruth]


type Assessment = Accepted | Rejected | VariableAssessment


def assess(criterion: Criterion, record: MediationRecord) -> Assessment:
    if criterion == ENDPOINT_REACHED:
        truth = record.outcome.reached
        if truth:
            return Accepted(criterion, CHANNELS, "every channel reaches the endpoint")
        return Rejected(criterion, CHANNELS, "no channel reaches the endpoint")
    if criterion == THROUGH_ALPHA:
        truths = map_family(
            record.traces,
            lambda trace: CriterionTruth(
                trace.mediator.channel,
                trace.mediator.channel is Channel.ALPHA,
            ),
            rotate_truth,
            "the channel-specific criterion varies with the channel frame",
        )
        return VariableAssessment(criterion, truths)
    return Rejected(criterion, frozenset(), "the criterion is not declared")


def make_interaction(name: str, source: str, endpoint: str, units: int) -> Interaction:
    return Interaction(name, source, endpoint, stress=Stress(units))
