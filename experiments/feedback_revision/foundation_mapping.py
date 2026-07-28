"""Post-hoc pressure mapping kept outside the neutral mechanics."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MappingStatus(Enum):
    PRESSURE = "pressure"
    UNMAPPED = "unmapped"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class Mapping:
    neutral_term: str
    possible_foundation_term: str | None
    status: MappingStatus
    reason: str


@dataclass(frozen=True, slots=True)
class RevisionFinding:
    prospective_not_retroactive: bool
    revision_is_cast: bool | None
    model_is_ars: bool | None
    assessment_is_demonstration: bool | None


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[Mapping, ...]
    finding: RevisionFinding


def attempt_mapping() -> MappingReport:
    return MappingReport(
        (
            Mapping(
                "Model",
                "Form or Ars-local theory",
                MappingStatus.UNMAPPED,
                "role unresolved",
            ),
            Mapping(
                "Prediction",
                "derived Form",
                MappingStatus.PRESSURE,
                "historically owned result",
            ),
            Mapping(
                "TrialPlan",
                "Context-bound plan",
                MappingStatus.PRESSURE,
                "precommitted boundary",
            ),
            Mapping(
                "Assessment",
                "acceptance or verification",
                MappingStatus.UNMAPPED,
                "ADR 0009 does not choose the relation",
            ),
            Mapping(
                "Revision",
                "construction of a new Form",
                MappingStatus.PRESSURE,
                "source remains available",
            ),
            Mapping(
                "ModelVersion",
                "historically owned Form",
                MappingStatus.UNMAPPED,
                "identity role unresolved",
            ),
            Mapping(
                "Replay",
                None,
                MappingStatus.UNMAPPED,
                "execution, interpretation, and simulation remain open",
            ),
            Mapping(
                "Model as world truth",
                None,
                MappingStatus.REJECTED,
                "working selection does not establish cause",
            ),
        ),
        RevisionFinding(
            prospective_not_retroactive=True,
            revision_is_cast=None,
            model_is_ars=None,
            assessment_is_demonstration=None,
        ),
    )
