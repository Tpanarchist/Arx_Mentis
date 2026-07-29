# Foundations of a Geometric Art of Magick

**Status:** Provisional foundation  
**Purpose:** Establish the present basis of Arx Mentis before surface syntax or
implementation choices are allowed to harden around it.

## 1. Central idea

Arx Mentis is conceived where four traditions meet:

- The Liberal Arts supply the fields and methods of knowledge.
- Crowleyan Magick supplies deliberate change directed by Will.
- Euclid's *Elements* supplies definitions, permitted constructions, and
  demonstration.
- Sacred geometry supplies a structural language of Point, Line, Form, relation,
  proportion, and transformation.

These are not themes placed over an ordinary programming language. Each contributes
a different part of the language's operation.

When an unresolved construction's alternatives are related by declared symmetry,
Potential preserves that structure until settlement makes a Point. Unequal causal
hypotheses, open propositions, hidden facts, and other incomplete knowledge are not
Potential merely because they remain unresolved. Points connect through Lines to make
Forms. Will supplies the criterion an acceptable Effect must satisfy. A Spell states
exact steps and that Will contract. An Interpreter elaborates those steps under an
Ars, discovering their capabilities rather than trusting a handwritten requirement
list. Cast produces an Effect, Refusal, or Failure. Demonstration supplies evidence
of Conformity. Related definitions, equality, transformation groups, Postulates,
Forms, Spells, and demonstrations belong to an Ars.

## 2. The four sources

### 2.1 The Liberal Arts: organized powers of knowing

The Liberal Arts are ways of forming, testing, communicating, measuring, and
applying knowledge.

The Trivium concerns language and reason:

- Grammar — how Forms are made readable.
- Dialectic — what follows, what conflicts, and what remains unsettled.
- Rhetoric — how a Form acts upon an Audience within a Context.

The Quadrivium concerns number and proportion:

- Arithmetic — discrete quantity.
- Geometry — magnitude and Form in space.
- Music — proportion and order through time.
- Astronomy — cycles, motion, and systems observed as wholes.

Each becomes an Ars: an organized body of knowledge that can be defined, practiced,
extended, and tested.

### 2.2 Crowleyan Magick: intentional change

Arx Mentis takes Magick operationally as the science and art of causing change in
conformity with Will:

- Will declares the intended change.
- Spell gives the exact means.
- Cast performs those means under actual conditions.
- Effect is what actually happens.

Execution alone is insufficient. A procedure without a declared acceptance criterion
is not yet a complete magical operation; Effect must be assessed against Will within
Context. A Spell may be exact while a Cast refuses a missing capability, fails a
permitted construction, or produces a nonconforming Effect. These distinctions must
remain visible.

### 2.3 Euclid's *Elements*: construction with reasons

Arx Mentis adopts Euclid's progression from definitions, postulates, and common
notions to increasingly complex constructions and demonstrations:

- A Definition fixes how a term is being used.
- A Postulate states a primitive construction the Ars permits.
- A Common Notion states a rule shared across relevant constructions.
- A Proposition names something to construct or demonstrate.
- A Spell gives the exact construction.
- A Cast performs it.
- An Effect supplies the resulting Form.
- A Demonstration shows why the Effect has the claimed properties.

The aim is not to make every program resemble a geometric proof. It is to prevent
hidden operations from appearing midway through a construction. Every complex power
must ultimately rest on declared primitive powers.

### 2.4 Sacred geometry: structure with meaning

Sacred geometry contributes the idea that construction, proportion, boundary,
center, and transformation can carry meaning without ceasing to be exact. It is not
decoration or a shortcut around proof.

- Point — settled distinction and position.
- Line — relation, direction, or passage.
- Form — an intelligible arrangement of Points and Lines.
- Angle — difference between directions.
- Ratio — proportion between Forms or parts of Forms.
- Symmetry — a transformation that preserves something.
- Figure — a bounded Form.
- Construction — exact steps that produce a Form.
- Demonstration — a showing that the construction has the claimed properties.

These concepts may become language features only where experiments show that they
perform real work.

## 3. Core terms

