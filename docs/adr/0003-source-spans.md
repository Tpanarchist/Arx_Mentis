# ADR 0003: Source spans begin at tokenization and survive checking

Status: Accepted

## Context

Retrofitting provenance after parsing produces weak diagnostics and makes later
representations depend on hidden source lookups.

## Decision

Spans begin with the first future token and survive parsing, resolution, and
checking. AST and checked representations must retain or deliberately compose source
provenance.

## Consequences

Future tokens and representation nodes need explicit span-bearing structure. This
cost is accepted early because it determines diagnostic and transformation
interfaces without selecting syntax, type rules, evaluation rules, or backend
behavior.

