# Vision

Arx Mentis will be a language whose design is learned through executable programs,
not a Python library whose incidental behavior is retroactively declared a language.
The Python implementation is the first precise, runnable reference, while explicit
interfaces preserve the option to change representations, lower into an IR, or use
another backend.

## Stage 0 principles

1. Preserve uncertainty where evidence is absent.
2. Make source provenance and diagnostics structural from the first token onward.
3. Keep semantic values owned by Arx Mentis, even when Python performs internal work.
4. Explore high-level constructs by attempting to lower them before choosing a
   low-level control-flow representation.
5. Use self-hosting pressure early enough to expose horizontal weaknesses.

Stage 0 is infrastructure, not a small language. It contains no syntax, AST,
semantics, evaluator, runtime values, or IR. Naming a future boundary does not imply
that its representation or behavior has been selected.

## Non-goals

This bootstrap does not select a thesis, type/value discipline, integer behavior,
equality, evaluation order, mutability, error model, module system, concurrency
model, memory model, IR shape, or backend target. It also does not publish a package
or promise that the `arx-mentis` name is available on PyPI.