| Foundation | Arx Mentis term | Meaning |
| --- | --- | --- |
| Symmetry-indexed open or settled construction | Distinction[A] | The provisional phased family `Potential[A]` or `Point[A]` |
| Symmetry-indexed unresolved construction | Potential[H, K, A] | An equivariant family `K → A` over an `H`-frame, plus partial settlement by evidence |
| Settled distinction | Point[A] | A selected `A` together with settlement evidence or provenance |
| Relationship or passage | Line | A connection between Points; whether direction is intrinsic remains experimental |
| Structured information | Form | Points and Lines arranged into a readable whole |
| Acceptance criterion | Will[E] | A predicate over Context and Effect `E` |
| Exact construction | Spell[I, E] | A Form containing stated steps and a Will contract; requirements are derived by elaboration |
| Capability-checked interpretation | Cast | Interpretation of a Spell within explicit Context |
| Execution outcome | CastResult[E] | Produced Effect, principled Refusal, or construction Failure |
| Actual result | Effect | The Form or change actually produced by a Cast |
| Evidence of acceptance | Conformity | Demonstration or Counterexample from a terminating Will check |
| Conditions surrounding execution | Context | Bindings, capabilities, choice-frames, Interpreter, and conditions |
| Organized body of knowledge | Ars | Definitions, relation laws, postulates, Forms, Spells, and demonstrations |

These terms are roles inside one system, not unrelated substances.

## 4. Point, Line, and Form

### 4.1 Distinction, Potential, and Point

Within the currently evidenced symmetry-indexed scope, Potential and Point are the
open and settled phases of one typed family:

```text
Distinction[A] = Potential[A, K] | Point[A]
Potential[A, K] ──settlement──▶ Point[A]
```

A Potential carries an equivariant family and partial settlement rule. A Point
carries the selected value and evidence or provenance of choosing a frame. A
geometric Point is therefore `Point[Location]`; the word does not make every kind of
information an untyped geometric location.

A settled distinction still requires real alternatives, actual settlement, and
something capable of responding differently because of it. Ink, voltage, sound,
memory, or another medium may carry the distinction without defining its meaning.

This phased family is not a universal model of unresolvedness. Experiment 006 has a
settled event, one definite but unavailable world cause, and several unequal
Reader-relative causal hypotheses. Forcing those hypotheses into a transitive frame
destroys their declared structure.

### 4.2 Line

One Point gives position. A second makes relationship possible. A Line makes that
relationship explicit. A Line may carry connection, direction, order, distance,
dependency, or passage from one Form to another.

The foundation does not yet decide which properties belong to Line itself and which
require additional Forms. It must not inherit the answer from a host language's
lists, graphs, or object references.

### 4.3 Form

A Form is an intelligible arrangement of Points and Lines. Ordinary data,
instructions, definitions, arguments, proofs, Effects, and Spells are all Forms:

```text
same Form + Inspector    → data role
same Form + Interpreter → Spell role
same Form + Audience    → rhetorical Effect
```

Nothing in the underlying substance permanently marks it as instruction or datum.
Its role depends on how it is read within a Context.

### 4.4 Relations are typed

One undifferentiated equality relation is insufficient. The foundation distinguishes
at least:

| Relation | Meaning |
| --- | --- |
| Same | The same occurrence or identity |
| Equal | Equal under laws declared by an Ars |
| Congruent | Equivalent geometric Form under permitted transformations |
| Equivalent | The same relevant meaning or behavior within Context |
| Conforms | An Effect satisfies a Will within Context |

Thus AB and AC in Euclid I.1 are different Lines whose lengths are Equal. Source
preservation is a Same/provenance claim. Meaning preservation is an Ars-specific
Equivalent relation. Every relation called equality must declare its laws rather
than silently inherit reflexivity, symmetry, or transitivity from Python.

## 5. Will, Spell, Cast, and Effect

### 5.1 Will

Will is an acceptance predicate over Effect within Context:

```text
Conforms(W, E, C) iff W(C, E)
```

This remains the working acceptance role, not a decision that every source target is
only a Will. Experiment 007 derives an AcceptanceRule and an ActionPolicy separately
from one neutral TargetForm. Targets with the same acceptance rule can guide different
paths, and targets with the same guidance can impose different thresholds. The
experiment therefore keeps acceptance and guidance distinct while leaving open
whether a future Reader derives either role from a shared Form.

A single target Form is one special case. The Euclid I.1 Will accepts any Effect
that is a triangle on the given AB whose three side-lengths are Equal. Without Will,
successful construction cannot be distinguished from conformity.

### 5.2 Spell

A Spell is a Form placed in the role of exact transformational instructions. The
programmer supplies the steps; the machine does not secretly invent the method from
a stated desire.

