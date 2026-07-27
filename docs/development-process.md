# Development process

## Feature acceptance

Every future language feature must earn acceptance in its implementation work with
all four of the following:

1. evidence from the motivating difficulty or tension;
2. examples that isolate the underlying idea;
3. tests at the appropriate unit, integration, and conformance levels;
4. a short lowering sketch describing how the feature might reach a simpler form,
   including any part that does not lower cleanly.

The sketch is required even before an IR exists. It is a probe, not a promise of a
specific IR.

## Owned-value implementation gate

The first commit capable of producing an observable Arx Mentis value must introduce
an owned value representation in that same commit. The implementation may delegate
internally to Python, but tests and semantic interfaces may not expose a bare Python
value as an Arx Mentis result.

If that first observable value is an integer, ADR 0005 must still have **Open
question** status in that commit. If the first value is not an integer, ADR 0005 must
be resolved no later than the first commit capable of producing an integer. This
ordering prevents Python's `int` behavior from becoming an unreviewed decision.

## Evidence and synthesis

Record design friction as it is observed under `friction.md`. Thesis work becomes
warranted when the same nameable tension appears in three genuinely unrelated
programs, domains, or implementation situations. Repeated wording or variants from
one design episode count as one source of evidence.

The trigger permits synthesis. It does not require immediate publication of a
thesis, and it does not prohibit earlier exploratory language about a possible
thesis. Evidence remains useful even when the team decides not to synthesize it yet.

## Change discipline

- Update an ADR when a decision or explicit trigger changes.
- Fill equivalence obligations before claiming two backends are equivalent.
- Justify each dependency before adding it.
- Keep experiments disposable and prevent their APIs from crossing semantic seams.
- Keep generated artifacts, local environments, caches, wheels, and reports out of
  version control.

