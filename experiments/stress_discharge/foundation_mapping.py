"""Post-hoc comparison of stress-discharge mechanics with the foundation."""

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
class StressFinding:
    stress_is_scalar: bool
    trigger_is_complete_cause: bool
    discharge_is_resolution: bool
    resolution_is_acceptance: bool
    capacity_is_symmetric_potential: bool
    conclusion: str


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[RoleMapping, ...]
    finding: StressFinding
    open_questions: tuple[str, ...]


def attempt_mapping() -> MappingReport:
    return MappingReport(
        (
            RoleMapping(
                "StressField",
                "distributed Context state candidate",
                MappingStatus.PRESSURE,
                "equal totals can cause different lawful discharge paths",
            ),
            RoleMapping(
                "Trigger",
                "condition or event candidate",
                MappingStatus.PRESSURE,
                "it initiates a mechanism but cannot replace its antecedents",
            ),
            RoleMapping(
                "Discharge and CausalTrace",
                "construction and provenance candidates",
                MappingStatus.UNMAPPED,
                "transfer, rupture, dissipation, and oscillation have different jobs",
            ),
            RoleMapping(
                "ResolutionRule and AcceptanceCriterion",
                "separate completion and Will candidates",
                MappingStatus.CANDIDATE,
                "a mechanically resolved state can remain externally unacceptable",
            ),
            RoleMapping(
                "CapacityProfile",
                "Potential candidate",
                MappingStatus.REJECTED,
                "capacity constrains paths but stores no symmetric candidate result",
            ),
            RoleMapping(
                "HistoricalResidue",
                "persistent provenance or Effect history candidate",
                MappingStatus.PRESSURE,
                "equal present fields need not erase rupture or loading history",
            ),
        ),
        StressFinding(
            stress_is_scalar=False,
            trigger_is_complete_cause=False,
            discharge_is_resolution=False,
            resolution_is_acceptance=False,
            capacity_is_symmetric_potential=False,
            conclusion=(
                "distributed stress discharges through declared causal mechanics; "
                "neither its path nor a desired result is encoded in advance"
            ),
        ),
        (
            "Does distributed state belong to Context, Effect, or another record?",
            "Is discharge one construction or a family of domain mechanisms?",
            "How do rupture and irreversible residue affect equality and identity?",
            "Can a trigger activate without becoming a nominal Cast?",
            "How are oscillatory and partially resolved processes represented?",
            "Does progress require a declared guidance or acceptance relation?",
        ),
    )