A Spell states the Forms it receives, exact steps, and Will contract. It does not
authoritatively declare hidden requirements. The Interpreter elaborates each step
under the current Ars:

```text
elaborate(Spell, Ars) → ElaboratedSpell | Refusal
```

The elaborated result may record derived capabilities as explanation or cache. Adding
a Postulate must allow the same unchanged Spell to elaborate further.

### 5.3 Cast

A Cast is capability-checked interpretation of a Spell within actual Context. It is
total at the experimental boundary even when a construction cannot run:

```text
CastResult[E] = Produced(E) | Refused(MissingCapability) | Failed(ConstructionFailure)
```

Unknown instructions are Refused when the Interpreter has no corresponding
construction. A permitted construction that cannot produce its required Form is a
Failure. Neither becomes an accidental Python exception. Different results must
follow from declared Context rather than hidden global behavior.

### 5.4 Effect

An Effect is the actual result of a Cast. Arx Mentis begins with non-destructive
transformation:

```text
source Form ──Cast──▶ Effect
     │
     └── remains available
```

Each step produces a new Form rather than silently replacing its source. Possible
outside action remains a separate question.

### 5.5 Conformity

Construction and assessment remain separate. A Will belongs to a terminating,
executable fragment declared by its Ars:

```text
check(Will, Effect, Context) → Conforms | Counterexample
```

ADR 0009 accepts only this observable separation: producing a result does not perform
its acceptance check, and checking acceptance does not produce or repair the result.
The name `Will`, checking phase, representation, universality, and effect on control
flow remain provisional.

A Demonstration is evidence that Will holds for the actual Effect, not prose attached
afterward. When Effect is Potential, checking is lifted pointwise. An invariant Will
produces a constant truth family and therefore ordinary Conforms or Counterexample
without settling Effect. A non-invariant Will produces a frame-dependent truth family
and can be rejected as a specification error before Cast.

A general Proposition is distinct:

```text
prove(Proposition, Context) → Demonstration | Refutation | Open
```

`Open` is lack of proof, not Potential in the constructed object.

## 6. Potential

Potential is neither a third truth value nor null, unknown-as-a-value, or a hidden
default. It applies when the unresolved alternatives are related by a declared
symmetry. Across the three current positive experiments, its approximate type is:

```text
Potential[H, K, A]:
    family: K → A
    settlement: Evidence ⇀ K
```

The ambient transformation group `G` belongs to the Ars. The stabilizer `H` of the
givens is derived from `G`; it is not authored per Potential. In the current regular
examples, `K` is an `H`-torsor for a default-free choice. Whether more general actions,
multiple orbits, or partial transformation relations belong under the same term
remains open. A symmetry-indexed family must be equivariant:

```text
p(h · k) = h · p(k)
```

Possible results are the derived image of this family, so an `options` field is
redundant. Composition is functional:

```text
map(f, p)(k) = f(p(k))
shared(p, q)(k) = (p(k), q(k))
twisted(p, q, t)(k) = (p(k), q(t(k)))
independent(p, q)(k, l) = (p(k), q(l))
```

A construction may map uniformly through Potential without inspecting or settling
its frame. A Ward is therefore mechanical: invariant predicates collapse safely;
non-invariant predicates remain frame-dependent and may not be collapsed into a
Boolean or continuation without evidence.

A valid settler must be capable of yielding another outcome. Evidence qualifies
when it could genuinely have pointed in another direction: different options make a
program succeed or fail, a construction preserves or loses meaning under different
rules, independent situations expose the same tension, or an observation could have
produced another result.

Ease of implementation, existing Python behavior, repetitions of one design episode,
and taste without an independent check do not qualify. A deadline or new Witness may
force a pressure-driven settlement, but that settlement still owes the system a real
trigger later.

The default test has two independent gates. Let `H` be the stabilizer of the givens
inside the Ars's ambient group. An option not fixed by `H` cannot be constructed from
those givens by equivariant operations. But fixed does not imply constructible:

```text
legitimate default iff FixedBy(H) and ConstructibleFrom(Postulates)
```

The midpoint of AB is fixed by reflection yet unavailable before a midpoint
construction has been derived. Equivariance of every permitted construction is the
hypothesis that makes the fixed-point obstruction valid. An Ars must declare and
test it. If `H` acts trivially on a multi-option space, the ambient group may be too
small and the test is uninformative rather than permissive.

