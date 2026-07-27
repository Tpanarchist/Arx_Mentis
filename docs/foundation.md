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

Points connect through Lines to make Forms. Will names an intended Form or change. A
Spell is a Form containing the exact construction meant to produce that change. A
Cast performs the Spell within a Context. The Effect is the Form or change actually
produced. When the available Context cannot justify one outcome among real
alternatives, the result remains Potential. Related definitions, laws, Forms,
Spells, constructions, and demonstrations belong to an Ars.

## 2. The four sources

### 2.1 The Liberal Arts: organized powers of knowing

The Liberal Arts are ways of forming, testing, communicating, measuring, and
applying knowledge.

The Trivium concerns language and reason:

- Grammar — how Forms are made readable.
- Dialectic — what follows, what conflicts, and what remains unsettled.
- Rhetoric — how a Form acts upon a Reader within a Context.

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

Execution alone is insufficient. A procedure that runs without a declared intended
change is not yet a complete magical operation; the Effect must be compared with the
Will. A Spell may be exact while a Cast encounters a different Context. The language
must preserve the distinction between intended change, attempted construction, and
actual Effect.

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
| Smallest settled distinction | Point | A definite “here” rather than elsewhere; the smallest addressable distinction |
| Relationship or passage | Line | An ordered connection between Points |
| Structured information | Form | Points and Lines arranged into a readable whole |
| Intended change | Will | The Form or condition an operation is meant to produce |
| Exact construction | Spell | A Form containing the steps for causing the intended change |
| Performing the construction | Cast | Carrying out a Spell |
| Actual result | Effect | The Form or change produced by a Cast |
| Unsettled alternatives | Potential | Possible Forms together with what could settle among them |
| Conditions surrounding execution | Context | The Forms, Readers, permissions, conditions, and Potentials available to a Cast |
| Organized body of knowledge | Ars | Related definitions, postulates, laws, Forms, Spells, constructions, and demonstrations |

These terms are roles inside one system, not unrelated substances.

## 4. Point, Line, and Form

### 4.1 Point

A Point is not a tiny physical object. It is the simplest settled distinction the
system can address: here, not elsewhere. Ink, voltage, sound, memory, or another
medium may carry the distinction without defining its meaning.

A settled distinction requires real alternatives, an actual settlement, and
something capable of responding differently because of it.

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
same Form + examining Reader  → data
same Form + executing Reader  → Spell
```

Nothing in the underlying substance permanently marks it as instruction or datum.
Its role depends on how it is read within a Context.

## 5. Will, Spell, Cast, and Effect

### 5.1 Will

Will names the intended change. It is not merely a wish: it must distinguish the
desired outcome from meaningful alternatives. Without Will, success cannot be
distinguished from the fact that something happened.

### 5.2 Spell

A Spell is a Form placed in the role of exact transformational instructions. The
programmer supplies the steps; the machine does not secretly invent the method from
a stated desire.

A Spell should make clear the Forms it receives, the Will it serves, the
constructions it uses, the Context it requires, and the Effect it expects.

### 5.3 Cast

A Cast performs a Spell within an actual Context. The same Spell may produce
different Effects in different Contexts without changing what the Spell says:

```text
Spell + Context A → Effect A
Spell + Context B → Effect B
```

The difference must follow from declared Context, not hidden global behavior.

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

## 6. Potential

Potential is neither a third truth value nor null, unknown-as-a-value, or a hidden
default. It has exactly:

```text
Potential:
    options
    trigger
