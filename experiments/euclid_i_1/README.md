# Euclid I.1 equivariant-family experiment

**Question:** Can interpretation discover Euclid's hidden continuity assumption, and
can the remaining construction pass lawfully through an unsettled reflection frame
while conformity is decided without settlement?

## Model under test

- A Spell states only inputs, steps, and Will. `elaborate(Spell, Ars)` derives
  requirements by interpreting each step under the Ars.
- Ars Geometrica declares its Forms, constructions, qualified equality, ambient
  transformation group, finite Will fragment, and Bridges.
- The stabilizer `H` is derived from the givens. Reflection across AB fixes those
  givens, so the two intersection frames form an `H`-torsor.
- `Potential(family, settlement)` stores an equivariant family `K → A`; possible
  results are its derived image, not a stored option list.
- Lines and the triangle are constructed uniformly throughout that family without
  selecting a frame.

## Success signal and observed results

- The unchanged Spell refuses elaboration at intersection under the initial Ars,
  after two successfully interpreted circle steps. Adding an explicit intersection
  Postulate makes the same Spell elaborate and records derived requirements.
- Direct sharing and twisted sharing each have two joint results but encode different
  relationships. Independent frame keys yield four.
- Direction and plane chirality combine by XOR: flipping either flips side, while
  flipping both preserves it. The effective shared side belongs in Potential's
  derived frame rather than a fresh left/right declaration.
- The equilateral Will is reflection-invariant. Pointwise checking yields a constant
  true family, so Conformity is demonstrated while the triangle remains Potential.
- “Apex on the positive side” is not invariant. Validation detects that before Cast,
  and lifted checking produces a nonconstant Potential of truth values.
- Default legitimacy has two gates: fixed by the stabilizer and constructible from
  declared Postulates. An intersection branch fails the first; the midpoint passes
  the first but fails the second before a midpoint construction is added.
- The equality proof crosses an explicit length Bridge from Ars Geometrica to Ars
  Arithmetica. The Bridge declares equality preservation, commutation with
  constructions, and equivariance.

## Assumptions

- The finite symbolic `Z/2` action represents only the reflection relevant to I.1.
- Equivariance evidence is declared and exercised, not mechanically proved by a
  general theorem prover.
- The Will fragment contains two terminating symbolic predicates only.
- Python graphs and frozen sets are disposable carrier choices.

## Failure conditions exercised

- Intersection elaborates before its Postulate exists.
- Requirements appear authoritatively in the Spell.
- Shared, twisted, and independent composition have the wrong cardinalities or
  relationships.
- Lifted Line construction forces settlement.
- A Frame-free Context selects a result.
- Simultaneously flipping direction and chirality changes side.
- A non-invariant Will collapses to an ordinary Boolean.
- Fixed-point status alone makes an unavailable construction a legitimate default.

Run with:

```console
python -m experiments.euclid_i_1
python -m pytest tests/experiments/test_euclid_i_1.py
```

## Deletion or promotion path

Delete any representation that fails these algebraic laws. Promote only
backend-neutral theorems independently exercised in other Artes; never promote this
Python API wholesale.
