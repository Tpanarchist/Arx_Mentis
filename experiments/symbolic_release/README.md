# State Zero Experiment 008: Symbolic Encoding and Release

**Status:** Disposable evidence experiment. Nothing here is package API or accepted
language semantics.

## Question

What must an intermediate representation preserve so that a source can be encoded,
released, and later acted upon without the carrier becoming identical to the source,
its interpretation, its activation, or its eventual outcome?

The motivating source is Stephen Mace's
[*Sorcery as Virtual Mechanics*](https://www.scribd.com/doc/96245037/37606530-Stephen-Mace-Sorcery-as-Virtual-Mechanics).
This experiment extracts only the neutral mechanics of symbolic mediation. It makes
no claim that sigils act, symbols contain energy, or occult causation occurs.

## Assumptions

- A finite deterministic route system can isolate representation, interpretation,
  activation, execution, and provenance without external I/O or physical claims.
- Frozen Python records are disposable carriers, not proposed runtime values.
- Derivation records are trusted experimental inputs, not cryptographic proofs.
- Release means execution stops depending on direct source availability; it does not
  erase derivation history.

## Models

1. **Transparent encoding** preserves enough fields for exact reconstruction.
2. **Compiled encoding** retains action selection but omits acceptance and
   explanation. It is operationally sufficient and semantically incomplete.
3. **Context-keyed encoding** lets navigation and audit decoders read one carrier as
   separate policy and acceptance artifacts.
4. **Opaque inert encoding** has a derived carrier but no supported reading or
   activation.
5. **Lossy encoding** maps distinct sources to one carrier and returns an explicit
   collision rather than semantic equality.
6. **Forged encoding** has a valid-looking shape but no declared derivation.

The execution boundary is deliberately staged:

```text
SourceForm -> Carrier -> Interpretation -> Activation -> Execution -> Outcome
```

No stage silently performs the next. A pending carrier whose source disappears
before compilation returns `MissingDependency`; a compiled policy continues after
release and retains provenance.

## Success signal

The experiment succeeds if executable witnesses separate source, carrier, meaning,
activation, execution, outcome, and history; show that equal outcomes do not reveal
their decoding; preserve shared-source correlation; expose accidental local equality;
and return owned results for unsupported, forged, colliding, inert, and prematurely
released cases.

## Executable witness

```powershell
.venv\Scripts\python.exe -m experiments.symbolic_release
.venv\Scripts\python.exe -m pytest tests/experiments/test_symbolic_release.py
```

## Result and boundary

A symbol does not interpret or execute itself. One source can produce separately
owned policy and acceptance artifacts, and one carrier can receive different lawful
roles under declared keys. A compiled artifact may remain executable after source
release without being an exact reconstruction. Provenance survives that release, but
local value and historical origin remain different comparisons.

This is a second direct witness for contextual reading after Grammatica and a second
for source-independent derived execution after Actualization. Neither reaches the
three-domain gate. The result does not decide whether encoding is a Cast, whether
activation is general semantics, or how any eventual language represents these
stages.

## Deletion or promotion path

Delete the experiment if a later counterexample cannot preserve the staged
boundaries or if derivation history is carrying semantic content accidentally.
Promote only backend-neutral behavior that recurs in three independent domains with
a negative boundary. Never promote these Python records, route names, symbolic tags,
or harness diagnostics.

