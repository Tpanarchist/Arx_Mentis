# Roadmap

This order is a constraint on learning, not a release schedule.

1. Preserve Stage 0 packaging, diagnostic boundaries, evidence records, and open
   decisions.
2. Introduce the smallest tokenizer probe with spans originating at the first token.
3. Add the handwritten recursive-descent parser with Pratt expression parsing and
   preserve spans into a deliberately small AST.
4. Establish resolution/checking and a **typed checked representation**.
5. Add an owned value representation in the commit that first produces an
   observable value, following the ADR 0005 integer trigger.
6. Exercise the Python reference evaluator and high-level lowering sketches as
   sibling consumers of checked programs.
7. Use failed lowering attempts to decide whether a high-level IR is justified.
8. Select a backend target only after the backend interface has real consumers.

The typed checked representation must precede freezing evaluation order, equality,
mutability, or error propagation. Those choices need typed programs and observable
examples; deciding them from untyped evaluator convenience would make reversal
needlessly expensive.

## Primary early horizontal probe

Self-host the tokenizer first and the parser second. This is the primary early
horizontal probe because it crosses text processing, collections, control flow,
diagnostics, modules, and performance pressure without requiring the entire toolchain
to be self-hosted. The probe is evidence, not a promise that self-hosting is a final
product goal.

Package adapters are optional and late. They should follow a stable semantic core
and a concrete interoperability need, never drive core naming or value semantics.

