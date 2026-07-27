# ADR 0006: High-level IR shape

Status: Open question

## Context

Choosing SSA, basic blocks, or an instruction set before real checked programs are
lowered would optimize for familiar machinery rather than the language's actual
high-level constructs.

## Question

Which source-level facts and high-level operations need explicit IR representation,
and which low-level form should eventually carry them to a backend?

## Resolution evidence

Require lowering sketches with feature work. Attempt real lowerings and record where
simplification loses typing facts, evaluation constraints, provenance, or diagnostic
quality. Repeated failure modes may justify high-level nodes. Decide low-level form
only after those attempts provide multiple representative cases.

## Safe deferral

The Python reference evaluator can consume a future checked representation as a
sibling to lowering. No Stage 0 API promises an IR shape.

