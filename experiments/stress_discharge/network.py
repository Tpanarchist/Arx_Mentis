"""The declared topology and capacity profile of the constrained network."""

from __future__ import annotations

from .source_model import (
    CapacityEntry,
    CapacityProfile,
    ConstrainedNetwork,
    Link,
    LinkKind,
    Site,
)


def default_network() -> ConstrainedNetwork:
    return ConstrainedNetwork(
        "three-site-network",
        (
            Link("a-b", Site.A, Site.B, 3, 2, 10, LinkKind.TRANSFER),
            Link("a-c", Site.A, Site.C, 2, 1, 8, LinkKind.TRANSFER),
            Link("b-out", Site.B, None, 2, 3, 9, LinkKind.RELEASE),
            Link("c-out", Site.C, None, 3, 3, 8, LinkKind.RELEASE),
            Link("b-c", Site.B, Site.C, 4, 1, 9, LinkKind.TRANSFER),
            Link("c-b", Site.C, Site.B, 4, 1, 9, LinkKind.TRANSFER),
            Link("c-void", Site.C, None, 2, 1, 99, LinkKind.DISSIPATE),
        ),
    )


def capacity_profile(network: ConstrainedNetwork) -> CapacityProfile:
    entries = tuple(
        CapacityEntry(link.identifier, link.capacity, link.kind)
        for link in network.links
    )
    return CapacityProfile(
        network.identifier,
        entries,
        sum(entry.capacity for entry in entries),
    )
