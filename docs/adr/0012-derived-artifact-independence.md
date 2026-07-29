# ADR 0012: Derived operation may outlive source availability only by declaration

Status: Candidate

## Context

Three independent domains separate source availability from a derived mechanism's
continued authority:

- Actualization releases a compiled guidance policy that continues without live
  TargetForm access while retaining provenance.
- Symbolic Release executes a lawfully compiled Carrier after SourceForm release;
  incomplete derivation instead returns MissingDependency.
- Scoped Model Adoption permits a declared snapshot artifact to continue after its
  source Adoption is revoked until explicit expiry. A live-linked artifact stops,
  new derivation is blocked, and unspecified lifecycle behavior is refused.

The shared job is conditional independence, not deletion: a derived artifact may
continue only when the required dependency and authority were explicitly discharged,
while origin and history remain inspectable.

## Candidate decision

> Source availability and derived operational authority are distinct. A derived
> artifact may continue without rereading its source only when its construction
> explicitly establishes sufficient independent authority and preserves origin;
> otherwise loss or revocation of the source must remain observable.

## Boundary

This candidate does not make every compiled or derived artifact independent. It
requires live-linked, incomplete, expired, and unspecified cases to remain distinct
from lawful snapshots or released artifacts.

## Explicitly not decided

- how authority, dependency, provenance, expiry, or release is represented;
- whether the transition is Cast, Effect, lifecycle, scope, ownership, or permission;
- whether independent artifacts may be transferred, serialized, or persisted;
- syntax, AST, types, runtime values, diagnostics, or package API.

## Promotion gate

Before acceptance, reconcile the three domains' dependency-discharge and authority
conditions in backend-neutral terms. The rule must preserve negative cases and may
not infer independence merely from compilation, copying, or source disappearance.