## 7. Context

Context, rather than Circle, is the general execution boundary. Circle remains an
important geometric and magical Form.

A Context may contain bindings, capabilities, shared choice-frames, Interpreter,
conditions, relevant history, active Potentials, and evidence supplied by Witnesses.
Capabilities name primitive constructions; elaboration derives those required by a
Spell's stated steps under the current Ars.

Context must remain explicit. If it becomes an invisible collection of host-language
variables, files, global state, and exceptions, the host language becomes the true
semantics of Arx Mentis. Context must also prevent an unresolved Potential from being
treated as settled merely because a later step expects an answer.

Reader is a family of typed roles rather than one concrete type:

- **Interpreter:** maps a Form in Spell role to permitted constructions.
- **Inspector:** examines a Form without executing it.
- **Audience:** receives or is influenced by a rhetorical Form.
- **Witness:** supplies or observes evidence capable of settlement.

## 8. Ars

An Ars is the organized discipline itself, not merely a module that might store it.
At minimum it declares its Forms, permitted constructions with equivariance laws,
qualified equality, ambient transformation group, terminating Will fragment, and
Bridges. It may also contain Definitions, Common Notions, Propositions, Spells,
Casts, Effects, Demonstrations, and Potentials.

The transformation group follows the Erlangen principle: it determines geometric
congruence, supplies the ambient action from which stabilizers and Potentials are
derived, and governs default legitimacy. Choosing it too small manufactures false
defaults; choosing it too large erases structure that should survive.

Forms cross between Artes only through an explicit Bridge. A Bridge must preserve
the relevant qualified equality, commute with constructions, and respect the
transformation action. Euclid I.1 already needs the length Bridge from geometric
Lines to arithmetic magnitudes; Common Notion 1 operates on those magnitudes, not on
Line identity.

The seven Liberal Ars are:

- **Ars Grammatica:** formation and reading of Forms; names, composition, syntax,
  and preservation of meaning through transformation.
- **Ars Dialectica:** inference, alternatives, contradiction, consistency, valid
  consequence, symmetric Potential, unequal attribution, and other unresolved states.
- **Ars Rhetorica:** Effects of Forms upon Readers; interpretation, presentation,
  persuasion, translation, and preservation or distortion of meaning.
- **Ars Arithmetica:** discrete quantity, number, equality, ratio, combination, and
  separation.
- **Ars Geometrica:** Point, Line, magnitude, boundary, orientation, construction,
  transformation, symmetry, and proof through Form.
- **Ars Musica:** ratio and Form through time; rhythm, interval, harmony, repetition,
  phase, and synchronization.
- **Ars Astronomica:** cycles, motion, recurrence, observation, prediction, and the
  behavior of systems larger than one immediate Cast.

These may eventually form the standard library only after their operations have
been earned through concrete constructions.

## 9. Governing principles

1. **One substance:** instructions, data, definitions, and Effects are all Forms.
2. **Role through reading:** a Form becomes a Spell when read as exact instructions.
3. **Declared Will:** a magical operation names the change it intends.
4. **Exact construction:** a Spell supplies steps instead of hiding its method.
5. **Explicit Context:** every Cast occurs under named, examinable conditions.
6. **Preserved source:** transformation creates a new Form without silently
   destroying the old one.
7. **No false settlement:** Potential has no default result and no null substitute.
8. **No accidental choice:** when declared semantics provide no discriminator among
   distinct admissible alternatives, incidental representation order cannot supply
   one. Declared sequence, priority, canonicalization, or policy remains legitimate.
9. **Evidence over convenience:** implementation pressure cannot establish truth.
10. **Demonstrable effects:** an Effect is compared with Will and justified from the
   construction where such justification is claimed.
11. **No privileged metalayer:** Arx Mentis rules are Forms open to inspection and
    revision.
12. **Incompleteness is expected:** a system that represents its own instructions
    cannot settle every expressible claim.
13. **Symbolism must work:** geometric and magical names must correspond to real
    language behavior.

These principles remain provisional until executable experiments expose where they
succeed, conflict, or require correction.

## 10. Transformation and settlement

Transformation and settlement are distinct.

A deterministic Spell reorganizes, reveals, combines, or translates existing Forms:

```text
existing Forms → exact steps → new Form
```

It may make information newly useful without creating a genuinely new alternative
inside a closed system.

