"""Recorded evidence settles an equivariant family of symbolic cycle models.

This experiment intentionally shares no implementation types with Euclid I.1.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class Form:
    __slots__ = ()


class Verdict(Enum):
    HOLDS = "holds"
    DOES_NOT_HOLD = "does-not-hold"


@dataclass(frozen=True, slots=True)
class Occasion(Form):
    name: str


@dataclass(frozen=True, slots=True)
class ObservedState(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Observation(Form):
    occasion: Occasion
    state: ObservedState


@dataclass(frozen=True, slots=True)
class Prediction(Form):
    occasion: Occasion
    state: ObservedState


@dataclass(frozen=True, slots=True)
class CycleModel(Form):
    name: str
    predictions: frozenset[Prediction]


class Swap(Enum):
    IDENTITY = "identity"
    EXCHANGE = "exchange"


@dataclass(frozen=True, slots=True)
class ModelGroup(Form):
    elements: frozenset[Swap]


@dataclass(frozen=True, slots=True)
class Stabilizer(Form):
    group: ModelGroup
    prior: Observation
    elements: frozenset[Swap]


@dataclass(frozen=True, slots=True)
class ModelFrame(Form):
    token: Swap


@dataclass(frozen=True, slots=True)
class FamilyAssignment(Form):
    frame: ModelFrame
    value: Form


@dataclass(frozen=True, slots=True)
class EquivariantFamily(Form):
    stabilizer: Stabilizer
    graph: frozenset[FamilyAssignment]
    law: str


@dataclass(frozen=True, slots=True)
class EvidenceFrame(Form):
    state: ObservedState
    frame: ModelFrame


@dataclass(frozen=True, slots=True)
class ObservationSettlement(Form):
    occasion: Occasion
    witness_role: str
    evidence_frames: frozenset[EvidenceFrame]


@dataclass(frozen=True, slots=True)
class Potential(Form):
    family: EquivariantFamily
    settlement: ObservationSettlement


@dataclass(frozen=True, slots=True)
class SettlementEvidence(Form):
    observation: Observation
    frame: ModelFrame


@dataclass(frozen=True, slots=True)
class Point(Form):
    selected: Form
    evidence: SettlementEvidence


class Operation(Enum):
    COMPARE_PRIOR = "compare-prior"
    FORM_MODEL_FAMILY = "form-model-family"
    PROJECT_MODEL = "project-model"


@dataclass(frozen=True, slots=True)
class Capability(Form):
    operation: Operation


@dataclass(frozen=True, slots=True)
class ConstructionRule(Form):
    operation: Operation
    capability: Capability
    equivariant: Verdict


@dataclass(frozen=True, slots=True)
class Ars(Form):
    name: str
    group: ModelGroup
    constructions: frozenset[ConstructionRule]
    equality: str


@dataclass(frozen=True, slots=True)
class Instruction(Form):
    operation: Operation


@dataclass(frozen=True, slots=True)
class Will(Form):
    description: str


@dataclass(frozen=True, slots=True)
class Spell(Form):
    name: str
    steps: tuple[Instruction, ...]
    will: Will


@dataclass(frozen=True, slots=True)
class DiscriminationForm(Form):
    spell: Spell
    candidates: tuple[CycleModel, CycleModel]
    prior: Observation
    occasion: Occasion


@dataclass(frozen=True, slots=True)
class ProjectionForm(Form):
    spell: Spell
    occasion: Occasion


@dataclass(frozen=True, slots=True)
class ElaboratedSpell(Form):
    source: Spell
    rules: tuple[ConstructionRule, ...]
    derived_capabilities: frozenset[Capability]


@dataclass(frozen=True, slots=True)
class ElaborationRefusal(Form):
    source: Spell
    instruction: Instruction


type ElaborationResult = ElaboratedSpell | ElaborationRefusal


@dataclass(frozen=True, slots=True)
class Context(Form):
    ars: Ars
    observations: frozenset[Observation]
    capabilities: frozenset[Capability]


@dataclass(frozen=True, slots=True)
class SelectionEffect(Form):
    model: CycleModel
    will: Will
    evidence: SettlementEvidence


@dataclass(frozen=True, slots=True)
class ProjectionEffect(Form):
    prediction: Prediction
    will: Will
    source: Point


@dataclass(frozen=True, slots=True)
class Refused(Form):
    missing: Capability


class DiagnosticKind(Enum):
    MISSING_PRIOR = "missing-prior"
    PRIOR_DISAGREEMENT = "prior-disagreement"
    CONTRADICTORY_EVIDENCE = "contradictory-evidence"
    NO_MATCHING_MODEL = "no-matching-model"
    MISSING_PROJECTION = "missing-projection"


@dataclass(frozen=True, slots=True)
class ExperimentalDiagnostic(Form):
    kind: DiagnosticKind
    reason: str
    related: frozenset[Form] = frozenset()


type CastResult = Potential | Refused | ExperimentalDiagnostic
type SettlementResult = Potential | Point | ExperimentalDiagnostic
type ProjectionResult = Potential | ProjectionEffect | Refused | ExperimentalDiagnostic


COMPARE = Capability(Operation.COMPARE_PRIOR)
FORM_FAMILY = Capability(Operation.FORM_MODEL_FAMILY)
PROJECT = Capability(Operation.PROJECT_MODEL)
COMPARE_RULE = ConstructionRule(Operation.COMPARE_PRIOR, COMPARE, Verdict.HOLDS)
FAMILY_RULE = ConstructionRule(
    Operation.FORM_MODEL_FAMILY,
    FORM_FAMILY,
    Verdict.HOLDS,
)
PROJECT_RULE = ConstructionRule(Operation.PROJECT_MODEL, PROJECT, Verdict.HOLDS)


@dataclass(frozen=True, slots=True)
class Experiment(Form):
    discrimination: DiscriminationForm
    projection: ProjectionForm
    context: Context
    bright: Observation
    dark: Observation
    irrelevant: Observation


def _prediction(model: CycleModel, occasion: Occasion) -> Prediction | None:
    matches = tuple(item for item in model.predictions if item.occasion == occasion)
    return matches[0] if len(matches) == 1 else None


def make_experiment() -> Experiment:
    prior_time = Occasion("prior")
    discriminator = Occasion("discriminator")
    future = Occasion("future")
    irrelevant_time = Occasion("irrelevant")
    steady = ObservedState("steady")
    bright = ObservedState("bright")
    dark = ObservedState("dark")
    rising = ObservedState("rising")
    falling = ObservedState("falling")
    prior = Observation(prior_time, steady)
    dawn = CycleModel(
        "dawn model",
        frozenset(
            {
                Prediction(prior_time, steady),
                Prediction(discriminator, bright),
                Prediction(future, rising),
            }
        ),
    )
    dusk = CycleModel(
        "dusk model",
        frozenset(
            {
                Prediction(prior_time, steady),
                Prediction(discriminator, dark),
                Prediction(future, falling),
            }
        ),
    )
    discrimination_spell = Spell(
        "distinguish cycle models",
        (
            Instruction(Operation.COMPARE_PRIOR),
            Instruction(Operation.FORM_MODEL_FAMILY),
        ),
        Will("identify the model warranted by recorded evidence"),
    )
    projection_spell = Spell(
        "project cycle model",
        (Instruction(Operation.PROJECT_MODEL),),
        Will("produce the model's future prediction"),
    )
    ars = Ars(
        "Ars Astronomica",
        ModelGroup(frozenset({Swap.IDENTITY, Swap.EXCHANGE})),
        frozenset({COMPARE_RULE, FAMILY_RULE, PROJECT_RULE}),
        "models are equal when their declared predictions agree",
    )
    context = Context(
        ars,
        frozenset({prior}),
        frozenset({COMPARE, FORM_FAMILY, PROJECT}),
    )
    return Experiment(
        DiscriminationForm(
            discrimination_spell,
            (dawn, dusk),
            prior,
            discriminator,
        ),
        ProjectionForm(projection_spell, future),
        context,
        Observation(discriminator, bright),
        Observation(discriminator, dark),
        Observation(irrelevant_time, bright),
    )


def elaborate(spell: Spell, ars: Ars) -> ElaborationResult:
    rules = {rule.operation: rule for rule in ars.constructions}
    interpreted: tuple[ConstructionRule, ...] = ()
    for instruction in spell.steps:
        rule = rules.get(instruction.operation)
        if rule is None:
            return ElaborationRefusal(spell, instruction)
        interpreted = (*interpreted, rule)
    return ElaboratedSpell(
        spell,
        interpreted,
        frozenset(rule.capability for rule in interpreted),
    )


def _missing(
    spell: ElaboratedSpell,
    context: Context,
) -> Refused | None:
    missing = spell.derived_capabilities - context.capabilities
    return None if not missing else Refused(next(iter(missing)))


def image(potential: Potential) -> frozenset[Form]:
    return frozenset(item.value for item in potential.family.graph)


def cast(
    form: DiscriminationForm,
    elaborated: ElaboratedSpell,
    context: Context,
) -> CastResult:
    refusal = _missing(elaborated, context)
    if refusal is not None:
        return refusal
    if form.prior not in context.observations:
        return ExperimentalDiagnostic(
            DiagnosticKind.MISSING_PRIOR,
            "Context lacks the declared prior Observation",
            frozenset({form.prior}),
        )
    disagreeing = frozenset(
        model
        for model in form.candidates
        if _prediction(model, form.prior.occasion)
        != Prediction(form.prior.occasion, form.prior.state)
    )
    if disagreeing:
        return ExperimentalDiagnostic(
            DiagnosticKind.PRIOR_DISAGREEMENT,
            "a candidate does not explain the prior Observation",
            disagreeing,
        )
    stabilizer = Stabilizer(
        context.ars.group,
        form.prior,
        context.ars.group.elements,
    )
    frames = (ModelFrame(Swap.IDENTITY), ModelFrame(Swap.EXCHANGE))
    family = EquivariantFamily(
        stabilizer,
        frozenset(
            FamilyAssignment(frame, model)
            for frame, model in zip(frames, form.candidates, strict=True)
        ),
        "exchanging the model frame exchanges the candidate model",
    )
    evidence_frames = frozenset(
        EvidenceFrame(
            _prediction(item.value, form.occasion).state,
            item.frame,
        )
        for item in family.graph
        if isinstance(item.value, CycleModel)
        and _prediction(item.value, form.occasion) is not None
    )
    return Potential(
        family,
        ObservationSettlement(form.occasion, "Witness", evidence_frames),
    )


def with_observations(context: Context, *observations: Observation) -> Context:
    return replace(
        context,
        observations=context.observations | frozenset(observations),
    )


def settle(potential: Potential, context: Context) -> SettlementResult:
    relevant = frozenset(
        observation
        for observation in context.observations
        if observation.occasion == potential.settlement.occasion
    )
    if not relevant:
        return potential
    states = frozenset(observation.state for observation in relevant)
    if len(states) != 1:
        return ExperimentalDiagnostic(
            DiagnosticKind.CONTRADICTORY_EVIDENCE,
            "recorded Observations disagree",
            relevant,
        )
    observation = next(iter(relevant))
    matching_frames = tuple(
        item.frame
        for item in potential.settlement.evidence_frames
        if item.state == observation.state
    )
    if len(matching_frames) != 1:
        return ExperimentalDiagnostic(
            DiagnosticKind.NO_MATCHING_MODEL,
            "evidence does not select exactly one model frame",
            frozenset({observation}),
        )
    values = tuple(
        item.value
        for item in potential.family.graph
        if item.frame == matching_frames[0]
    )
    if len(values) != 1:
        return ExperimentalDiagnostic(
            DiagnosticKind.NO_MATCHING_MODEL,
            "the selected frame does not identify one family value",
            frozenset({observation}),
        )
    evidence = SettlementEvidence(observation, matching_frames[0])
    return Point(values[0], evidence)


def project(
    form: ProjectionForm,
    elaborated: ElaboratedSpell,
    source: Potential | Point,
    context: Context,
) -> ProjectionResult:
    refusal = _missing(elaborated, context)
    if refusal is not None:
        return refusal
    if isinstance(source, Potential):
        graph: set[FamilyAssignment] = set()
        for item in source.family.graph:
            if not isinstance(item.value, CycleModel):
                continue
            prediction = _prediction(item.value, form.occasion)
            if prediction is None:
                return ExperimentalDiagnostic(
                    DiagnosticKind.MISSING_PROJECTION,
                    "a model lacks the requested future prediction",
                    frozenset({item.value}),
                )
            graph.add(FamilyAssignment(item.frame, prediction))
        family = EquivariantFamily(
            source.family.stabilizer,
            frozenset(graph),
            "projection is applied uniformly throughout the model frame",
        )
        return Potential(family, source.settlement)
    if not isinstance(source.selected, CycleModel):
        return ExperimentalDiagnostic(
            DiagnosticKind.MISSING_PROJECTION,
            "the settled Point does not contain a cycle model",
            frozenset({source}),
        )
    prediction = _prediction(source.selected, form.occasion)
    if prediction is None:
        return ExperimentalDiagnostic(
            DiagnosticKind.MISSING_PROJECTION,
            "the selected model lacks the requested prediction",
            frozenset({source.selected}),
        )
    return ProjectionEffect(prediction, form.spell.will, source)
