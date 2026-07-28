"""Read one generic composite Form as data or exact construction.

There is intentionally no ``Spell`` class in this experiment. Reader and Context
give the same Form its role. These Python representations remain disposable.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class Form:
    __slots__ = ()


@dataclass(frozen=True, slots=True)
class Name(Form):
    text: str


@dataclass(frozen=True, slots=True)
class Predicate(Form):
    text: str


@dataclass(frozen=True, slots=True)
class Clause(Form):
    subject: Name
    predicate: Predicate


@dataclass(frozen=True, slots=True)
class Operation(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Will(Form):
    description: str
    expected_subject: Name


class RelationKind(Enum):
    GIVEN = "given"
    FROM = "from"
    TO = "to"
    SERVES = "serves"


@dataclass(frozen=True, slots=True)
class Relation(Form):
    source: Form
    kind: RelationKind
    target: Form


@dataclass(frozen=True, slots=True)
class CompositeForm(Form):
    nodes: frozenset[Form]
    relations: frozenset[Relation]


@dataclass(frozen=True, slots=True)
class Inspector(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Interpreter(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Audience(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Witness(Form):
    name: str


type Reader = Inspector | Interpreter | Audience | Witness


class Construction(Enum):
    RENAME_CLAUSE_SUBJECT = "rename-clause-subject"


@dataclass(frozen=True, slots=True)
class Permission(Form):
    construction: Construction


@dataclass(frozen=True, slots=True)
class GrammarDefinition(Form):
    operation_name: str
    required_relations: frozenset[RelationKind]


@dataclass(frozen=True, slots=True)
class EqualityDeclaration(Form):
    ars_name: str
    subject: str
    reflexive: bool
    symmetric: bool
    transitive: bool


@dataclass(frozen=True, slots=True)
class Context(Form):
    reader: Reader
    permissions: frozenset[Permission]
    definitions: frozenset[GrammarDefinition]
    equality: EqualityDeclaration


@dataclass(frozen=True, slots=True)
class Inspection(Form):
    reader: Reader
    source: CompositeForm
    nodes: frozenset[Form]
    relations: frozenset[Relation]


@dataclass(frozen=True, slots=True)
class RelationPreservationTrace(Form):
    definition: GrammarDefinition
    source: Clause
    effect: Clause
    replaced: tuple[Name, Name]
    preserved_predicate: Predicate


@dataclass(frozen=True, slots=True)
class Effect(Form):
    source: CompositeForm
    form: Clause
    will: Will
    trace: RelationPreservationTrace


@dataclass(frozen=True, slots=True)
class Equivalent(Form):
    ars_name: str
    source: Clause
    effect: Clause
    law: EqualityDeclaration
    preserved_relation: Predicate


@dataclass(frozen=True, slots=True)
class Counterexample(Form):
    will: Will
    effect: Effect
    reason: str


type CheckResult = Equivalent | Counterexample


@dataclass(frozen=True, slots=True)
class Refused(Form):
    missing: Form
    reason: str


@dataclass(frozen=True, slots=True)
class Failed(Form):
    reason: str
    related: frozenset[Form] = frozenset()


class DiagnosticKind(Enum):
    UNSUPPORTED_READER = "unsupported-reader"
    AMBIGUOUS_DEFINITION = "ambiguous-definition"


@dataclass(frozen=True, slots=True)
class ExperimentalDiagnostic(Form):
    """Harness-only outcome; it does not define Arx Mentis failure."""

    kind: DiagnosticKind
    reason: str
    related: frozenset[Form] = frozenset()


type ReadResult = Inspection | Effect | Refused | Failed | ExperimentalDiagnostic


RENAME_PERMISSION = Permission(Construction.RENAME_CLAUSE_SUBJECT)
RENAME_GRAMMAR = GrammarDefinition(
    "rename-subject",
    frozenset(
        {
            RelationKind.GIVEN,
            RelationKind.FROM,
            RelationKind.TO,
            RelationKind.SERVES,
        }
    ),
)
GRAMMATICAL_EQUIVALENCE = EqualityDeclaration(
    "Ars Grammatica",
    "equivalence of clause relations relevant to the declared rename",
    True,
    True,
    True,
)


@dataclass(frozen=True, slots=True)
class Experiment(Form):
    form: CompositeForm
    examining_context: Context
    executing_context: Context
    unsupported_context: Context
    source_clause: Clause


def make_experiment() -> Experiment:
    mercury = Name("mercury")
    hermes = Name("hermes")
    moves = Predicate("moves")
    source_clause = Clause(mercury, moves)
    operation = Operation("rename-subject")
    will = Will("rename the clause subject while preserving its predicate", hermes)
    nodes: frozenset[Form] = frozenset(
        {mercury, hermes, moves, source_clause, operation, will}
    )
    relations = frozenset(
        {
            Relation(operation, RelationKind.GIVEN, source_clause),
            Relation(operation, RelationKind.FROM, mercury),
            Relation(operation, RelationKind.TO, hermes),
            Relation(operation, RelationKind.SERVES, will),
        }
    )
    form = CompositeForm(nodes, relations)
    examining_context = Context(
        Inspector("structural examiner"),
        frozenset({RENAME_PERMISSION}),
        frozenset({RENAME_GRAMMAR}),
        GRAMMATICAL_EQUIVALENCE,
    )
    executing_context = replace(
        examining_context,
        reader=Interpreter("construction interpreter"),
    )
    unsupported_context = replace(
        examining_context,
        reader=Audience("rhetorical audience"),
    )
    return Experiment(
        form,
        examining_context,
        executing_context,
        unsupported_context,
        source_clause,
    )


def _target(
    form: CompositeForm,
    operation: Operation,
    kind: RelationKind,
) -> Form | Failed:
    targets = tuple(
        relation.target
        for relation in form.relations
        if relation.source == operation and relation.kind is kind
    )
    if len(targets) != 1:
        return Failed(
            f"the construction requires exactly one {kind.value} relation",
            frozenset({operation}),
        )
    return targets[0]


def _execute(
    form: CompositeForm,
    context: Context,
) -> Effect | Refused | Failed | ExperimentalDiagnostic:
    definitions = tuple(
        definition
        for definition in context.definitions
        if definition.operation_name == RENAME_GRAMMAR.operation_name
    )
    if not definitions:
        return Refused(
            RENAME_GRAMMAR,
            "Context cannot read the composite construction",
        )
    if len(definitions) != 1:
        return ExperimentalDiagnostic(
            DiagnosticKind.AMBIGUOUS_DEFINITION,
            "Context contains competing readings for the operation",
            frozenset(definitions),
        )
    definition = definitions[0]
    if RENAME_PERMISSION not in context.permissions:
        return Refused(
            RENAME_PERMISSION,
            "Reader may recognize but may not perform the rename construction",
        )
    operations = tuple(
        node
        for node in form.nodes
        if isinstance(node, Operation) and node.name == definition.operation_name
    )
    if len(operations) != 1:
        return Failed(
            "the Form requires exactly one recognized operation node",
            frozenset(operations),
        )
    operation = operations[0]
    extracted = {
        kind: _target(form, operation, kind) for kind in definition.required_relations
    }
    diagnostic = next(
        (value for value in extracted.values() if isinstance(value, Failed)),
        None,
    )
    if diagnostic is not None:
        return diagnostic
    source = extracted[RelationKind.GIVEN]
    old_name = extracted[RelationKind.FROM]
    new_name = extracted[RelationKind.TO]
    will = extracted[RelationKind.SERVES]
    if not (
        isinstance(source, Clause)
        and isinstance(old_name, Name)
        and isinstance(new_name, Name)
        and isinstance(will, Will)
        and source.subject == old_name
    ):
        return Failed(
            "the related Forms do not satisfy the rename grammar",
            frozenset(value for value in extracted.values() if isinstance(value, Form)),
        )
    effect_clause = Clause(new_name, source.predicate)
    trace = RelationPreservationTrace(
        definition,
        source,
        effect_clause,
        (old_name, new_name),
        source.predicate,
    )
    return Effect(form, effect_clause, will, trace)


def read(form: CompositeForm, context: Context) -> ReadResult:
    """Give one Form a role through a concrete typed Reader."""

    if isinstance(context.reader, Inspector):
        return Inspection(context.reader, form, form.nodes, form.relations)
    if isinstance(context.reader, Interpreter):
        return _execute(form, context)
    return ExperimentalDiagnostic(
        DiagnosticKind.UNSUPPORTED_READER,
        "Context names no reading behavior for this Reader",
        frozenset({context.reader}),
    )


def check(effect: Effect, context: Context) -> CheckResult:
    """Assess Will separately using Ars-qualified grammatical equivalence."""

    if (
        effect.form.subject == effect.will.expected_subject
        and effect.form.predicate == effect.trace.source.predicate
    ):
        return Equivalent(
            context.equality.ars_name,
            effect.trace.source,
            effect.form,
            context.equality,
            effect.form.predicate,
        )
    return Counterexample(
        effect.will,
        effect,
        "the produced clause does not satisfy the declared rename contract",
    )
