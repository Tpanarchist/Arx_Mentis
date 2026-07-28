# Ars Grammatica reading-role experiment

**Question:** Can one generic composite Form remain data for an `Inspector` and
become exact construction for an `Interpreter` without a nominal `Spell` type?

The Form relates an ordinary clause, old and new names, a rename operation, and Will.
An `Inspector` returns its structure. An `Interpreter` recognizes the same
relations through a declared Grammar Definition and performs the rename. `Audience`
and `Witness` are distinct types, not values of one universal Reader enum.

## Assumptions

- Relation kinds and the composite graph are experimental representation choices.
- The single-clause rename is a probe of role and preservation, not a general
  grammar, binding, or substitution system.
- Reader kinds are explicit Form types; Python dispatch is not language law.
- Ars-qualified grammatical equivalence is checked after construction, separately
  from whether construction occurred.
- Unsupported Readers and ambiguous definitions remain harness-only diagnostics.

## Success signal

- The module defines no nominal `Spell` class.
- The exact same Form object can be inspected or executed by changing only its
  concrete Reader Form.
- Examination performs no construction.
- Execution creates a new clause, changes only the declared subject, preserves the
  predicate, and leaves the source Form unchanged.
- Missing permission is a `Refused` construction; malformed relations are a
  `Failed` construction; an unsupported Reader remains an owned diagnostic.
- A separately invoked check can establish grammatical equivalence or produce a
  counterexample to Will.

Run with:

```console
python -m experiments.ars_grammatica_reading
python -m pytest tests/experiments/test_ars_grammatica_reading.py
```

## Deletion or promotion path

Delete the probe if contextual reading adds no clarity over nominal instruction
types. Promote only the contextual-role distinction if independent experiments can
state it without importing this graph representation.
