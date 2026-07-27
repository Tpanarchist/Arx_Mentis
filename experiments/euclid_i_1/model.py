"""An owned, inspectable model of Euclid I.1.

This module is experiment code, not an Arx Mentis implementation. Its Python
representation exists to make the proposed behavior precise enough to challenge;
none of its classes, iteration behavior, or failure policy is language law.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Form:
    """Marker for values that cross this experiment's observation boundary."""

    __slots__ = ()


class Side(Enum):
    """A side relative to an explicitly oriented line."""

    LEFT = "left"
    RIGHT = "right"


class Construction(Enum):
    CIRCLE_FROM_CENTER_AND_POINT = "circle-from-center-and-point"
    CIRCLE_INTERSECTIONS = "circle-intersections"
    LINE_BETWEEN_POINTS = "line-between-points"


class Conformity(Enum):
    CONFORMS = "conforms"


@dataclass(frozen=True, slots=True)
class Ars(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Point(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Circle(Form):
    center: Point
    through: Point


@dataclass(frozen=True, slots=True)
class OrientedLine(Form):
    """A temporary experiment form; it does not make every Line directed."""

    start: Point
    end: Point


@dataclass(frozen=True, slots=True)
class IntersectionPoint(Form):
    circles: frozenset[Circle]
    relative_to: OrientedLine
    side: Side


type PointForm = Point | IntersectionPoint


@dataclass(frozen=True, slots=True)
class Line(Form):
    endpoints: frozenset[PointForm]

    def __post_init__(self) -> None:
        if len(self.endpoints) != 2:
            raise ValueError("an experimental Line requires two distinct Points")


@dataclass(frozen=True, slots=True)
class GeometricForm(Form):
    points: frozenset[PointForm]
    lines: frozenset[Line]


@dataclass(frozen=True, slots=True)
class Definition(Form):
    name: str
    statement: str


@dataclass(frozen=True, slots=True)
class Postulate(Form):
    name: str
    construction: Construction
    statement: str


@dataclass(frozen=True, slots=True)
class CommonNotion(Form):
    name: str
    statement: str


type Rule = Definition | CommonNotion


@dataclass(frozen=True, slots=True)
class EqualityClaim(Form):
    lines: frozenset[Line]

    def __post_init__(self) -> None:
        if len(self.lines) != 2:
            raise ValueError("an equality claim relates two distinct Lines")


@dataclass(frozen=True, slots=True)
class EquilateralClaim(Form):
    lines: frozenset[Line]

    def __post_init__(self) -> None:
        if len(self.lines) != 3:
            raise ValueError("an equilateral claim requires three Lines")


type Claim = EqualityClaim | EquilateralClaim


@dataclass(frozen=True, slots=True)
class DemonstrationStep(Form):
    conclusion: Claim
    basis: Rule
    premises: tuple[Claim, ...] = ()
    witnesses: tuple[Form, ...] = ()


@dataclass(frozen=True, slots=True)
class Demonstration(Form):
    steps: tuple[DemonstrationStep, ...]
    conclusion: EquilateralClaim


@dataclass(frozen=True, slots=True)
class ExpectedEffect(Form):
    description: str


@dataclass(frozen=True, slots=True)
class Will(Form):
    name: str
    intended_effect: ExpectedEffect


@dataclass(frozen=True, slots=True)
class CircleStep(Form):
    bind: str
    center: str
    through: str
    postulate: Postulate


@dataclass(frozen=True, slots=True)
class IntersectionsStep(Form):
    bind: str
    first_circle: str
    second_circle: str
    axis_start: str
    axis_end: str
    postulate: Postulate


@dataclass(frozen=True, slots=True)
class LineStep(Form):
    bind: str
    first_point: str
    second_point: str
    postulate: Postulate


type ConstructionStep = CircleStep | IntersectionsStep | LineStep


@dataclass(frozen=True, slots=True)
class EffectSpec(Form):
    points: tuple[str, ...]
    lines: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DemonstrationPlan(Form):
    first_circle: str
    first_radius: str
    first_peer_radius: str
    second_circle: str
    second_radius: str
    second_peer_radius: str
    triangle_lines: tuple[str, str, str]
    radius_definition: Definition
    equality_common_notion: CommonNotion
    equilateral_definition: Definition


@dataclass(frozen=True, slots=True)
class Requirements(Form):
    postulates: frozenset[Postulate]
    definitions: frozenset[Definition]
    common_notions: frozenset[CommonNotion]


@dataclass(frozen=True, slots=True)
class Spell(Form):
    name: str
    ars: Ars
    inputs: tuple[str, ...]
    will: Will
    requirements: Requirements
    steps: tuple[ConstructionStep, ...]
    effect: EffectSpec
    demonstration: DemonstrationPlan


@dataclass(frozen=True, slots=True)
class NamedForm(Form):
    name: str
    form: Form


@dataclass(frozen=True, slots=True)
class Reader(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Orientation(Form):
    line: OrientedLine
    selected_side: Side


@dataclass(frozen=True, slots=True)
class Context(Form):
    reader: Reader
    forms: frozenset[NamedForm]
    postulates: frozenset[Postulate]
    definitions: frozenset[Definition]
    common_notions: frozenset[CommonNotion]
    orientation: Orientation | None = None


@dataclass(frozen=True, slots=True)
class TraceEntry(Form):
    step: ConstructionStep
    basis: Postulate
    produced: tuple[Form, ...]


@dataclass(frozen=True, slots=True)
class ConstructionTrace(Form):
    entries: tuple[TraceEntry, ...]


@dataclass(frozen=True, slots=True)
class WillComparison(Form):
    will: Will
    evidence: EquilateralClaim
    judgement: Conformity


@dataclass(frozen=True, slots=True)
class Effect(Form):
    form: GeometricForm
    trace: ConstructionTrace
    demonstration: Demonstration
    comparison: WillComparison


@dataclass(frozen=True, slots=True)
class OrientationTrigger(Form):
    line: OrientedLine


@dataclass(frozen=True, slots=True)
class Potential(Form):
    """Unsettled options and the only declared means of settling them."""

    options: frozenset[Effect]
    trigger: OrientationTrigger


@dataclass(frozen=True, slots=True)
class ExperimentRefusal(Form):
    """Harness-only diagnostic; deliberately not a proposed failure semantic."""

    reason: str
    missing: frozenset[Form] = frozenset()


type CastResult = Effect | Potential | ExperimentRefusal


ARS_GEOMETRICA = Ars("Ars Geometrica")

CIRCLE_POSTULATE = Postulate(
    "circle construction",
    Construction.CIRCLE_FROM_CENTER_AND_POINT,
    "A circle may be constructed from a center through a Point.",
)
INTERSECTION_POSTULATE = Postulate(
    "circle intersection construction",
    Construction.CIRCLE_INTERSECTIONS,
    "The intersection Points of two circles may be constructed.",
)
LINE_POSTULATE = Postulate(
    "line construction",
    Construction.LINE_BETWEEN_POINTS,
    "A Line may be constructed between two distinct Points.",
)
CIRCLE_RADII_DEFINITION = Definition(
    "equal radii of one circle",
    "Lines from one circle's center to its circumference are equal.",
)
EQUILATERAL_DEFINITION = Definition(
    "equilateral triangular Form",
    "A triangular Form is equilateral when its three Lines are equal.",
)
EQUALITY_COMMON_NOTION = CommonNotion(
    "common notion 1",
    "Things equal to the same thing are equal to one another.",
)


def make_proposition() -> tuple[Line, Spell]:
    """Create the given Line and the inspectable Spell Form for Euclid I.1."""

    point_a = Point("A")
    point_b = Point("B")
    line_ab = Line(frozenset({point_a, point_b}))
    will = Will(
        "construct Euclid I.1",
        ExpectedEffect("an equilateral triangular Form on the given Line AB"),
    )
    requirements = Requirements(
        postulates=frozenset(
            {CIRCLE_POSTULATE, INTERSECTION_POSTULATE, LINE_POSTULATE}
        ),
        definitions=frozenset({CIRCLE_RADII_DEFINITION, EQUILATERAL_DEFINITION}),
        common_notions=frozenset({EQUALITY_COMMON_NOTION}),
    )
    spell = Spell(
        name="Euclid I.1",
        ars=ARS_GEOMETRICA,
        inputs=("A", "B", "AB"),
        will=will,
        requirements=requirements,
        steps=(
            CircleStep("circle_A", "A", "B", CIRCLE_POSTULATE),
            CircleStep("circle_B", "B", "A", CIRCLE_POSTULATE),
            IntersectionsStep(
                "C",
                "circle_A",
                "circle_B",
                "A",
                "B",
                INTERSECTION_POSTULATE,
            ),
            LineStep("AC", "A", "C", LINE_POSTULATE),
            LineStep("BC", "B", "C", LINE_POSTULATE),
        ),
        effect=EffectSpec(points=("A", "B", "C"), lines=("AB", "AC", "BC")),
        demonstration=DemonstrationPlan(
            first_circle="circle_A",
            first_radius="AB",
            first_peer_radius="AC",
            second_circle="circle_B",
            second_radius="AB",
            second_peer_radius="BC",
            triangle_lines=("AB", "AC", "BC"),
            radius_definition=CIRCLE_RADII_DEFINITION,
            equality_common_notion=EQUALITY_COMMON_NOTION,
            equilateral_definition=EQUILATERAL_DEFINITION,
        ),
    )
    return line_ab, spell


def make_context(
    line_ab: Line,
    *,
    selected_side: Side | None = None,
) -> Context:
    """Create a complete Context, optionally declaring an orientation trigger."""

    named_points = sorted(
        (point for point in line_ab.endpoints if isinstance(point, Point)),
        key=lambda point: point.name,
    )
    if len(named_points) != 2:
        raise ValueError("the Euclid I.1 experiment requires named Points A and B")
    points = {point.name: point for point in named_points}
    point_a = points["A"]
    point_b = points["B"]
    axis = OrientedLine(point_a, point_b)
    orientation = None if selected_side is None else Orientation(axis, selected_side)
    return Context(
        reader=Reader("Euclid I.1 experimental caster"),
        forms=frozenset(
            {
                NamedForm("A", point_a),
                NamedForm("B", point_b),
                NamedForm("AB", line_ab),
            }
        ),
        postulates=frozenset(
            {CIRCLE_POSTULATE, INTERSECTION_POSTULATE, LINE_POSTULATE}
        ),
        definitions=frozenset({CIRCLE_RADII_DEFINITION, EQUILATERAL_DEFINITION}),
        common_notions=frozenset({EQUALITY_COMMON_NOTION}),
        orientation=orientation,
    )


def _requirements_refusal(spell: Spell, context: Context) -> ExperimentRefusal | None:
    missing: frozenset[Form] = frozenset(
        (spell.requirements.postulates - context.postulates)
        | (spell.requirements.definitions - context.definitions)
        | (spell.requirements.common_notions - context.common_notions)
    )
    if missing:
        return ExperimentRefusal(
            "the Context does not justify every construction and demonstration",
            missing,
        )
    return None


def _initial_bindings(
    spell: Spell, context: Context
) -> dict[str, Form] | ExperimentRefusal:
    bindings = {named.name: named.form for named in context.forms}
    missing = frozenset(Point(name) for name in spell.inputs if name not in bindings)
    if missing:
        return ExperimentRefusal("the Context lacks required input Forms", missing)
    return bindings


def _point(bindings: dict[str, Form], name: str) -> PointForm:
    value = bindings[name]
    if not isinstance(value, Point | IntersectionPoint):
        raise TypeError(f"{name} is not a Point Form")
    return value


def _line(bindings: dict[str, Form], name: str) -> Line:
    value = bindings[name]
    if not isinstance(value, Line):
        raise TypeError(f"{name} is not a Line Form")
    return value


def _circle(bindings: dict[str, Form], name: str) -> Circle:
    value = bindings[name]
    if not isinstance(value, Circle):
        raise TypeError(f"{name} is not a Circle Form")
    return value


def _execute_step(
    step: ConstructionStep,
    bindings: dict[str, Form],
    context: Context,
) -> tuple[tuple[Form, ...], OrientationTrigger | None] | ExperimentRefusal:
    if isinstance(step, CircleStep):
        center = _point(bindings, step.center)
        through = _point(bindings, step.through)
        if not isinstance(center, Point) or not isinstance(through, Point):
            return ExperimentRefusal(
                "this experiment only constructs its two circles from given Points"
            )
        return (Circle(center, through),), None

    if isinstance(step, IntersectionsStep):
        first = _circle(bindings, step.first_circle)
        second = _circle(bindings, step.second_circle)
        start = _point(bindings, step.axis_start)
        end = _point(bindings, step.axis_end)
        if not isinstance(start, Point) or not isinstance(end, Point):
            return ExperimentRefusal(
                "this experiment requires a given oriented reference axis"
            )
        axis = OrientedLine(start, end)
        circles = frozenset({first, second})
        candidates = tuple(IntersectionPoint(circles, axis, side) for side in Side)
        if context.orientation is None:
            return candidates, OrientationTrigger(axis)
        if context.orientation.line != axis:
            return ExperimentRefusal(
                "the Context orientation does not address this intersection"
            )
        selected = next(
            candidate
            for candidate in candidates
            if candidate.side is context.orientation.selected_side
        )
        return (selected,), None

    first = _point(bindings, step.first_point)
    second = _point(bindings, step.second_point)
    return (Line(frozenset({first, second})),), None


def _demonstrate(
    spell: Spell,
    bindings: dict[str, Form],
) -> Demonstration:
    plan = spell.demonstration
    first_circle = _circle(bindings, plan.first_circle)
    second_circle = _circle(bindings, plan.second_circle)
    first_radius = _line(bindings, plan.first_radius)
    first_peer = _line(bindings, plan.first_peer_radius)
    second_radius = _line(bindings, plan.second_radius)
    second_peer = _line(bindings, plan.second_peer_radius)

    apex = next(
        point for point in first_peer.endpoints if isinstance(point, IntersectionPoint)
    )
    if first_circle not in apex.circles or second_circle not in apex.circles:
        raise ValueError("the claimed apex is not on both constructed circles")

    first_equality = EqualityClaim(frozenset({first_radius, first_peer}))
    second_equality = EqualityClaim(frozenset({second_radius, second_peer}))
    peer_equality = EqualityClaim(frozenset({first_peer, second_peer}))
    triangle_lines = frozenset(_line(bindings, name) for name in plan.triangle_lines)
    conclusion = EquilateralClaim(triangle_lines)
    steps = (
        DemonstrationStep(
            first_equality,
            plan.radius_definition,
            witnesses=(first_circle, apex),
        ),
        DemonstrationStep(
            second_equality,
            plan.radius_definition,
            witnesses=(second_circle, apex),
        ),
        DemonstrationStep(
            peer_equality,
            plan.equality_common_notion,
            (first_equality, second_equality),
        ),
        DemonstrationStep(
            conclusion,
            plan.equilateral_definition,
            (first_equality, second_equality, peer_equality),
        ),
    )
    return Demonstration(steps, conclusion)


def _make_effect(
    spell: Spell,
    bindings: dict[str, Form],
    trace: tuple[TraceEntry, ...],
) -> Effect:
    produced_form = GeometricForm(
        points=frozenset(_point(bindings, name) for name in spell.effect.points),
        lines=frozenset(_line(bindings, name) for name in spell.effect.lines),
    )
    demonstration = _demonstrate(spell, bindings)
    comparison = WillComparison(
        spell.will,
        demonstration.conclusion,
        Conformity.CONFORMS,
    )
    return Effect(
        form=produced_form,
        trace=ConstructionTrace(trace),
        demonstration=demonstration,
        comparison=comparison,
    )


def cast(spell: Spell, context: Context) -> CastResult:
    """Read one Spell Form as instructions within one explicit Context."""

    refusal = _requirements_refusal(spell, context)
    if refusal is not None:
        return refusal
    initial = _initial_bindings(spell, context)
    if isinstance(initial, ExperimentRefusal):
        return initial

    states: list[tuple[dict[str, Form], tuple[TraceEntry, ...]]] = [(initial, ())]
    unresolved_trigger: OrientationTrigger | None = None
    for step in spell.steps:
        next_states: list[tuple[dict[str, Form], tuple[TraceEntry, ...]]] = []
        for bindings, trace in states:
            execution = _execute_step(step, bindings, context)
            if isinstance(execution, ExperimentRefusal):
                return execution
            results, trigger = execution
            if trigger is not None:
                if unresolved_trigger is not None and unresolved_trigger != trigger:
                    return ExperimentRefusal(
                        "the disposable caster cannot carry two independent Potentials"
                    )
                unresolved_trigger = trigger
            for result in results:
                branch_bindings = dict(bindings)
                branch_bindings[step.bind] = result
                entry = TraceEntry(step, step.postulate, (result,))
                next_states.append((branch_bindings, (*trace, entry)))
        states = next_states

    effects = frozenset(
        _make_effect(spell, bindings, trace) for bindings, trace in states
    )
    if unresolved_trigger is not None:
        return Potential(effects, unresolved_trigger)
    if len(effects) != 1:
        return ExperimentRefusal("a settled Cast did not produce exactly one Effect")
    return next(iter(effects))
