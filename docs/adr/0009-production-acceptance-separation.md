# ADR 0009: Production and acceptance are separate operations

Status: Accepted

## Context

Four independent experimental domains expose the same distinction without sharing a
Python representation:

- Euclid I.1 constructs a symmetry-indexed Effect before an invariant Will check.
- Ars Grammatica performs a rename separately from checking preservation of the
  declared clause relation.
- Ars Dialectica can verify a produced inference while its Effect still diverges from
  Will.
- State Zero Experiment 007 varies guidance and acceptance independently in both
  directions: equal acceptance can guide different paths, and equal guidance can use
  different acceptance thresholds.

The boundary is exercised by permitted nonconforming Effects, frame-dependent checks,
partial progress, unreachable targets, and several distinct mechanisms producing the
same conforming state.

## Decision

Accept this backend-neutral obligation:

> Producing a result and determining whether that result satisfies an acceptance
> criterion are observably distinct operations. Neither operation may be defined as
> automatically performing the other.

Production may complete before acceptance is evaluated. Acceptance must inspect an
actual result rather than substitute the intended result. A successful production
does not imply conformity, and conformity does not identify the production mechanism.

An implementation may fuse the operations internally only if their separate inputs,
outcomes, provenance, failure boundaries, and observable ordering remain expressible.

## Explicitly not decided

This decision does not determine:

- whether the final language uses the name `Will`;
- whether acceptance is static, dynamic, staged, or available in several forms;
- whether every construction declares an acceptance criterion;
- how acceptance predicates or results are represented;
- whether acceptance and guidance may be derived from one source Form;
- whether conformity affects control flow or continuation typing;
- whether checking is implicit in a larger operation at some source boundary;
- any syntax, AST, type, runtime value, package API, or backend strategy.

## Consequences

- Evidence and tests must be able to distinguish construction outcome from acceptance
  outcome.
- A nonconforming result is not retroactively reclassified as “no production” merely
  because its acceptance check fails.
- A declared acceptance criterion cannot create, repair, or select its own result.
- Provenance for production and evidence for acceptance may be related but cannot be
  treated as identical by default.
- Guidance remains a third open role. Experiment 007 shows that one TargetForm can
  derive guidance and acceptance separately, but one domain does not establish a
  general guidance algebra or decide the identity of Will.

## Implementation deferral

Do not add tokens, grammar, AST nodes, types, evaluators, shared foundation classes,
or package APIs from this decision. The accepted content is only the observable
separation. Representation work remains behind the full synthesis gate.

