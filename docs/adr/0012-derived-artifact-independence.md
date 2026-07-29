# ADR 0012: Derived independence is relative to explicit dependencies

Status: Accepted

## Context

Four independent domains separate source availability from a derived mechanism's
continued authority:

- Actualization releases a compiled guidance policy that continues without live
  TargetForm access while retaining provenance.
- Symbolic Release executes a lawfully compiled Carrier after SourceForm release;
  incomplete derivation instead returns MissingDependency.
- Scoped Model Adoption permits a declared snapshot artifact to continue after its
  source Adoption is revoked until explicit expiry. A live-linked artifact stops,
  new derivation is blocked, and unspecified lifecycle behavior is refused.
- Bound Delegation executes a compiled Delegate after SourcePlan content release
  while independently rechecking authority, scope, resources, lease, budget,
  revocation, admission, and provenance. Copies without grants or lineage remain
  inadmissible, and consequences remain attributable.

The shared job is conditional independence, not deletion: a derived artifact may
continue only when the required dependency and authority were explicitly discharged,
while origin and history remain inspectable.

## Decision

> A lawfully derived artifact may continue without rereading its source when every
> dependency required for later operation has been preserved or explicitly
> externalized. Independence must be stated relative to particular dependencies and
> does not imply independent authority, scope, resources, lifecycle, provenance, or
> responsibility.

Source-content, interpretation, authority, scope, resource, lifecycle, provenance,
and consequence dependencies are separately observable. The accepted law rejects a
single total-independence inference.

## Boundary

This decision does not make every compiled or derived artifact independent. It
requires live-linked, incomplete, expired, and unspecified cases to remain distinct
from lawful snapshots or released artifacts.

## Explicitly not decided

- how authority, dependency, provenance, expiry, or release is represented;
- whether the transition is Cast, Effect, lifecycle, scope, ownership, or permission;
- whether independent artifacts may be transferred, serialized, or persisted;
- syntax, AST, types, runtime values, diagnostics, or package API.

## Implementation deferral

Bound Delegation supplies the missing dimensioned-dependency and unauthorized-copy
boundaries. The accepted law still authorizes no dependency-vector type, lifecycle
model, authority system, compiler behavior, syntax, runtime value, or package feature.
