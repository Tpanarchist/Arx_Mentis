# ADR 0011: Explicit context may supply an artifact's use role

Status: Candidate

## Context

Three independent domains exhibit one carrier or source under multiple lawful roles:

- Ars Grammatica reads one generic Form for inspection or execution; changing the
  explicit Reader role changes behavior without mutating the Form.
- Symbolic Release reads one keyed Carrier into policy or acceptance artifacts;
  unsupported readings return owned results and the Carrier does not interpret
  itself.
- Scoped Model Adoption derives a PredictionRule or operative DerivedPolicy from the
  same Model under explicit predictive or control Adoption. Crossed and unsupported
  uses are refused, and Model contains neither role intrinsically.

The experiments share no carrier representation. Their common observable job is to
make role selection explicit while preserving source identity and rejecting
unsupported readings.

## Candidate decision

> An artifact's use role may be supplied by an explicit reading or operational
> context rather than fixed by carrier identity. One source may support multiple
> lawful roles without mutation, and unsupported roles must remain owned boundary
> results.

## Boundary

This is not the claim that every role is contextual or that nominal roles are
forbidden. Euclid, Astronomica, and Dialectica still use nominal Spell
representations. The candidate does not decide whether foundation Spell is nominal,
contextual, or a combination.

## Explicitly not decided

- representation of roles, Readers, keys, Adoptions, or artifacts;
- role composition, subtyping, capabilities, or authorization;
- whether interpretation and activation are one operation;
- syntax, AST, types, runtime values, diagnostics, or package API.

## Promotion gate

Before acceptance, compare the three domains' source preservation, unsupported-role
behavior, role composition pressure, and authority requirements without importing a
shared carrier. Acceptance requires a backend-neutral law that does not overrule the
nominal counterexamples.
