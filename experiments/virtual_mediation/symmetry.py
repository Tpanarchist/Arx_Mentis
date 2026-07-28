"""Cyclic symmetry and family mechanics for neutral mediation values."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace

from .source_model import (
    Channel,
    CriterionTruth,
    Mediator,
    Rotation,
    Signature,
    Trace,
)

CHANNELS = frozenset({Channel.ALPHA, Channel.BETA, Channel.GAMMA})
ROTATIONS = frozenset({Rotation.ZERO, Rotation.ONE, Rotation.TWO})


def rotate(channel: Channel, rotation: Rotation) -> Channel:
    ordered = (Channel.ALPHA, Channel.BETA, Channel.GAMMA)
    return ordered[(ordered.index(channel) + rotation.value) % len(ordered)]


def compose(first: Rotation, second: Rotation) -> Rotation:
    return Rotation((first.value + second.value) % 3)


def inverse(rotation: Rotation) -> Rotation:
    return Rotation((-rotation.value) % 3)


@dataclass(frozen=True, slots=True)
class CyclicActionReport:
    closed: bool
    identity_holds: bool
    composition_holds: bool
    inverses_hold: bool
    free: bool
    transitive: bool


def check_cyclic_action() -> CyclicActionReport:
    closed = all(
        rotate(channel, rotation) in CHANNELS
        for channel in CHANNELS
        for rotation in ROTATIONS
    )
    identity_holds = all(
        rotate(channel, Rotation.ZERO) is channel for channel in CHANNELS
    )
    composition_holds = all(
        rotate(rotate(channel, first), second)
        == rotate(
            channel,
            compose(first, second),
        )
        for channel in CHANNELS
        for first in ROTATIONS
        for second in ROTATIONS
    )
    inverses_hold = all(
        rotate(rotate(channel, rotation), inverse(rotation)) is channel
        for channel in CHANNELS
        for rotation in ROTATIONS
    )
    free = all(
        rotation is Rotation.ZERO
        or all(rotate(channel, rotation) is not channel for channel in CHANNELS)
        for rotation in ROTATIONS
    )
    transitive = all(
        any(rotate(source, rotation) is target for rotation in ROTATIONS)
        for source in CHANNELS
        for target in CHANNELS
    )
    return CyclicActionReport(
        closed,
        identity_holds,
        composition_holds,
        inverses_hold,
        free,
        transitive,
    )


@dataclass(frozen=True, slots=True)
class Assignment[T]:
    coordinate: Channel
    value: T


@dataclass(frozen=True, slots=True)
class EquivarianceReport:
    name: str
    holds: bool
    checked_pairs: int


@dataclass(frozen=True, slots=True)
class ChannelFamily[T]:
    subject: str
    assignments: frozenset[Assignment[T]]
    law: EquivarianceReport


def at[T](family: ChannelFamily[T], coordinate: Channel) -> T:
    matches = tuple(
        assignment.value
        for assignment in family.assignments
        if assignment.coordinate is coordinate
    )
    if len(matches) != 1:
        raise ValueError("a channel family must have exactly one value per coordinate")
    return matches[0]


def image[T](family: ChannelFamily[T]) -> frozenset[T]:
    return frozenset(assignment.value for assignment in family.assignments)


def build_family[T](
    subject: str,
    build: Callable[[Channel], T],
    transform: Callable[[T, Rotation], T],
    law_name: str,
) -> ChannelFamily[T]:
    assignments = frozenset(Assignment(channel, build(channel)) for channel in CHANNELS)
    provisional = ChannelFamily(
        subject,
        assignments,
        EquivarianceReport(law_name, False, 0),
    )
    holds = all(
        transform(at(provisional, channel), rotation)
        == at(provisional, rotate(channel, rotation))
        for channel in CHANNELS
        for rotation in ROTATIONS
    )
    law = EquivarianceReport(law_name, holds, len(CHANNELS) * len(ROTATIONS))
    return replace(provisional, law=law)


def map_family[T, U](
    family: ChannelFamily[T],
    transform_value: Callable[[T], U],
    rotate_value: Callable[[U, Rotation], U],
    law_name: str,
) -> ChannelFamily[U]:
    return build_family(
        family.subject,
        lambda channel: transform_value(at(family, channel)),
        rotate_value,
        law_name,
    )


def rotate_trace(trace: Trace, rotation: Rotation) -> Trace:
    channel = rotate(trace.mediator.channel, rotation)
    sources = trace.provenance.sources
    return replace(
        trace,
        mediator=Mediator(
            channel,
            trace.mediator.directly_observed,
        ),
        provenance=replace(
            trace.provenance,
            sources=(sources[0], channel.value, *sources[2:]),
        ),
    )


def rotate_signature(signature: Signature, rotation: Rotation) -> Signature:
    channel = rotate(signature.channel, rotation)
    return replace(signature, channel=channel, marker=f"signature-{channel.value}")


def rotate_truth(truth: CriterionTruth, rotation: Rotation) -> CriterionTruth:
    channel = rotate(truth.channel, rotation)
    return CriterionTruth(channel, channel is Channel.ALPHA)


@dataclass(frozen=True, slots=True)
class DefaultReport:
    candidate: Channel
    fixed_by_all_rotations: bool
    legitimate: bool
    reason: str


def assess_default(candidate: Channel) -> DefaultReport:
    fixed = all(rotate(candidate, rotation) is candidate for rotation in ROTATIONS)
    return DefaultReport(
        candidate,
        fixed,
        fixed,
        "a channel is legitimate only if every declared rotation fixes it",
    )


@dataclass(frozen=True, slots=True)
class ListedChoice:
    candidate: Channel
    legitimate: bool
    reason: str


def choose_listed_first(channels: tuple[Channel, ...]) -> ListedChoice:
    return ListedChoice(
        channels[0],
        False,
        "sequence position is representation-dependent and not symmetry-respecting",
    )
