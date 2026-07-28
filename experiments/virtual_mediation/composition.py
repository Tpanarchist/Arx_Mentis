"""Correlation-preserving composition and an adversarial option-bag model."""

from __future__ import annotations

from dataclasses import dataclass

from .source_model import Channel, Rotation, Trace
from .symmetry import (
    CHANNELS,
    ChannelFamily,
    at,
    build_family,
    rotate,
    rotate_trace,
)


@dataclass(frozen=True, slots=True)
class JointTrace:
    first: Trace
    second: Trace


def pair_channels(pair: JointTrace) -> tuple[Channel, Channel]:
    return pair.first.mediator.channel, pair.second.mediator.channel


def rotate_joint(value: JointTrace, rotation: Rotation) -> JointTrace:
    return JointTrace(
        rotate_trace(value.first, rotation),
        rotate_trace(value.second, rotation),
    )


@dataclass(frozen=True, slots=True)
class CorrelatedMediations:
    relation: str
    first: ChannelFamily[Trace]
    second: ChannelFamily[Trace]
    joint: ChannelFamily[JointTrace]


def shared(
    first: ChannelFamily[Trace],
    second: ChannelFamily[Trace],
) -> CorrelatedMediations:
    joint = build_family(
        f"shared:{first.subject}:{second.subject}",
        lambda channel: JointTrace(at(first, channel), at(second, channel)),
        rotate_joint,
        "both mediated interactions rotate through one shared channel coordinate",
    )
    return CorrelatedMediations("shared", first, second, joint)


def twisted(
    first: ChannelFamily[Trace],
    second: ChannelFamily[Trace],
) -> CorrelatedMediations:
    joint = build_family(
        f"twisted:{first.subject}:{second.subject}",
        lambda channel: JointTrace(
            at(first, channel),
            at(second, rotate(channel, Rotation.ONE)),
        ),
        rotate_joint,
        "the second interaction stays one rotation ahead of the first",
    )
    return CorrelatedMediations("twisted-one-step", first, second, joint)


@dataclass(frozen=True, slots=True)
class PairCoordinate:
    first: Channel
    second: Channel


@dataclass(frozen=True, slots=True)
class ProductAssignment:
    coordinate: PairCoordinate
    value: JointTrace


@dataclass(frozen=True, slots=True)
class ProductFamily:
    subject: str
    first: ChannelFamily[Trace]
    second: ChannelFamily[Trace]
    assignments: frozenset[ProductAssignment]


def independent(
    first: ChannelFamily[Trace],
    second: ChannelFamily[Trace],
) -> ProductFamily:
    return ProductFamily(
        f"independent:{first.subject}:{second.subject}",
        first,
        second,
        frozenset(
            ProductAssignment(
                PairCoordinate(first_channel, second_channel),
                JointTrace(at(first, first_channel), at(second, second_channel)),
            )
            for first_channel in CHANNELS
            for second_channel in CHANNELS
        ),
    )


def correlated_image(
    value: CorrelatedMediations,
) -> frozenset[JointTrace]:
    return frozenset(assignment.value for assignment in value.joint.assignments)


def product_image(value: ProductFamily) -> frozenset[JointTrace]:
    return frozenset(assignment.value for assignment in value.assignments)


@dataclass(frozen=True, slots=True)
class OptionBag[T]:
    options: frozenset[T]


@dataclass(frozen=True, slots=True)
class LocalOptionView:
    first: OptionBag[Trace]
    second: OptionBag[Trace]


def forget_relationship(
    value: CorrelatedMediations | ProductFamily,
) -> LocalOptionView:
    if isinstance(value, CorrelatedMediations):
        pairs = correlated_image(value)
    else:
        pairs = product_image(value)
    return LocalOptionView(
        OptionBag(frozenset(pair.first for pair in pairs)),
        OptionBag(frozenset(pair.second for pair in pairs)),
    )