```

The options are Forms that could result. The trigger states what could legitimately
settle among them. An unsettled Potential has no selected result, and its Reader set
remains empty. When a Reader tries to branch on it, the system must settle it through
the declared trigger or preserve the boundary between unresolved Potential and
settled Form.

A valid settler must be capable of yielding another outcome. Evidence qualifies
when it could genuinely have pointed in another direction: different options make a
program succeed or fail, a construction preserves or loses meaning under different
rules, independent situations expose the same tension, or an observation could have
produced another result.

Ease of implementation, existing Python behavior, repetitions of one design episode,
and taste without an independent check do not qualify. A deadline or new Reader may
force a pressure-driven settlement, but that settlement still owes the system a real
trigger later.

## 7. Context

Context, rather than Circle, is the general execution boundary. Circle remains an
important geometric and magical Form.

A Context may contain the Reader, available Forms, permitted constructions, starting
conditions, orientation and location, relevant history, active Potentials, evidence
that can settle them, and limits on what the Cast may affect.

Context must remain explicit. If it becomes an invisible collection of host-language
variables, files, global state, and exceptions, the host language becomes the true
semantics of Arx Mentis. Context must also prevent an unresolved Potential from being
treated as settled merely because a later step expects an answer.

## 8. Ars

An Ars is the organized discipline itself, not merely a module that might store it.
It may contain Definitions, Postulates, Common Notions, Propositions, Forms, Spells,
Casts, Effects, Demonstrations, and Potentials.

The seven Liberal Ars are:

- **Ars Grammatica:** formation and reading of Forms; names, composition, syntax,
  and preservation of meaning through transformation.
- **Ars Dialectica:** inference, alternatives, contradiction, consistency, valid
  consequence, and unresolved Potential.
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
8. **Evidence over convenience:** implementation pressure cannot establish truth.
9. **Demonstrable effects:** an Effect is compared with Will and justified from the
   construction where such justification is claimed.
10. **No privileged metalayer:** Arx Mentis rules are Forms open to inspection and
    revision.
11. **Incompleteness is expected:** a system that represents its own instructions
    cannot settle every expressible claim.
12. **Symbolism must work:** geometric and magical names must correspond to real
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

Settlement selects among alternatives that could genuinely have resolved
differently:

```text
Potential + valid trigger → settled Form
```

A Cast may transform without settling any Potential. A Cast that claims settlement
must identify the trigger that made the alternatives real and the outcome warranted.

## 11. First executable proposition

The first experiment belongs to Ars Geometrica:

> Given a finite Line, construct an equilateral triangle upon it.

**Given:** a Line AB.

**Will:** construct an equilateral triangular Form on AB.

**Context:** AB exists; a circle may be constructed from a center and radius; a Line
may be constructed between two Points; equality of radii may be used in
demonstration; no orientation has been silently chosen.

**Spell:**

1. Construct a circle centered at A passing through B.
2. Construct a circle centered at B passing through A.
3. Find their intersection Point.
4. Construct a Line from that Point to A.
5. Construct a Line from that Point to B.

**Cast:** perform the construction within the declared Context.

**Effect:** a triangular Form whose three Lines are equal.

**Demonstration:** AB and AC are radii of the first circle and are equal. AB and BC
are radii of the second and are equal. Things equal to the same thing are equal to
one another. Therefore AB, AC, and BC are equal.

The two circles normally meet at two Points, one on each side of AB. The instruction
to find their intersection therefore contains:

```text
Potential:
    options:
        intersection on one side of AB
        intersection on the other side of AB
    trigger:
        orientation declared by Context
```

Without orientation, the system must not choose the visually upper Point. It must
preserve both valid Forms, return unresolved Potential, or receive a legitimate
orientation through Context.

This construction tests Point, Line, Form, Will, Spell, Cast, Effect, Context,
Potential without a default, non-destructive construction, Euclidean demonstration,
sacred geometry, organization through Ars Geometrica, and code/data identity because
the Spell remains inspectable.

## 12. Repository implications

The Stage 0 repository remains useful precisely because it has no implemented syntax
or semantics. The immediate learning order is now:

```text
formalize the first Forms
→ model one Spell as an inspectable Form
→ Cast it through a declared Context
→ produce and demonstrate its Effect
→ expose its hidden Potential
→ then design the source notation needed to express it
```

The first work belongs in a disposable experiment, not permanent language
semantics. It succeeds only if:

- the same Spell Form can be inspected as data and Cast as instructions;
- original Forms remain unchanged and the Effect is a new Form;
- Context contains every construction required by the Spell;
- the two-way intersection is represented without a default;
- the demonstration traces to declared Definitions, Postulates, and Common Notions;
- no Python behavior is mistaken for an Arx Mentis law.

Only then should the project decide which tokens, grammar, AST, or type system can
express the distinctions the experiment actually required.

## 13. Open questions

The foundation does not yet settle:

- whether Point is always binary or binary distinction arises through relations;
- whether Line includes direction, order, distance, or only relation;
- how Forms are represented while remaining equally available as code and data;
- how a Reader is represented within Context;
- how Will is compared with Effect;
- how failure, refusal, and incomplete Casts are represented;
- how Context declares permissions and outside resources;
- whether an Effect may act outside the information system;
- how demonstrations become executable or mechanically checkable;
- how one Ars imports or extends another;
- how Potential is carried across Contexts;
- surface syntax, type discipline, evaluation order, concurrency, memory behavior,
  and backend target.

These are named Potentials awaiting experiments capable of settling them.

## 14. Working thesis

Arx Mentis is a language of exact, inspectable construction. Its information takes
Form through Point and Line. Its operations are directed by Will, expressed as
Spells, performed as Casts within explicit Contexts, and judged by their Effects. Its
knowledge is organized into Ars and developed through definitions, postulates,
constructions, and demonstrations. It treats unresolved alternatives as Potential
rather than hiding them behind defaults, and it requires its own rules to remain
subject to the same discipline they impose.

## References

- Aleister Crowley, *Magick in Theory and Practice*, Introduction and Theorems.
- Euclid, *Elements*, Book I.
- Euclid, Book I, Proposition 1.
- The Seven Liberal Arts: Trivium and Quadrivium.
