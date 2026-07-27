# ADR 0001: Python-first executable reference specification

Status: Accepted

## Context

The project needs an implementation that makes proposals runnable early without
making its host language the permanent definition or target.

## Decision

Build the first executable reference specification in Python 3.13+. Keep semantic
interfaces and values owned by Arx Mentis. Treat conformance examples and accepted
decisions as the source of observable behavior; Python implementation details carry
no independent semantic authority.

## Consequences

Exploration can use a small, readable implementation and mature development tools.
Python exceptions, numbers, collections, object identity, evaluation order, I/O,
and finalization must be contained until individually decided. Another backend may
replace or coexist with Python without imitating unrelated host details.

