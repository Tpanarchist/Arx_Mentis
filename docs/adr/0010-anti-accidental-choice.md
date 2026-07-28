# ADR 0010: Incidental representation order supplies no discriminator

Status: Accepted

## Context

Three independent domains reject a choice that is justified only by representation
order:

- Euclid I.1 cannot select one reflected construction by presentation order. A
  legitimate default must be semantically fixed and constructible.
- Virtual Mediation cannot select one channel by list position. Reversing presentation
  leaves the cyclic family and its correlations unchanged.
- Stress and Discharge returns the same AmbiguousDischarge for an exact mechanical tie
  when link storage order is reversed.

These domains use unrelated representations and exercise geometric construction,
cyclic mediation, and causal network flow. Their shared candidate is broader than any
one default theorem.

## Decision

> When declared semantics provide no discriminator among distinct admissible
> alternatives, incidental representation order must not supply one. The system must
> preserve ambiguity, refuse the operation, or require an explicit selection policy.

The obligation prohibits an implementation from inventing a missing decision. It
does not require one universal response: a domain may preserve every candidate,
return an unresolved result, require a policy, reject during checking, refuse during
execution, or define another owned ambiguity result.

## Legitimate declared ordering

Ordering remains semantic when the domain declares it as part of the operation. A
first-applicable rule, greater declared priority, or least value under a named
canonical order may select a result. In each case the discriminator is inspectable
and reversing incidental storage while preserving the declared relation does not
change the result. Undeclared list, dictionary, traversal, call, presentation, or
hash order supplies no such authority.

## Confirming hostile evidence

State Zero Experiment 010 constructs incompatible equal-priority interventions whose
composition is undeclared. It returns one owned conflict containing the same
candidates when their declaration order is reversed. No first element, sorted key,
hash, or call order becomes a winner.

This is a fourth independent domain and a hostile witness: the probabilistic model
would otherwise make it easy for an implementation to choose whichever intervention
it traverses first. The observable obligation is carrier-independent: the conflict is
unchanged by a permutation that changes no declared semantics.

## Explicitly not decided

The decision does not determine:

- how ambiguity is represented;
- whether a particular domain requires an error, family, conflict, or policy request;
- what selection policies exist or how they compose;
- which declared ordering or canonicalization relations any domain should provide;
- any syntax, AST, type, runtime value, diagnostic shape, or package API.

## Implementation deferral

The hostile witness has passed independently of the three existing domains, so the
narrow semantic law is accepted. This record still authorizes no particular
representation or language feature. Syntax, runtime values, diagnostics, and explicit
selection-policy design remain behind the full synthesis gate.
