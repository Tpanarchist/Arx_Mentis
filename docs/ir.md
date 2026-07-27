# IR discovery

Arx Mentis has no intermediate representation at Stage 0. The first task is to learn
what high-level distinctions must survive lowering, not to select SSA, basic blocks,
or an instruction encoding.

## Discovery method

For every feature implementation, write a short lowering sketch. Attempt to express
the construct using simpler checked constructs and record where the attempt loses
meaning, source provenance, typing facts, evaluation constraints, or diagnostic
quality. Repeated failed lowering attempts are evidence for high-level IR nodes or
effects.

Only after several real programs have exercised this path should the project decide
whether a control-flow graph, SSA form, stack form, tree form, or combination is
appropriate. ADR 0006 owns that decision.

## Separation from evaluation

The Python reference evaluator and future high-level lowering are sibling consumers
of the checked representation. Evaluator implementation details do not become IR
operations, and an early IR experiment does not constrain the reference evaluator.

