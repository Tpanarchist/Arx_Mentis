"""Provisional correspondence attempted only after neutral mechanics execute."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .mediation import MediationRecord, VariableAssessment
from .source_model import Accepted


class MappingStatus(Enum):
    CANDIDATE = "candidate"
    PRESSURE = "pressure"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class RoleMapping:
    neutral_term: str
    provisional_reading: str
    status: MappingStatus
    friction: str


@dataclass(frozen=True, slots=True)
class VirtualityDimensions:
    operationally_definite_per_coordinate: bool
    mediator_directly_observed: bool
    locating_coordinate_unresolved: bool
    explanation: str


@dataclass(frozen=True, slots=True)
class DualResultPressure:
    public_outcome_settled: bool
    internal_mediation_unresolved: bool
    retained_together: bool
    pressure: str


@dataclass(frozen=True, slots=True)
class MappingReport:
    mappings: tuple[RoleMapping, ...]
    virtuality: VirtualityDimensions
    result_shape: DualResultPressure
    open_questions: tuple[str, ...]


def attempt_mapping(
    record: MediationRecord,
    assessment: Accepted | VariableAssessment,
) -> MappingReport:
    """Describe possible foundation roles without changing the neutral record."""

    mappings = (
        RoleMapping(
            "interaction specification",
            "Form or nominal Spell candidate",
            MappingStatus.UNRESOLVED,
            "the neutral mechanics do not need to choose nominal or contextual role",
        ),
        RoleMapping(
            "intervention",
            "construction input candidate",
            MappingStatus.CANDIDATE,
            "it begins work but does not itself describe the produced result",
        ),
        RoleMapping(
            "mediation trace family",
            "Potential candidate",
            MappingStatus.CANDIDATE,
            "the channel coordinate is unresolved while each indexed trace is definite",
        ),
        RoleMapping(
            "endpoint outcome",
            "Effect candidate",
            MappingStatus.PRESSURE,
            "a settled public outcome coexists with unresolved internal mediation",
        ),
        RoleMapping(
            "signature observation",
            "settlement evidence or Witness contribution candidate",
            MappingStatus.UNRESOLVED,
            "the evidence informs the mechanism without changing the endpoint outcome",
        ),
        RoleMapping(
            "acceptance criterion",
            "Will candidate",
            MappingStatus.CANDIDATE,
            (
                "invariant and channel-specific criteria have different "
                "pre-observation shapes"
            ),
        ),
        RoleMapping(
            "Denied",
            "Refusal candidate",
            MappingStatus.CANDIDATE,
            "permission is absent before mediation work begins",
        ),
        RoleMapping(
            "Breakdown",
            "Failure candidate",
            MappingStatus.CANDIDATE,
            "permitted mediation begins but cannot complete",
        ),
    )
    virtuality = VirtualityDimensions(
        operationally_definite_per_coordinate=all(
            assignment.value.mediator.channel is assignment.coordinate
            for assignment in record.traces.assignments
        ),
        mediator_directly_observed=any(
            assignment.value.mediator.directly_observed
            for assignment in record.traces.assignments
        ),
        locating_coordinate_unresolved=True,
        explanation=(
            "direct observability and unresolved channel location are independent axes"
        ),
    )
    result_shape = DualResultPressure(
        public_outcome_settled=record.outcome.reached,
        internal_mediation_unresolved=len(record.traces.assignments) == 3,
        retained_together=True,
        pressure=(
            "one construction may need to retain a settled public outcome and an "
            "unresolved internal family"
        ),
    )
    return MappingReport(
        mappings,
        virtuality,
        result_shape,
        (
            "Is intervention nominal instruction or a generic Form read for execution?",
            "Is the trace itself an Effect, or only the endpoint outcome?",
            (
                "Does identifying a channel add knowledge without changing prior "
                "semantics?"
            ),
            "May invariant aggregation be exposed while its source family is retained?",
            "Is visibility a separate type dimension from settlement phase?",
            "Is signature evidence about the mechanism, outcome, or their relation?",
            "Can provenance be definite while the represented mediator is unresolved?",
            (
                f"How should {type(assessment).__name__} participate in continuation "
                "typing?"
            ),
        ),
    )
