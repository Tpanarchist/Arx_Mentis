# ADR 0002: Handwritten recursive-descent parser with Pratt expressions

Status: Accepted

## Context

The future grammar will change during exploration. Parser behavior and diagnostic
structure must remain visible and locally adjustable without adding a parser-runtime
dependency or choosing semantic rules.

## Decision

Use a handwritten recursive-descent parser for declarations, statements, and other
structural forms, with Pratt parsing for expressions and operator binding.

## Consequences

The parser strategy fixes an implementation seam but no grammar, operator, or syntax
at Stage 0. Binding-power tables and recovery behavior will require tests when syntax
arrives. The approach keeps source spans and targeted diagnostics under project
control.

