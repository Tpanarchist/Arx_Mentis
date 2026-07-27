# ADR 0004: Value and type discipline

Status: Open question

## Context

The project has not observed programs that justify static versus dynamic choices,
the relation between types and runtime representations, polymorphism, subtyping,
effects, inference, or the boundary between checking and execution.

## Question

What value and type discipline best explains the evidence while supporting useful
diagnostics, constructive well-typed generation, lowering, and more than one backend?

## Resolution evidence

Resolve through unrelated program evidence and checked-representation prototypes,
not by mirroring Python's object or annotation model. Any proposal must include
examples, tests, a lowering sketch, and an account of generator/checker independence.

## Safe deferral

Stage 0 produces no language values and exposes no checking API. The semantic
boundary package reserves dependency direction without committing a representation.

