"""Named source forms and world state for the symbolic-release witnesses."""

from __future__ import annotations

from .source import SourceForm, WorldState


def navigation_source(identifier: str = "source-safe") -> SourceForm:
    return SourceForm(
        identifier,
        ("safe-a-c", "safe-c-d"),
        destination="D",
        minimum_resources=2,
        explanation="reach D while avoiding unsafe edges",
    )


def fast_source(identifier: str = "source-fast") -> SourceForm:
    return SourceForm(
        identifier,
        ("fast-a-d",),
        destination="D",
        minimum_resources=2,
        explanation="reach D by the shortest available route",
    )


def initial_world() -> WorldState:
    return WorldState("A", resources=3)
