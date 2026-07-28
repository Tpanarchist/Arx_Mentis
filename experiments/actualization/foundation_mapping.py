"""Post-hoc comparison of the neutral Actualization records with the foundation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MappingStatus(Enum):
    CANDIDATE = "candidate"
    PRESSURE = "pressure"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class RoleMapping:
    neutral_term: str
    provisional_reading: str
    status: MappingStatus
    reason: str


@dataclass(frozen=True, slots=True)
class ActualizationFinding:
    acceptance_and_guidance_distinct: bool
    one_target_can_derive_both: bool
    conformity_identifies_mechanism: bool
    direct_assignment_is_causal: bool
    conclusion: str


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[RoleMapping, ...]
    finding: ActualizationFinding
    open_questions: tuple[str, ...]


def attempt_mapping() -> MappingReport:
    return MappingReport(
        (
            RoleMapping(
                "TargetForm",
                "Form, Aim, or source from which roles are read",
                MappingStatus.PRESSURE,
                "one neutral record derives distinct acceptance and policy records",
            ),
            RoleMapping(
                "AcceptanceRule",
                "Will candidate",
                MappingStatus.CANDIDATE,
                "it evaluates an independently produced state but does not produce it",
            ),
            RoleMapping(
                "ActionPolicy and Controller",
                "construction-guidance candidates",
                MappingStatus.PRESSURE,
                "guidance changes transitions without changing the acceptance relation",
            ),
            RoleMapping(
                "Outcome and CausalTrace",
                "Effect and Demonstration or provenance candidates",
                MappingStatus.PRESSURE,
                "the same state can retain distinct, inspectable production histories",
            ),
            RoleMapping(
                "direct assignment",
                "construction candidate",
                MappingStatus.REJECTED,
                "copying the target into the world is circular and causally empty",
            ),
        ),
        ActualizationFinding(
            acceptance_and_guidance_distinct=True,
            one_target_can_derive_both=True,
            conformity_identifies_mechanism=False,
            direct_assignment_is_causal=False,
            conclusion=(
                "a TargetForm may be read into separate acceptance and guidance "
                "structures, but this does not decide whether foundation Will names "
                "the source, only the criterion, or another relation"
            ),
        ),
        (
            "Is Will only an acceptance criterion or also a source of guidance?",
            "Does Context or Reader determine which role is derived from a target?",
            "How are approximation and partial progress represented?",
            "When can a compiled policy outlive availability of its source target?",
            "What evidence justifies attributing an observed result to a mechanism?",
        ),
    )
