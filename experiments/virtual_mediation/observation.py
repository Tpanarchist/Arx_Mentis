"""Later observations identify channel coordinates without changing prior results."""

from __future__ import annotations

from dataclasses import dataclass

from .composition import CorrelatedMediations, ProductFamily
from .source_model import Channel, Observation, ObservationKind, Signature, Trace
from .symmetry import ChannelFamily, at


@dataclass(frozen=True, slots=True)
class ObservationLaw:
    discriminating_kind: ObservationKind
    non_discriminating_kind: ObservationKind


SIGNATURE_LAW = ObservationLaw(
    ObservationKind.SIGNATURE,
    ObservationKind.ENDPOINT,
)


@dataclass(frozen=True, slots=True)
class Identification[T]:
    channel: Channel
    value: T
    evidence: frozenset[Observation]


@dataclass(frozen=True, slots=True)
class EvidenceConflict:
    subject: str
    evidence: frozenset[Observation]
    reason: str


@dataclass(frozen=True, slots=True)
class RejectedObservation:
    observation: Observation
    reason: str


type IdentificationResult[T] = (
    ChannelFamily[T] | Identification[T] | EvidenceConflict | RejectedObservation
)


def signature_observation(subject: str, channel: Channel) -> Observation:
    return Observation(
        subject,
        ObservationKind.SIGNATURE,
        Signature(subject, channel, f"signature-{channel.value}"),
    )


def _identified_channel(
    subject: str,
    observations: frozenset[Observation],
) -> Channel | EvidenceConflict | RejectedObservation | None:
    related = frozenset(item for item in observations if item.subject == subject)
    undeclared = next(
        (item for item in related if item.kind is ObservationKind.UNDECLARED),
        None,
    )
    if undeclared is not None:
        return RejectedObservation(
            undeclared,
            "the observation method lies outside the declared observation law",
        )
    signatures = frozenset(
        item
        for item in related
        if item.kind is SIGNATURE_LAW.discriminating_kind and item.signature is not None
    )
    channels = frozenset(
        item.signature.channel for item in signatures if item.signature
    )
    if len(channels) > 1:
        return EvidenceConflict(
            subject,
            signatures,
            "signature observations identify contradictory channels",
        )
    return next(iter(channels)) if channels else None


def identify[T](
    family: ChannelFamily[T],
    observations: frozenset[Observation],
) -> IdentificationResult[T]:
    result = _identified_channel(family.subject, observations)
    if isinstance(result, (EvidenceConflict, RejectedObservation)):
        return result
    if result is None:
        return family
    relevant = frozenset(
        item
        for item in observations
        if item.subject == family.subject and item.kind is ObservationKind.SIGNATURE
    )
    return Identification(result, at(family, result), relevant)


@dataclass(frozen=True, slots=True)
class IdentifiedPair:
    first: Trace
    second: Trace
    evidence: frozenset[Observation]


type CorrelatedIdentification = (
    CorrelatedMediations | IdentifiedPair | EvidenceConflict | RejectedObservation
)


def identify_correlated(
    value: CorrelatedMediations,
    observations: frozenset[Observation],
) -> CorrelatedIdentification:
    result = _identified_channel(value.first.subject, observations)
    if isinstance(result, (EvidenceConflict, RejectedObservation)):
        return result
    if result is None:
        return value
    pairs = tuple(
        assignment.value
        for assignment in value.joint.assignments
        if assignment.value.first.mediator.channel is result
    )
    if len(pairs) != 1:
        return EvidenceConflict(
            value.first.subject,
            observations,
            "one channel observation did not identify one correlated pair",
        )
    relevant = frozenset(
        item for item in observations if item.subject == value.first.subject
    )
    return IdentifiedPair(pairs[0].first, pairs[0].second, relevant)


@dataclass(frozen=True, slots=True)
class PartiallyIdentified:
    first: Trace
    second: ChannelFamily[Trace]
    evidence: frozenset[Observation]


type IndependentIdentification = (
    ProductFamily | PartiallyIdentified | EvidenceConflict | RejectedObservation
)


def identify_independent_first(
    value: ProductFamily,
    observations: frozenset[Observation],
) -> IndependentIdentification:
    result = identify(value.first, observations)
    if isinstance(result, ChannelFamily):
        return value
    if isinstance(result, (EvidenceConflict, RejectedObservation)):
        return result
    return PartiallyIdentified(result.value, value.second, result.evidence)
