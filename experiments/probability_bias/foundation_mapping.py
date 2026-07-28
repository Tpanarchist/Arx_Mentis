"""Post-hoc foundation comparison for weighted finite production."""

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
class ProbabilityFinding:
    bias_is_command: bool
    sample_is_kernel: bool
    report_is_stream: bool
    probability_is_potential: bool
    ambiguity_resolved_by_order: bool
    conclusion: str


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[RoleMapping, ...]
    finding: ProbabilityFinding
    open_questions: tuple[str, ...]


def attempt_mapping() -> MappingReport:
    return MappingReport(
        (
            RoleMapping(
                "Kernel",
                "weighted production-law candidate",
                MappingStatus.UNMAPPED,
                "the foundation has no accepted probability or frequency category",
            ),
            RoleMapping(
                "Intervention",
                "Context change or construction candidate",
                MappingStatus.PRESSURE,
                "it transforms weights without commanding an event",
            ),
            RoleMapping(
                "Trial and EventStream",
                "produced event or Effect candidates",
                MappingStatus.PRESSURE,
                "samples remain separate from their production law",
            ),
            RoleMapping(
                "TrialPlan",
                "precommitted Form candidate",
                MappingStatus.PRESSURE,
                "it records target and collection policy without becoming mechanism",
            ),
            RoleMapping(
                "weighted Kernel",
                "Potential candidate",
                MappingStatus.REJECTED,
                "unequal mass has no declared transitive frame or settlement operation",
            ),
            RoleMapping(
                "InterventionConflict",
                "ambiguity or Refusal candidate",
                MappingStatus.CANDIDATE,
                "equal priority has no lawful discriminator or composition policy",
            ),
        ),
        ProbabilityFinding(
            bias_is_command=False,
            sample_is_kernel=False,
            report_is_stream=False,
            probability_is_potential=False,
            ambiguity_resolved_by_order=False,
            conclusion=(
                "bias changes exact weights without commanding an outcome; production, "
                "observation, reporting, acceptance, causation, and attribution remain "
                "separate"
            ),
        ),
        (
            "Does probability belong to an Ars, Context, type, or external model?",
            "How are exact, empirical, and inferred weights distinguished?",
            "Can interventions compose under an explicitly declared algebra?",
            "What relation connects precommitment, provenance, and causal validity?",
            "How does observer-relative mixture uncertainty relate to world state?",
            "Can acceptance consume distributions without becoming a production law?",
        ),
    )
