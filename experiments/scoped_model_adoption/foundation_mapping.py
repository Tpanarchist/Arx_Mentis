"""Post-hoc foundation pressure mapping for scoped adoption."""

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
class AdoptionFinding:
    scoped_use_is_truth: bool
    contextual_roles_recur: bool
    snapshot_independence_recurs: bool
    adoption_is_cast: bool | None


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[Mapping, ...]
    finding: AdoptionFinding


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
                "Adoption",
                "Context-bound role or authority",
                MappingStatus.PRESSURE,
                "scoped relation",
            ),
            Mapping(
                "UseMode",
                "Reader or Interpreter role",
                MappingStatus.PRESSURE,
                "same model, distinct readings",
            ),
            Mapping(
                "DerivedPolicy",
                "operative Form",
                MappingStatus.PRESSURE,
                "source and authority lineage retained",
            ),
            Mapping(
                "Activation",
                "Cast or lifecycle operation",
                MappingStatus.UNMAPPED,
                "operation kind unresolved",
            ),
            Mapping(
                "TruthAssertion",
                "Proposition or commitment",
                MappingStatus.UNMAPPED,
                "execution relation unresolved",
            ),
            Mapping(
                "Scoped adoption as truth",
                None,
                MappingStatus.REJECTED,
                "instrumental use is not ontology",
            ),
        ),
        AdoptionFinding(
            scoped_use_is_truth=False,
            contextual_roles_recur=True,
            snapshot_independence_recurs=True,
            adoption_is_cast=None,
        ),
    )
