# Euclid I.1 foundation experiment

**Question:** Can one immutable, inspectable Spell Form construct and demonstrate
Euclid I.1 while an undeclared orientation remains a real Potential rather than a
host-language default?

This is the first executable probe of the provisional Arx Mentis foundation. It is
deliberately outside `src/arx_mentis`: importing it as a library contract or treating
its Python representation as language semantics would invalidate the experiment.

## Assumptions made only for this probe

- A `Line` is modeled as an unordered two-Point relation. A separate
  `OrientedLine(A, B)` distinguishes left and right without deciding that all Lines
  are directed.
- Circle construction, circle intersection, and Line construction are primitive
  powers only because the Spell requires named Postulates and the Context supplies
  them.
- The two intersection Points are relational forms. No floating-point coordinates
  or Python numeric behavior are involved. The probe specializes to the two
  equal-radius circles built on distinct A and B; it does not propose a general
  circle-intersection algorithm.
- Demonstrations are inspectable traces with declared Definitions and a Common
  Notion. This probe constructs the trace; it does not yet provide a general proof
  checker.
- `ExperimentRefusal` is an owned harness diagnostic for an incomplete probe. It
  explicitly does not answer the open language question of failure or refusal.
- Python dictionaries hold private binding state. `frozenset` prevents an option
  order from becoming a choice, but neither container's host behavior is proposed
  as an Arx Mentis law.

## Success signal

The probe succeeds when all of these observations hold:

1. The same `Spell` object is inspectable as a Form and cast as instructions.
2. The given Line remains unchanged and every Effect contains a new geometric Form.
3. Every construction and proof rule used is a declared Spell requirement supplied
   by the Context.
4. An unoriented Context produces `Potential(options, trigger)` with two Effects and
   no selected value.
5. A Context orientation settles that Potential to the corresponding Effect, and
   left and right Contexts produce different Effects from the same Spell.
6. Each Effect carries a demonstration trace from equal radii, Common Notion 1, and
   the definition of an equilateral triangular Form.

Run the witness and its focused tests from the repository root:

```console
python -m experiments.euclid_i_1
python -m pytest tests/experiments/test_euclid_i_1.py
```

Use the repository's Python 3.13+ environment for both commands.

## Deletion or promotion path

Delete the probe if its distinctions fail to clarify the construction. If repeated,
independent experiments support some distinction, promote only that distinction
through examples, conformance tests, an ADR where appropriate, and a lowering
sketch. Do not move this Python API into `src/arx_mentis` wholesale.
