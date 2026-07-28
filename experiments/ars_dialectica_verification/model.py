"""Local Forms for the disposable Ars Dialectica verification probe."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Form:
    __slots__ = ()


@dataclass(frozen=True, slots=True)
class Atom(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Implication(Form):
    antecedent: Atom
    consequent: Atom


type Proposition = Atom | Implication


class RuleName(Enum):
    MODUS_PONENS = "modus-ponens"


@dataclass(frozen=True, slots=True)
class Capability(Form):
    name: str


@dataclass(frozen=True, slots=True)
class Rule(Form):
    name: RuleName
    capability: Capability


@dataclass(frozen=True, slots=True)
class InferenceInstruction(Form):
    rule: RuleName
    premises: tuple[Proposition, ...]
    conclusion: Proposition


@dataclass(frozen=True, slots=True)
class Will(Form):
    description: str
    expected: Proposition


@dataclass(frozen=True, slots=True)
class Spell(Form):
    name: str
    starting_premises: frozenset[Proposition]
    instructions: tuple[InferenceInstruction, ...]
    will: Will


@dataclass(frozen=True, slots=True)
class EqualityDeclaration(Form):
    ars_name: str
    subject: str
    reflexive: bool
    symmetric: bool
    transitive: bool


@dataclass(frozen=True, slots=True)
class WillLanguage(Form):
    name: str
    predicates: frozenset[str]
    terminating: bool


@dataclass(frozen=True, slots=True)
class Ars(Form):
    name: str
    rules: frozenset[Rule]
    equality: EqualityDeclaration
    will_language: WillLanguage


@dataclass(frozen=True, slots=True)
class Context(Form):
    ars: Ars
    premises: frozenset[Proposition]
    permissions: frozenset[Capability]
    refuted: frozenset[Proposition] = frozenset()


@dataclass(frozen=True, slots=True)
class ElaboratedSpell(Form):
    spell: Spell
    ars: Ars
    required_capabilities: frozenset[Capability]


@dataclass(frozen=True, slots=True)
class ElaborationRefusal(Form):
    spell: Spell
    missing_rule: RuleName
    step_index: int
    elaborated_prefix: int


type ElaborationResult = ElaboratedSpell | ElaborationRefusal


@dataclass(frozen=True, slots=True)
class InferenceApplication(Form):
    rule: RuleName
    premises: tuple[Proposition, ...]
    conclusion: Proposition


@dataclass(frozen=True, slots=True)
class Demonstration(Form):
    starting_premises: frozenset[Proposition]
    applications: tuple[InferenceApplication, ...]
    conclusion: Proposition


@dataclass(frozen=True, slots=True)
class Effect(Form):
    source: Spell
    conclusion: Proposition
    demonstration: Demonstration


@dataclass(frozen=True, slots=True)
class Refused(Form):
    missing_capability: Capability
    reason: str


class FailureKind(Enum):
    MISSING_PREMISE = "missing-premise"
    INAPPLICABLE_RULE = "inapplicable-rule"


@dataclass(frozen=True, slots=True)
class Failed(Form):
    kind: FailureKind
    reason: str
    related: frozenset[Proposition]


type CastResult = Effect | Refused | Failed


@dataclass(frozen=True, slots=True)
class VerifiedDemonstration(Form):
    demonstration: Demonstration
    checked_premises: frozenset[Proposition]
    checked_applications: int
    checked_conclusion: Proposition


@dataclass(frozen=True, slots=True)
class InvalidDemonstration(Form):
    reason: str
    step_index: int | None


type VerificationResult = VerifiedDemonstration | InvalidDemonstration


@dataclass(frozen=True, slots=True)
class Conforms(Form):
    effect: Effect
    will: Will
    law: EqualityDeclaration


@dataclass(frozen=True, slots=True)
class Counterexample(Form):
    effect: Effect
    will: Will
    reason: str


type ConformityResult = Conforms | Counterexample


@dataclass(frozen=True, slots=True)
class Refutation(Form):
    proposition: Proposition
    reason: str


@dataclass(frozen=True, slots=True)
class Open(Form):
    proposition: Proposition
    reason: str


type PropositionResult = Demonstration | Refutation | Open


MODUS_PONENS_CAPABILITY = Capability("apply-modus-ponens")
MODUS_PONENS_RULE = Rule(RuleName.MODUS_PONENS, MODUS_PONENS_CAPABILITY)
DIALECTICAL_EQUALITY = EqualityDeclaration(
    "Ars Dialectica",
    "structural equality of declared finite propositions",
    True,
    True,
    True,
)
FINITE_WILL_LANGUAGE = WillLanguage(
    "exact finite proposition",
    frozenset({"effect conclusion equals expected proposition"}),
    True,
)


@dataclass(frozen=True, slots=True)
class Experiment(Form):
    spell: Spell
    ars: Ars
    context: Context
    rain: Atom
    wet: Atom
    bloom: Atom
    sprout: Atom


def elaborate(spell: Spell, ars: Ars) -> ElaborationResult:
    """Derive capabilities from the Spell's instructions and the selected Ars."""

    rules = {rule.name: rule for rule in ars.rules}
    required: set[Capability] = set()
    for index, instruction in enumerate(spell.instructions):
        rule = rules.get(instruction.rule)
        if rule is None:
            return ElaborationRefusal(spell, instruction.rule, index, index)
        required.add(rule.capability)
    return ElaboratedSpell(spell, ars, frozenset(required))


def make_experiment() -> Experiment:
    rain = Atom("rain")
    wet = Atom("wet")
    bloom = Atom("bloom")
    sprout = Atom("sprout")
    rain_implies_wet = Implication(rain, wet)
    wet_implies_bloom = Implication(wet, bloom)
    premises: frozenset[Proposition] = frozenset(
        {rain, rain_implies_wet, wet_implies_bloom}
    )
    spell = Spell(
        "derive bloom in two steps",
        premises,
        (
            InferenceInstruction(
                RuleName.MODUS_PONENS,
                (rain, rain_implies_wet),
                wet,
            ),
            InferenceInstruction(
                RuleName.MODUS_PONENS,
                (wet, wet_implies_bloom),
                bloom,
            ),
        ),
        Will("derive bloom", bloom),
    )
    ars = Ars(
        "Ars Dialectica",
        frozenset({MODUS_PONENS_RULE}),
        DIALECTICAL_EQUALITY,
        FINITE_WILL_LANGUAGE,
    )
    context = Context(ars, premises, frozenset({MODUS_PONENS_CAPABILITY}))
    return Experiment(spell, ars, context, rain, wet, bloom, sprout)