Settlement chooses a frame basepoint using legitimate Witness evidence:

```text
Potential[H, K, A] + Evidence ⇀ K → Point[A, SettlementEvidence]
```

A Cast may transform without settling any Potential. A Cast that claims settlement
must identify the trigger that made the alternatives real and the outcome warranted.

## 11. First executable proposition

The first experiment belongs to Ars Geometrica:

> Given a finite Line, construct an equilateral triangle upon it.

**Given:** a Line AB.

**Will:** accept an Effect when it is a triangle containing AB and its three
side-lengths are Equal under Ars Geometrica.

**Initial Ars:** circle and Line constructions are Postulates with equivariance
evidence. No circle-intersection or continuity construction is declared. Ars
Geometrica supplies an ambient group containing reflection across AB and qualified
geometric equality.

**Spell:**

1. Construct a circle centered at A passing through B.
2. Construct a circle centered at B passing through A.
3. Find their intersection Point.
4. Construct a Line from that Point to A.
5. Construct a Line from that Point to B.

**First elaboration:** interpret the unchanged steps within the initial Ars. The first
two steps are licensed. At `intersect_circles`, elaboration returns:

```text
Refused:
    missing capability: circle-circle intersection
```

This Refusal is the first successful observation of the experiment. Euclid's stated
postulates license drawing the circles but do not establish that their intersection
exists. The missing operation must be made explicit rather than inherited from the
diagram.

**Second Ars:** add a circle-circle intersection or continuity Postulate. The same
unchanged Spell now elaborates, and its requirements are derived from the interpreted
steps. Cast constructs an Effect whose Form remains a Potential triangle.

**Effect:** a triangular Form whose three side-lengths are Equal.

**Demonstration:** the length of AB equals the length of AC because both are radii of
the first circle. The length of AB equals the length of BC because both are radii of
the second. Under the declared transitivity law, the three lengths are Equal. The
Demonstration is the evidence that the Effect Conforms to Will.

The two circles normally meet at two Points, one on each side of AB. The instruction
to find their intersection therefore contains:

```text
Potential[H, K, Triangle]:
    family: K → Triangle
    settlement: Witness evidence ⇀ K
```

Here `H` is the stabilizer of A, B, and AB, derived from the Ars's ambient group, and
`K` is its two-frame torsor. Without Witness evidence, the system does not choose a
basepoint. Line and triangle construction map uniformly through the family. Direct
and twisted sharing each yield two related joint results; independent torsors yield
four. Context transfer without a Frame preserves the family.

Direction and plane chirality form one frame-placement experiment:

```text
side = segment direction XOR plane chirality
```

Flipping either component changes side; flipping both preserves it. The experiment
compares placing direction in Line, Context, or Potential's frame and favors the
derived Potential frame for I.1 because it carries one shared or twisted relation
across segments without a fresh arbitrary left/right declaration.

Finally, `check` lifts the equilateral Will through the Potential triangle. Reflection
preserves the property, so the resulting truth family is constant and collapses to
Conforms with a Demonstration while the triangle remains unsettled. The length Bridge
translates geometric Lines into arithmetic magnitudes and supplies its equality,
commutation, and equivariance obligations. A side-specific Will produces a
nonconstant truth family and is diagnosed as non-invariant before Cast.

This construction tests derived capability Refusal, phased Point/Potential,
equivariant construction, shared/twisted/independent composition, the Ward, default
legitimacy, frame placement, qualified equality, Bridges, and Conformity without
settlement.

## 12. Repository implications

The Stage 0 repository remains useful precisely because it has no implemented syntax
or semantics. The immediate learning order is now:

```text
formalize phased Distinctions, Ars declarations, and typed relations
→ elaborate exact steps and derive their capabilities
→ refuse the first elaboration at the hidden intersection operation
→ add the missing Postulate explicitly
→ lift construction through the derived reflection torsor
→ check invariant Will without settling Effect
→ then design the source notation needed to express it
```

The first work belongs in a disposable experiment, not permanent language
semantics. It succeeds only if:

- the Spell contains no authoritative hand-written requirements;
- elaboration discovers the missing intersection from the Ars;
- original Forms remain unchanged and the Effect is a new Form;
- missing capability produces Refusal rather than hidden construction or exception;
- direct, twisted, and independent families compose with the required relationships;
- construction proceeds through Potential without frame inspection;
- the Ars declares its group, qualified equality, equivariant constructions, Will
  fragment, and Bridge obligations;
