"""Euclid I.1 as capability discovery and equivariant construction.

This disposable experiment derives capabilities by elaborating steps against an Ars,
then lifts construction uniformly through a reflection torsor. No representation in
this module is an accepted Arx Mentis language type.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from enum import Enum
from itertools import product


class Form:
    __slots__ = ()


class Verdict(Enum):
    HOLDS = "holds"
    DOES_NOT_HOLD = "does-not-hold"


class Parity(Enum):
    IDENTITY = "identity"
    FLIPPED = "flipped"


@dataclass(frozen=True, slots=True)
class TransformationGroup(Form):
    name: str
    elements: frozenset[Parity]


@dataclass(frozen=True, slots=True)
class Location(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Occurrence(Form):
    name: str


@dataclass(frozen=True, slots=True)
class GivenEvidence(Form):
    description: str


@dataclass(frozen=True, slots=True)
class SettlementEvidence(Form):
    witnesses: frozenset[FrameWitness]


@dataclass(frozen=True, slots=True)
class Point(Form):
    """The settled phase of a distinction."""

    selected: Form
    evidence: Form
    occurrence: Occurrence


@dataclass(frozen=True, slots=True)
class Line(Form):
    first: Point
    second: Point
    occurrence: Occurrence


@dataclass(frozen=True, slots=True)
class Circle(Form):
    center: Point
    through: Point
    occurrence: Occurrence


@dataclass(frozen=True, slots=True)
class GivenConfiguration(Form):
    point_a: Point
    point_b: Point
    base: Line


@dataclass(frozen=True, slots=True)
class Stabilizer(Form):
    ambient_group: TransformationGroup
    givens: GivenConfiguration
    elements: frozenset[Parity]


@dataclass(frozen=True, slots=True)
class FrameKey(Form):
    name: str
    stabilizer: Stabilizer


@dataclass(frozen=True, slots=True)
class FrameCoordinate(Form):
    key: FrameKey
    parity: Parity


@dataclass(frozen=True, slots=True)
class Frame(Form):
    coordinates: frozenset[FrameCoordinate]


@dataclass(frozen=True, slots=True)
class EquivarianceLaw(Form):
    construction: str
    statement: str
    verified: Verdict


@dataclass(frozen=True, slots=True)
class FrameTorsor(Form):
    keys: frozenset[FrameKey]
    frames: frozenset[Frame]
    action: EquivarianceLaw


@dataclass(frozen=True, slots=True)
class FamilyValue(Form):
    frame: Frame
    value: Form


@dataclass(frozen=True, slots=True)
class EquivariantFamily(Form):
    torsor: FrameTorsor
    graph: frozenset[FamilyValue]
    law: EquivarianceLaw


@dataclass(frozen=True, slots=True)
class SettlementRule(Form):
    witness_role: str
    evidence_description: str


@dataclass(frozen=True, slots=True)
class Potential(Form):
    """A lawful result varying with an unsettled frame."""

    family: EquivariantFamily
    settlement: SettlementRule


@dataclass(frozen=True, slots=True)
class FrameWitness(Form):
    coordinate: FrameCoordinate
    source: str


@dataclass(frozen=True, slots=True)
class Intersection(Form):
    circles: frozenset[Circle]
    parity: Parity


@dataclass(frozen=True, slots=True)
class CandidateLine(Form):
    fixed: Point
    apex: Intersection
    name: str


@dataclass(frozen=True, slots=True)
class Triangle(Form):
    base: Line
    apex: Intersection
    sides: frozenset[CandidateLine]


@dataclass(frozen=True, slots=True)
class Pair(Form):
    first: Form
    second: Form


@dataclass(frozen=True, slots=True)
class ProductValue(Form):
    values: tuple[Form, ...]


class Operation(Enum):
    CONSTRUCT_CIRCLE = "construct-circle"
    INTERSECT_CIRCLES = "intersect-circles"
    CONSTRUCT_LINE = "construct-line"
    CONSTRUCT_MIDPOINT = "construct-midpoint"


@dataclass(frozen=True, slots=True)
class Instruction(Form):
    operation: Operation
    bind: str
    arguments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Capability(Form):
    operation: Operation


@dataclass(frozen=True, slots=True)
class ConstructionRule(Form):
    operation: Operation
    postulate: str
    capability: Capability
    equivariance: EquivarianceLaw


@dataclass(frozen=True, slots=True)
class EqualityDeclaration(Form):
    ars_name: str
    subject: str
    reflexive: bool
    symmetric: bool
    transitive: bool


class WillPredicate(Enum):
    EQUILATERAL_ON_BASE = "equilateral-on-base"
    APEX_POSITIVE = "apex-positive"


@dataclass(frozen=True, slots=True)
class WillFragment(Form):
    predicates: frozenset[WillPredicate]
    termination_scope: str


@dataclass(frozen=True, slots=True)
class Bridge(Form):
    name: str
    source_ars: str
    target_ars: str
    translation: str
    preserves_equality: Verdict
    commutes_with_constructions: Verdict
    equivariant: Verdict


@dataclass(frozen=True, slots=True)
class Ars(Form):
    name: str
    forms: frozenset[str]
    constructions: frozenset[ConstructionRule]
    equality: EqualityDeclaration
    transformation_group: TransformationGroup
    will_fragment: WillFragment
    bridges: frozenset[Bridge]


@dataclass(frozen=True, slots=True)
class Will(Form):
    name: str
    predicate: WillPredicate
    base: Line


@dataclass(frozen=True, slots=True)
class Spell(Form):
    """Only stated inputs, steps, and Will; requirements are never authored here."""

    name: str
    inputs: tuple[str, ...]
    steps: tuple[Instruction, ...]
    will: Will


@dataclass(frozen=True, slots=True)
class ElaboratedStep(Form):
    instruction: Instruction
    rule: ConstructionRule


@dataclass(frozen=True, slots=True)
class ElaboratedSpell(Form):
    source: Spell
    steps: tuple[ElaboratedStep, ...]
    derived_requirements: frozenset[Capability]


@dataclass(frozen=True, slots=True)
class ElaborationRefusal(Form):
    source: Spell
    step: Instruction
    elaborated_prefix: tuple[ElaboratedStep, ...]
    missing_operation: Operation


type ElaborationResult = ElaboratedSpell | ElaborationRefusal


@dataclass(frozen=True, slots=True)
class Interpreter(Form):
    name: str


@dataclass(frozen=True, slots=True)
class NamedForm(Form):
    name: str
    form: Form


@dataclass(frozen=True, slots=True)
class Context(Form):
    bindings: frozenset[NamedForm]
    capabilities: frozenset[Capability]
    frame_witnesses: frozenset[FrameWitness]
    interpreter: Interpreter
    ars: Ars


@dataclass(frozen=True, slots=True)
class TraceEntry(Form):
    step: ElaboratedStep
    produced: Form


@dataclass(frozen=True, slots=True)
class Effect(Form):
    form: Potential | Triangle
    source: Line


@dataclass(frozen=True, slots=True)
class Produced(Form):
    effect: Effect
    trace: tuple[TraceEntry, ...]


@dataclass(frozen=True, slots=True)
class Refused(Form):
    missing: Capability
    step: ElaboratedStep
    trace: tuple[TraceEntry, ...]


@dataclass(frozen=True, slots=True)
class Failed(Form):
    reason: str
    step: ElaboratedStep | None
    trace: tuple[TraceEntry, ...]


type CastResult = Produced | Refused | Failed
type SettlementResult = Potential | Point | Failed


@dataclass(frozen=True, slots=True)
class Length(Form):
    source: Line | CandidateLine


@dataclass(frozen=True, slots=True)
class QualifiedEqual(Form):
    ars_name: str
    left: Length
    right: Length
    law: EqualityDeclaration


@dataclass(frozen=True, slots=True)
class BranchProof(Form):
    triangle: Triangle
    equalities: tuple[QualifiedEqual, QualifiedEqual, QualifiedEqual]


@dataclass(frozen=True, slots=True)
class InvariantDemonstration(Form):
    proofs: frozenset[BranchProof]
    bridge: Bridge
    constant_truth: Verdict


@dataclass(frozen=True, slots=True)
class Conforms(Form):
    will: Will
    effect: Effect
    evidence: InvariantDemonstration


@dataclass(frozen=True, slots=True)
class Counterexample(Form):
    will: Will
    effect: Effect
    witness: Form


@dataclass(frozen=True, slots=True)
class FrameDependentCheck(Form):
    will: Will
    effect: Effect
    family: Potential


type CheckResult = Conforms | Counterexample | FrameDependentCheck


@dataclass(frozen=True, slots=True)
class InvariantWill(Form):
    will: Will
    stabilizer: Stabilizer


@dataclass(frozen=True, slots=True)
class NonInvariantWill(Form):
    will: Will
    stabilizer: Stabilizer
    reason: str


type WillValidation = InvariantWill | NonInvariantWill


@dataclass(frozen=True, slots=True)
class Truth(Form):
    verdict: Verdict


class CandidateKind(Enum):
    POSITIVE_INTERSECTION = "positive-intersection"
    MIDPOINT = "midpoint"


@dataclass(frozen=True, slots=True)
class DefaultAssessment(Form):
    candidate: CandidateKind
    fixed_by_stabilizer: Verdict
    constructible: Verdict
    legitimate_default: Verdict
    equivariance_hypothesis: Verdict


class GroupDiagnostic(Enum):
    INFORMATIVE = "informative"
    TRIVIAL_ACTION = "trivial-action"


@dataclass(frozen=True, slots=True)
class GroupAssessment(Form):
    stabilizer: Stabilizer
    diagnostic: GroupDiagnostic


class FramePlacement(Enum):
    LINE = "line"
    CONTEXT = "context"
    POTENTIAL = "potential-frame"


class Side(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


@dataclass(frozen=True, slots=True)
class FramePlacementReport(Form):
    original: Side
    direction_flipped: Side
    chirality_flipped: Side
    both_flipped: Side
    direct_joint_outcomes: int
    twisted_joint_outcomes: int
    independent_joint_outcomes: int
    favored: FramePlacement
    reason: str


GEOMETRIC_GROUP = TransformationGroup(
    "Euclidean isometries including reflection",
    frozenset({Parity.IDENTITY, Parity.FLIPPED}),
)
GEOMETRIC_EQUALITY = EqualityDeclaration(
    "Ars Geometrica",
    "geometric congruence under the declared transformation group",
    True,
    True,
    True,
)
ARITHMETIC_EQUALITY = EqualityDeclaration(
    "Ars Arithmetica",
    "equality of magnitudes",
    True,
    True,
    True,
)
LENGTH_BRIDGE = Bridge(
    "geometric length",
    "Ars Geometrica",
    "Ars Arithmetica",
    "length(Line)",
    Verdict.HOLDS,
    Verdict.HOLDS,
    Verdict.HOLDS,
)
CIRCLE_CAPABILITY = Capability(Operation.CONSTRUCT_CIRCLE)
INTERSECTION_CAPABILITY = Capability(Operation.INTERSECT_CIRCLES)
LINE_CAPABILITY = Capability(Operation.CONSTRUCT_LINE)
MIDPOINT_CAPABILITY = Capability(Operation.CONSTRUCT_MIDPOINT)


def _equivariance(operation: Operation) -> EquivarianceLaw:
    return EquivarianceLaw(
        operation.value,
        "transform then construct equals construct then transform",
        Verdict.HOLDS,
    )


CIRCLE_RULE = ConstructionRule(
    Operation.CONSTRUCT_CIRCLE,
    "circle from center through a Point",
    CIRCLE_CAPABILITY,
    _equivariance(Operation.CONSTRUCT_CIRCLE),
)
INTERSECTION_RULE = ConstructionRule(
    Operation.INTERSECT_CIRCLES,
    "explicit circle-circle intersection or continuity postulate",
    INTERSECTION_CAPABILITY,
    _equivariance(Operation.INTERSECT_CIRCLES),
)
LINE_RULE = ConstructionRule(
    Operation.CONSTRUCT_LINE,
    "Line between two distinct Points",
    LINE_CAPABILITY,
    _equivariance(Operation.CONSTRUCT_LINE),
)
MIDPOINT_RULE = ConstructionRule(
    Operation.CONSTRUCT_MIDPOINT,
    "midpoint construction",
    MIDPOINT_CAPABILITY,
    _equivariance(Operation.CONSTRUCT_MIDPOINT),
)


@dataclass(frozen=True, slots=True)
class Experiment(Form):
    spell: Spell
    initial_ars: Ars
    extended_ars: Ars
    context: Context
    givens: GivenConfiguration


def _point(name: str, *, location: str | None = None) -> Point:
    return Point(
        Location(name if location is None else location),
        GivenEvidence("given by Proposition I.1"),
        Occurrence(name),
    )


def make_experiment(*, degenerate: bool = False) -> Experiment:
    point_a = _point("A")
    point_b = _point("B", location="A" if degenerate else "B")
    base = Line(point_a, point_b, Occurrence("AB"))
    givens = GivenConfiguration(point_a, point_b, base)
    will = Will(
        "equilateral triangle on AB",
        WillPredicate.EQUILATERAL_ON_BASE,
        base,
    )
    spell = Spell(
        "Euclid I.1",
        ("A", "B", "AB"),
        (
            Instruction(Operation.CONSTRUCT_CIRCLE, "circle_A", ("A", "B")),
            Instruction(Operation.CONSTRUCT_CIRCLE, "circle_B", ("B", "A")),
            Instruction(
                Operation.INTERSECT_CIRCLES,
                "C",
                ("circle_A", "circle_B"),
            ),
            Instruction(Operation.CONSTRUCT_LINE, "AC", ("A", "C")),
            Instruction(Operation.CONSTRUCT_LINE, "BC", ("B", "C")),
        ),
        will,
    )
    fragment = WillFragment(
        frozenset({WillPredicate.EQUILATERAL_ON_BASE, WillPredicate.APEX_POSITIVE}),
        "finite symbolic predicates declared by this experiment",
    )
    initial_ars = Ars(
        "Ars Geometrica",
        frozenset({"Point", "Line", "Circle", "Triangle"}),
        frozenset({CIRCLE_RULE, LINE_RULE}),
        GEOMETRIC_EQUALITY,
        GEOMETRIC_GROUP,
        fragment,
        frozenset({LENGTH_BRIDGE}),
    )
    extended_ars = replace(
        initial_ars,
        constructions=initial_ars.constructions | {INTERSECTION_RULE},
    )
    context = Context(
        frozenset(
            {
                NamedForm("A", point_a),
                NamedForm("B", point_b),
                NamedForm("AB", base),
            }
        ),
        frozenset({CIRCLE_CAPABILITY, INTERSECTION_CAPABILITY, LINE_CAPABILITY}),
        frozenset(),
        Interpreter("Euclid experiment interpreter"),
        extended_ars,
    )
    return Experiment(spell, initial_ars, extended_ars, context, givens)


def elaborate(spell: Spell, ars: Ars) -> ElaborationResult:
    """Discover requirements from steps and the current Ars."""

    by_operation = {rule.operation: rule for rule in ars.constructions}
    prefix: tuple[ElaboratedStep, ...] = ()
    for instruction in spell.steps:
        rule = by_operation.get(instruction.operation)
        if rule is None:
            return ElaborationRefusal(
                spell,
                instruction,
                prefix,
                instruction.operation,
            )
        prefix = (*prefix, ElaboratedStep(instruction, rule))
    return ElaboratedSpell(
        spell,
        prefix,
        frozenset(step.rule.capability for step in prefix),
    )


def derive_stabilizer(ars: Ars, givens: GivenConfiguration) -> Stabilizer:
    """Derive H from the ambient group and the given configuration."""

    elements = {Parity.IDENTITY}
    if Parity.FLIPPED in ars.transformation_group.elements:
        elements.add(Parity.FLIPPED)
    return Stabilizer(ars.transformation_group, givens, frozenset(elements))


def _single_frame_torsor(key: FrameKey) -> FrameTorsor:
    frames = frozenset(
        Frame(frozenset({FrameCoordinate(key, parity)}))
        for parity in key.stabilizer.elements
    )
    return FrameTorsor(
        frozenset({key}),
        frames,
        EquivarianceLaw(
            "frame action",
            "the nonidentity stabilizer element exchanges both frames",
            Verdict.HOLDS,
        ),
    )


def _coordinate(frame: Frame, key: FrameKey) -> FrameCoordinate:
    return next(coordinate for coordinate in frame.coordinates if coordinate.key == key)


def _flipped(parity: Parity) -> Parity:
    return Parity.FLIPPED if parity is Parity.IDENTITY else Parity.IDENTITY


def _flip_frame(frame: Frame, keys: frozenset[FrameKey]) -> Frame:
    return Frame(
        frozenset(
            FrameCoordinate(
                coordinate.key,
                _flipped(coordinate.parity)
                if coordinate.key in keys
                else coordinate.parity,
            )
            for coordinate in frame.coordinates
        )
    )


def _value_at(family: EquivariantFamily, frame: Frame) -> Form:
    return next(item.value for item in family.graph if item.frame == frame)


def image(potential: Potential) -> frozenset[Form]:
    """Derive possible results from the family; they are not stored as options."""

    return frozenset(item.value for item in potential.family.graph)


def _intersection_potential(
    circles: frozenset[Circle],
    stabilizer: Stabilizer,
) -> Potential:
    key = FrameKey("reflection frame of AB", stabilizer)
    torsor = _single_frame_torsor(key)
    graph = frozenset(
        FamilyValue(
            frame,
            Intersection(circles, _coordinate(frame, key).parity),
        )
        for frame in torsor.frames
    )
    family = EquivariantFamily(
        torsor,
        graph,
        EquivarianceLaw(
            "circle intersection",
            "reflecting the frame reflects the intersection",
            Verdict.HOLDS,
        ),
    )
    return Potential(
        family,
        SettlementRule("Witness", "an orientation Frame for the reflection torsor"),
    )


def _map(
    potential: Potential,
    name: str,
    transform: Callable[[Form], Form],
) -> Potential:
    family = EquivariantFamily(
        potential.family.torsor,
        frozenset(
            FamilyValue(item.frame, transform(item.value))
            for item in potential.family.graph
        ),
        EquivarianceLaw(
            name,
            "the construction is applied uniformly throughout the frame torsor",
            Verdict.HOLDS,
        ),
    )
    return Potential(family, potential.settlement)


def lift_line(point: Point, apex: Potential, name: str) -> Potential:
    return _map(
        apex,
        f"lifted Line {name}",
        lambda value: CandidateLine(point, value, name),
    )


def shared(first: Potential, second: Potential) -> Potential:
    """Direct sharing: both families read the same frame."""

    if first.family.torsor != second.family.torsor:
        raise ValueError("shared families require one torsor")
    graph = frozenset(
        FamilyValue(
            frame,
            Pair(_value_at(first.family, frame), _value_at(second.family, frame)),
        )
        for frame in first.family.torsor.frames
    )
    return Potential(
        EquivariantFamily(
            first.family.torsor,
            graph,
            EquivarianceLaw(
                "direct sharing",
                "both constructions use the same frame",
                Verdict.HOLDS,
            ),
        ),
        first.settlement,
    )


def twisted(first: Potential, second: Potential) -> Potential:
    """Twisted sharing: the second family reads the reflected frame."""

    if first.family.torsor != second.family.torsor:
        raise ValueError("twisted families require one torsor")
    keys = first.family.torsor.keys
    graph = frozenset(
        FamilyValue(
            frame,
            Pair(
                _value_at(first.family, frame),
                _value_at(second.family, _flip_frame(frame, keys)),
            ),
        )
        for frame in first.family.torsor.frames
    )
    return Potential(
        EquivariantFamily(
            first.family.torsor,
            graph,
            EquivarianceLaw(
                "twisted sharing",
                "the second construction uses the reflected frame",
                Verdict.HOLDS,
            ),
        ),
        first.settlement,
    )


def independent(first: Potential, second: Potential) -> Potential:
    """Independent families vary over the product torsor."""

    if first.family.torsor.keys & second.family.torsor.keys:
        raise ValueError("independent families require distinct frame keys")
    frames = frozenset(
        Frame(left.coordinates | right.coordinates)
        for left, right in product(
            first.family.torsor.frames,
            second.family.torsor.frames,
        )
    )
    torsor = FrameTorsor(
        first.family.torsor.keys | second.family.torsor.keys,
        frames,
        EquivarianceLaw(
            "product frame action",
            "each frame factor varies independently",
            Verdict.HOLDS,
        ),
    )
    graph = frozenset(
        FamilyValue(
            frame,
            Pair(
                _value_at(
                    first.family,
                    Frame(
                        frozenset(
                            coordinate
                            for coordinate in frame.coordinates
                            if coordinate.key in first.family.torsor.keys
                        )
                    ),
                ),
                _value_at(
                    second.family,
                    Frame(
                        frozenset(
                            coordinate
                            for coordinate in frame.coordinates
                            if coordinate.key in second.family.torsor.keys
                        )
                    ),
                ),
            ),
        )
        for frame in frames
    )
    return Potential(
        EquivariantFamily(
            torsor,
            graph,
            EquivarianceLaw(
                "independent composition",
                "the result is a family over the product torsor",
                Verdict.HOLDS,
            ),
        ),
        SettlementRule("Witness", "one Frame for each independent torsor"),
    )


def independent_copy(potential: Potential, name: str) -> Potential:
    """Reindex a family by an independently derived frame key for comparison."""

    old_key = next(iter(potential.family.torsor.keys))
    new_key = FrameKey(name, old_key.stabilizer)
    torsor = _single_frame_torsor(new_key)
    old_by_parity = {
        _coordinate(item.frame, old_key).parity: item.value
        for item in potential.family.graph
    }
    graph = frozenset(
        FamilyValue(frame, old_by_parity[_coordinate(frame, new_key).parity])
        for frame in torsor.frames
    )
    return Potential(
        EquivariantFamily(torsor, graph, potential.family.law),
        potential.settlement,
    )


def _triangle_potential(
    base: Line,
    apex: Potential,
    side_a: Potential,
    side_b: Potential,
) -> Potential:
    torsor = apex.family.torsor
    graph = frozenset(
        FamilyValue(
            frame,
            Triangle(
                base,
                _value_at(apex.family, frame),
                frozenset(
                    {
                        _value_at(side_a.family, frame),
                        _value_at(side_b.family, frame),
                    }
                ),
            ),
        )
        for frame in torsor.frames
    )
    return Potential(
        EquivariantFamily(
            torsor,
            graph,
            EquivarianceLaw(
                "triangle construction",
                "constructing throughout the frame commutes with reflection",
                Verdict.HOLDS,
            ),
        ),
        apex.settlement,
    )


def cast(spell: ElaboratedSpell, context: Context) -> CastResult:
    missing = spell.derived_requirements - context.capabilities
    if missing:
        capability = next(iter(missing))
        step = next(step for step in spell.steps if step.rule.capability == capability)
        return Refused(capability, step, ())
    bindings = {named.name: named.form for named in context.bindings}
    trace: tuple[TraceEntry, ...] = ()
    for input_name in spell.source.inputs:
        if input_name not in bindings:
            return Failed(f"missing input {input_name}", None, trace)
    point_a = bindings["A"]
    point_b = bindings["B"]
    base = bindings["AB"]
    if not isinstance(point_a, Point) or not isinstance(point_b, Point):
        return Failed("A and B must be settled Points", None, trace)
    if not isinstance(base, Line):
        return Failed("AB must be a Line", None, trace)
    circles: dict[str, Circle] = {}
    for step in spell.steps[:2]:
        instruction = step.instruction
        center = bindings[instruction.arguments[0]]
        through = bindings[instruction.arguments[1]]
        if not isinstance(center, Point) or not isinstance(through, Point):
            return Failed("circle arguments must be Points", step, trace)
        circle = Circle(center, through, Occurrence(instruction.bind))
        circles[instruction.bind] = circle
        trace = (*trace, TraceEntry(step, circle))
    intersection_step = spell.steps[2]
    if point_a.selected == point_b.selected:
        return Failed(
            "the permitted intersection cannot yield a two-frame family "
            "for coincident centers",
            intersection_step,
            trace,
        )
    stabilizer = derive_stabilizer(
        context.ars,
        GivenConfiguration(point_a, point_b, base),
    )
    apex = _intersection_potential(frozenset(circles.values()), stabilizer)
    trace = (*trace, TraceEntry(intersection_step, apex))
    side_a = lift_line(point_a, apex, "AC")
    side_b = lift_line(point_b, apex, "BC")
    trace = (*trace, TraceEntry(spell.steps[3], side_a))
    trace = (*trace, TraceEntry(spell.steps[4], side_b))
    triangle = _triangle_potential(base, apex, side_a, side_b)
    return Produced(Effect(triangle, base), trace)


def with_frame(
    context: Context,
    potential: Potential,
    parity: Parity,
) -> Context:
    witnesses = frozenset(
        FrameWitness(FrameCoordinate(key, parity), "declared orientation Frame")
        for key in potential.family.torsor.keys
    )
    return replace(
        context,
        frame_witnesses=context.frame_witnesses | witnesses,
    )


def settle(potential: Potential, context: Context) -> SettlementResult:
    by_key = {witness.coordinate.key: witness for witness in context.frame_witnesses}
    if not potential.family.torsor.keys <= by_key.keys():
        return potential
    frame = Frame(
        frozenset(by_key[key].coordinate for key in potential.family.torsor.keys)
    )
    matches = tuple(
        item.value for item in potential.family.graph if item.frame == frame
    )
    if len(matches) != 1:
        return Failed("Frame did not select exactly one family value", None, ())
    evidence = SettlementEvidence(
        frozenset(by_key[key] for key in potential.family.torsor.keys)
    )
    return Point(matches[0], evidence, Occurrence("settled frame value"))


def validate_will(
    will: Will,
    ars: Ars,
    givens: GivenConfiguration,
) -> WillValidation:
    stabilizer = derive_stabilizer(ars, givens)
    if will.predicate is WillPredicate.EQUILATERAL_ON_BASE:
        return InvariantWill(will, stabilizer)
    return NonInvariantWill(
        will,
        stabilizer,
        "reflection preserves the givens but changes the requested apex side",
    )


def _truth_for(will: Will, triangle: Triangle) -> Truth:
    if will.predicate is WillPredicate.EQUILATERAL_ON_BASE:
        holds = (
            triangle.base.occurrence == will.base.occurrence
            and len(triangle.sides) == 2
        )
        return Truth(Verdict.HOLDS if holds else Verdict.DOES_NOT_HOLD)
    holds = triangle.apex.parity is Parity.IDENTITY
    return Truth(Verdict.HOLDS if holds else Verdict.DOES_NOT_HOLD)


def _branch_proof(triangle: Triangle, ars: Ars) -> BranchProof:
    bridge = next(bridge for bridge in ars.bridges if bridge == LENGTH_BRIDGE)
    if not (
        bridge.preserves_equality is Verdict.HOLDS
        and bridge.commutes_with_constructions is Verdict.HOLDS
        and bridge.equivariant is Verdict.HOLDS
    ):
        raise ValueError("the length Bridge lacks its preservation obligations")
    side_a, side_b = tuple(triangle.sides)
    base_length = Length(triangle.base)
    side_a_length = Length(side_a)
    side_b_length = Length(side_b)
    equalities = (
        QualifiedEqual(
            "Ars Arithmetica",
            base_length,
            side_a_length,
            ARITHMETIC_EQUALITY,
        ),
        QualifiedEqual(
            "Ars Arithmetica",
            base_length,
            side_b_length,
            ARITHMETIC_EQUALITY,
        ),
        QualifiedEqual(
            "Ars Arithmetica",
            side_a_length,
            side_b_length,
            ARITHMETIC_EQUALITY,
        ),
    )
    return BranchProof(triangle, equalities)


def check(will: Will, effect: Effect, context: Context) -> CheckResult:
    """Lift a terminating Will through Potential and collapse invariant truth."""

    if isinstance(effect.form, Triangle):
        truth = _truth_for(will, effect.form)
        if truth.verdict is Verdict.HOLDS:
            proof = InvariantDemonstration(
                frozenset({_branch_proof(effect.form, context.ars)}),
                LENGTH_BRIDGE,
                Verdict.HOLDS,
            )
            return Conforms(will, effect, proof)
        return Counterexample(will, effect, effect.form)
    truth_potential = _map(
        effect.form,
        f"check {will.predicate.value}",
        lambda value: _truth_for(will, value),
    )
    truth_image = image(truth_potential)
    if truth_image == frozenset({Truth(Verdict.HOLDS)}):
        proofs = frozenset(
            _branch_proof(item.value, context.ars)
            for item in effect.form.family.graph
            if isinstance(item.value, Triangle)
        )
        return Conforms(
            will,
            effect,
            InvariantDemonstration(proofs, LENGTH_BRIDGE, Verdict.HOLDS),
        )
    if truth_image == frozenset({Truth(Verdict.DOES_NOT_HOLD)}):
        return Counterexample(will, effect, next(iter(image(effect.form))))
    return FrameDependentCheck(will, effect, truth_potential)


def assess_default(
    candidate: CandidateKind,
    ars: Ars,
    givens: GivenConfiguration,
) -> DefaultAssessment:
    all_equivariant = all(
        rule.equivariance.verified is Verdict.HOLDS for rule in ars.constructions
    )
    fixed = candidate is CandidateKind.MIDPOINT
    operation = (
        Operation.CONSTRUCT_MIDPOINT
        if candidate is CandidateKind.MIDPOINT
        else Operation.INTERSECT_CIRCLES
    )
    constructible = any(rule.operation is operation for rule in ars.constructions)
    legitimate = fixed and constructible and all_equivariant
    return DefaultAssessment(
        candidate,
        Verdict.HOLDS if fixed else Verdict.DOES_NOT_HOLD,
        Verdict.HOLDS if constructible else Verdict.DOES_NOT_HOLD,
        Verdict.HOLDS if legitimate else Verdict.DOES_NOT_HOLD,
        Verdict.HOLDS if all_equivariant else Verdict.DOES_NOT_HOLD,
    )


def assess_group(ars: Ars, givens: GivenConfiguration) -> GroupAssessment:
    stabilizer = derive_stabilizer(ars, givens)
    diagnostic = (
        GroupDiagnostic.INFORMATIVE
        if Parity.FLIPPED in stabilizer.elements
        else GroupDiagnostic.TRIVIAL_ACTION
    )
    return GroupAssessment(stabilizer, diagnostic)


def _side(direction: Parity, chirality: Parity) -> Side:
    return Side.POSITIVE if direction is chirality else Side.NEGATIVE


def frame_placement_report(
    direct: Potential,
    twisted_family: Potential,
    independent_family: Potential,
) -> FramePlacementReport:
    return FramePlacementReport(
        _side(Parity.IDENTITY, Parity.IDENTITY),
        _side(Parity.FLIPPED, Parity.IDENTITY),
        _side(Parity.IDENTITY, Parity.FLIPPED),
        _side(Parity.FLIPPED, Parity.FLIPPED),
        len(image(direct)),
        len(image(twisted_family)),
        len(image(independent_family)),
        FramePlacement.POTENTIAL,
        "the effective side frame is derived from direction XOR chirality and "
        "carries direct or twisted correlation without a fresh left/right choice",
    )
