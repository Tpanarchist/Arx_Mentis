# Testing strategy

Testing separates implementation correctness from language acceptance.

- **Unit tests** cover package metadata and isolated infrastructure behavior.
- **Integration tests** cover module and installed console entry points.
- **Conformance tests** will encode accepted observable language behavior and remain
  backend-neutral.
- **Generative tests** will eventually construct well-typed programs independently
  of the production checker.

Stage 0 package tests cover only bootstrap behavior. Focused experiment tests may
make provisional behavior executable under `tests/experiments`; they are evidence,
not backend-neutral language conformance tests. Empty future categories retain
guidance without inventing accepted language cases.

## Constructive well-typed generation

Well-typed program generation is a separate constructive encoding of the typing
rules, not a call to the production type checker followed by rejection sampling.
Its generators carry enough context to construct terms that are valid by design.
This creates an independent correctness obligation: the generator must be sound
with respect to the intended rules, useful across the relevant feature space, and
reviewed when those rules change.

Independence catches checker bugs but also creates drift risk. Changes to typing
rules must name their checker tests, generator changes, and cross-check properties.
Neither implementation is automatically authoritative merely because it agrees
with itself.

## Equivalence tests

Cross-backend comparisons cannot default to Python equality. They must use the
policies eventually filled in `equivalence.md`, including results, errors,
side-effects, I/O, floats, ordering, and finalization.
