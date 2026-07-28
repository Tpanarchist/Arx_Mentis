"""Post-hoc foundation comparison for the hostile attribution experiment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .attribution import AttributionReport
from .source_model import Correspondence, ObservedEvent, WorldEvent
from .symmetry_attempt import SymmetryAttempt


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
class WorldKnowledgeSplit:
    world_cause_definite: bool
    cause_available_to_observer: bool
    attribution_underdetermined: bool
    outcome_occurred: bool
    correspondence_established: bool
    causal_explanation_verified: bool
    conclusion: str


@dataclass(frozen=True, slots=True)
class ScopeBoundary:
    symmetric_construction_law_retained: bool
    universal_unresolved_algebra_rejected: bool
    candidate_scope: str


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[RoleMapping, ...]
    split: WorldKnowledgeSplit
    boundary: ScopeBoundary
    open_questions: tuple[str, ...]


def attempt_mapping(
    world_event: WorldEvent,
    observed: ObservedEvent,
    correspondence: Correspondence,
    attribution: AttributionReport,
    symmetry: SymmetryAttempt,
) -> MappingReport:
    mappings = (
        RoleMapping(
            "RecordedAim",
            "Form, criterion, or Will candidate",
            MappingStatus.PRESSURE,
            "a recorded desired feature is not by itself executable construction",
        ),
        RoleMapping(
            "Event",
            "settled occurrence or Effect candidate",
            MappingStatus.CANDIDATE,
            "occurrence does not imply correspondence, surprise, or causation",
        ),
        RoleMapping(
            "Correspondence",
            "qualified relation candidate",
            MappingStatus.CANDIDATE,
            "the relation follows a declared MatchRule without causal attribution",
        ),
        RoleMapping(
            "AttributionReport",
            "epistemic uncertainty candidate, not symmetric Potential",
            MappingStatus.REJECTED,
            "the hypotheses occupy unequal structural orbits",
        ),
    )
    split = WorldKnowledgeSplit(
        world_cause_definite=world_event.definite_cause is not None,
        cause_available_to_observer=observed.cause_available,
        attribution_underdetermined=attribution.underdetermined,
        outcome_occurred=observed.event.occurred_order >= 0,
        correspondence_established=correspondence.matches,
        causal_explanation_verified=not attribution.underdetermined,
        conclusion=(
            "the event occurred and corresponded while its definite world cause "
            "remains unavailable and the causal explanation remains unverified"
        ),
    )
    boundary = ScopeBoundary(
        symmetric_construction_law_retained=True,
        universal_unresolved_algebra_rejected=(
            not symmetry.proposed_cycle_preserves_structure
            and not symmetry.lawful_relation_transitive
        ),
        candidate_scope=(
            "unresolved constructions related by a declared symmetry must preserve "
            "equivariance, correlation, invariant descent, evidence conditions, and "
            "historical persistence"
        ),
    )
    return MappingReport(
        mappings,
        split,
        boundary,
        (
            "Does epistemic uncertainty require weights or only ordered support?",
            "When does evidence narrow hypotheses without selecting one?",
            "Is world state distinct from Reader-relative knowledge state?",
            "Which unresolved searches lack both probability and symmetry?",
            "May one result carry settled occurrence and unresolved attribution?",
            (
                f"Does correspondence={correspondence.matches} belong to the event, "
                "observer, or their relation?"
            ),
        ),
    )
