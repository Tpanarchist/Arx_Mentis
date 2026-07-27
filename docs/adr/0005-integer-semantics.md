# ADR 0005: Integer semantics

Status: Open question

## Context

Python offers arbitrary-precision signed integers with particular division,
conversion, hashing, and interoperability behavior. Reusing `int` internally would
be convenient but must not settle Arx Mentis overflow, width, signedness, literals,
division, or conversion rules.

## Question

What integer model and observable operations should Arx Mentis define?

## Mandatory resolution trigger

The first commit capable of producing an observable Arx Mentis value must introduce
an owned value representation in that same commit. If that first value is an
integer, this ADR must leave **Open question** status in that commit. Otherwise this
ADR must be resolved no later than the first commit capable of producing an integer.

That commit may delegate internally to Python, but tests and semantic interfaces may
not expose a bare Python value as an Arx Mentis result.

## Safe deferral

Stage 0 produces no values and includes no value module or numeric operation. There
is therefore no observable Python integer behavior to preserve.

