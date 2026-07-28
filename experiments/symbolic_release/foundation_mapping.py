"""Post-hoc foundation comparison for neutral symbolic release."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MappingStatus(Enum):
    CANDIDATE = "candidate"
    PRESSURE = "pressure"
    REJECTED = "rejected"
    UNMAPPED = "unmapped"


@dataclass(frozen=True, slots=True)
class RoleMapping:
    neutral_term: str
    provisional_reading: str
    status: MappingStatus
    reason: str


@dataclass(frozen=True, slots=True)
class ReleaseFinding:
    representation_self_interprets: bool
    operational_sufficiency_implies_semantic_completeness: bool
    release_erases_provenance: bool
    same_local_value_implies_same_derivation: bool
    conclusion: str


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[RoleMapping, ...]
    finding: ReleaseFinding
    open_questions: tuple[str, ...]


def attempt_mapping() -> MappingReport:
    return MappingReport(
        (
            RoleMapping(
                "SourceForm and Carrier",
                "distinct Form candidates",
                MappingStatus.PRESSURE,
                (
                    "a carrier may preserve less information and take a role only "
                    "when read"
                ),
            ),
            RoleMapping(
                "Decoder and InterpretationKey",
                "Reader or Interpreter candidates",
                MappingStatus.PRESSURE,
                "one carrier supports different lawful readings without nominal role",
            ),
            RoleMapping(
                "CompiledPolicy",
                "constructed operative Form candidate",
                MappingStatus.CANDIDATE,
                (
                    "it is sufficient for selected actions but cannot reconstruct "
                    "its source"
                ),
            ),
            RoleMapping(
                "Activation",
                "Cast candidate",
                MappingStatus.UNMAPPED,
                (
                    "activation and execution are distinct here, so Cast identity "
                    "is unclear"
                ),
            ),
            RoleMapping(
                "Outcome",
                "Effect candidate",
                MappingStatus.PRESSURE,
                "equal outcomes do not identify policy, decoding, or derivation",
            ),
            RoleMapping(
                "Provenance",
                "Demonstration, source map, or history candidate",
                MappingStatus.UNMAPPED,
                (
                    "historical derivation survives source unavailability without "
                    "proving acceptance"
                ),
            ),
        ),
        ReleaseFinding(
            representation_self_interprets=False,
            operational_sufficiency_implies_semantic_completeness=False,
            release_erases_provenance=False,
            same_local_value_implies_same_derivation=False,
            conclusion=(
                "a symbol does not interpret or execute itself; lawful decoding, "
                "activation, execution, and provenance remain separately observable"
            ),
        ),
        (
            "Is a Spell nominal or a Form read operatively?",
            "Is encoding a construction, and is compilation or execution a Cast?",
            "Is release a lifecycle transition or removal of a dependency?",
            "Does provenance belong to an artifact or an append-only history?",
            (
                "Can historical origin participate in equality without replacing "
                "local value?"
            ),
            "Is activation a general semantic operation or domain machinery?",
        ),
    )
