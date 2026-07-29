# ADR 0013: Lifecycle changes do not rewrite prior operations

Status: Candidate

## Context

Three independent domains preserve earlier operational conditions while changing
future behavior:

- Feedback and Model Revision constructs new model versions and assessments without
  rewriting committed predictions or historical outcomes.
- Scoped Model Adoption records switching and Revocation prospectively while prior
  actions retain the Model, Adoption, and authority that governed them.
- Bound Delegation blocks expired or revoked future actions while earlier Trace
  records retain their then-current lease, grant, action, consequence, and lineage.
  Compensation appends repair without deleting harm.

These domains share no history representation. Their common observable job is to
prevent present lifecycle state from being projected backward into prior operation.

## Candidate decision

> Changes to models, authority, or lifecycle govern future operations and may append
> new assessments, but do not retroactively alter the conditions, actions, or records
> under which earlier operations occurred.

## Boundary

The candidate does not require every past action to remain currently authorized,
valid for replay, successful, uncompensated, or accepted. New evidence may change a
present assessment of history while preserving what occurred and which rules applied
then.

## Explicitly not decided

- one universal history, event, provenance, or audit representation;
- retention duration, garbage collection, privacy, correction, or redaction policy;
- whether history participates in identity, equality, validity, or type checking;
- syntax, AST, types, runtime values, diagnostics, storage, or package API.

## Promotion gate

Before acceptance, reconcile prediction commitment, model switching, authority
expiry, correction, compensation, and reassessment in backend-neutral terms. The law
must distinguish preserving historical occurrence from freezing every later judgment
about it.