- invariant Conformity is decidable without settlement while non-invariant Will is
  exposed as frame-dependent;
- legitimate defaults pass both fixed-point and constructibility gates;
- no Python behavior is mistaken for an Arx Mentis law.

Only then should the project decide which tokens, grammar, AST, or type system can
express the distinctions the experiment actually required.

## 13. Open questions

The foundation does not yet settle:

- whether Line includes direction, order, distance, or only relation;
- how Forms are represented while remaining equally available as code and data;
- how Interpreter, Inspector, Audience, and Witness compose;
- how Will predicates and Conformity evidence participate in type checking;
- which distinctions among Refusal, Failure, and incomplete construction survive
  independent experiments;
- how Context declares permissions and outside resources;
- whether an Effect may act outside the information system;
- how demonstrations become executable or mechanically checkable;
- how one Ars imports or extends another;
- how structured choice-spaces and Frames are represented across Contexts;
- whether observability, availability, resolution, verification, and construction
  success are independent dimensions in the eventual type structure;
- whether one construction may retain both a settled public outcome and an
  unresolved internal mechanism, and how either relates to Effect;
- how unequal evidence, partial narrowing, probability, multiple orbits, or the
  absence of a meaningful transformation action are represented;
- whether probability is always exact and declared or may be inferred, where a
  production kernel belongs, and how samples, reports, stopping rules, and
  precommitted plans are represented;
- how causally distinct mechanisms with the same public distribution remain
  distinguishable to a privileged record without overstating an observer's
  attribution;
- whether prospective revision is ordinary construction, Cast, interpretation, or
  another operation, and whether a model is Form, Ars-local theory, or a contextual
  reading;
- whether model lineage participates in identity or provenance only, and how
  supersession, correction, and counterfactual replay affect those relations;
- how calibration evidence, independent evaluation, assessment rules, and adaptive
  interventions remain distinct when a model changes the Context it describes;
- whether model adoption is a Reader-relative stance, Context authority, capability,
  binding, interpretation, or another relation, and how purpose and scope constrain
  it;
- whether operational commitment can coexist with unresolved epistemic comparison
  without becoming settlement or truth assertion;
- how live-linked and snapshot authority, revocation, expiry, and prospective model
  switching relate to source availability and historical attribution;
- how a definite world state relates to Reader-relative knowledge and attribution;
- how source Form, encoded carrier, interpreted artifact, active mechanism,
  execution, and outcome relate without becoming nominal aliases;
- whether release changes lifecycle, scope, availability, or only dependency, and
  where derivation provenance belongs;
- whether local value and shared historical derivation require separate equality or
  identity relations;
- whether distributed stress belongs to Context, Effect, or another state record and
  how displacement, release, dissipation, rupture, and oscillation compose;
- how triggers participate in causation without being treated as complete causes;
- how mechanical resolution, declared acceptance, and progress relate without being
  collapsed into one success state;
- surface syntax, type discipline, evaluation order, concurrency, memory behavior,
  and backend target.

These are open questions awaiting experiments capable of resolving them. They are
not automatically values of the `Potential` type.

## 14. Working thesis

Arx Mentis is a language of exact, inspectable construction. Symmetry-indexed
constructions may move from structured Potential to settled Point; unresolvedness in
general has no single accepted representation. Lines relate Points into Forms.
Interpreters
elaborate Spells and perform capability-checked Casts in explicit Contexts, producing
Effects, Refusals,
or Failures. Will supplies a contract and Demonstration supplies evidence of
Conformity. Ars declare their own relations, laws, Postulates, and proofs. Symmetry
correlates choices across composition rather than decorating them.

## References

- Aleister Crowley, *Magick in Theory and Practice*, Introduction and Theorems.
- Euclid, *Elements*, Book I.
- Euclid, Book I, Proposition 1.
- Vincenzo De Risi, [“Intersections and Continuity in Euclid's
  Elements”](https://pure.mpg.de/rest/items/item_3288290_17/component/file_3323098/content).
- Mathlib, [torsors and affine spaces](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/AffineSpace/Defs.html).
- The Stacks Project, [torsors](https://stacks.math.columbia.edu/tag/0497).
- Ralph Freese, [universal algebra notes](https://math.hawaii.edu/~ralph/Classes/619/UA-Valeriote.pdf).
- The Seven Liberal Arts: Trivium and Quadrivium.
