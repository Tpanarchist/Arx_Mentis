# Architecture

The current experimental information flow is:

```text
given Forms + inspectable Spell + explicit Context
  → Cast
      ↘ Effect + Demonstration + Will comparison
      ↘ Potential(options, trigger)
```

This flow exists only under `experiments/` until repeated evidence earns stable
language representations. It must not be imported into the installable package.

After experiments justify source notation, the tentative implementation flow is:

```text
source
  → handwritten frontend
  → spanned AST
  → resolution and checking
  → typed checked representation
  → backend interface
      ↘ Python reference evaluation
      ↘ future high-level IR lowering
```

The final two paths are siblings. The Python reference evaluator does not define an
IR by accident, and the future lowering path does not have to mimic the evaluator's
internal call structure. Both consume an Arx Mentis-owned checked representation
through a backend-facing interface.

## Reversible seams

Package boundaries express dependency direction, not completed abstractions. The
frontend may construct syntax and diagnostics. Resolution/checking may consume
spanned syntax and produce a typed checked representation. Backends may consume
that checked representation. Adapters remain outside the semantic core.

Raw Python objects may exist behind an implementation boundary, but they are never
Arx Mentis semantic values. A result that crosses a semantic or experimental test
interface must use a representation owned by this project. This keeps Python
arithmetic, iteration, exceptions, object identity, resource finalization, and
container behavior from silently becoming language rules.

## Span invariant

A source span begins with the first future token and survives parsing, resolution,
and checking. Later representations may refine or combine provenance, but they may
not discard it. This is an implementation constraint for diagnostics, not a choice
of surface syntax or semantic behavior.
