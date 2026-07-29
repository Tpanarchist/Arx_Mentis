# State Zero Experiment 013: Bound Delegation

**Status:** Disposable evidence experiment. Nothing here is package API or accepted
language representation.

## Question

Can a derived mechanism act without rereading its source while remaining bounded by
separately declared authority, scope, resources, lifetime, and consequence rules?

Stephen Mace's
[*Sorcery as Virtual Mechanics*](https://www.scribd.com/doc/96245037/37606530-Stephen-Mace-Sorcery-as-Virtual-Mechanics)
motivates the mediation pressure. A later
[secondary discussion](https://podcasts.apple.com/ca/podcast/the-1988-book-that-cracked-magick/id1803423052?i=1000753711077)
motivates containment and blowback only as investigative language. Neither source is
treated as evidence for these neutral mechanics, and the experiment makes no occult,
empirical, security, or capability-system claim.

## Assumptions

- North, Center, and South form one exact finite symbolic environment.
- Integer resource units, authority priority, action budget, lease steps, and record
  order are harness values rather than proposed semantic units.
- A trusted derivation registry witnesses admissible lineage but is not a security or
  cryptographic mechanism.
- Frozen Python records are disposable carriers.

## Exact contained authority

A Principal derives a compiled Delegate from an immutable SourcePlan. The standard
grant declares:

```text
role          rebalance resources
scope         North, Center
capabilities  read inventory, transfer, write operation record
transfer      at most 2 units per action
lease         steps 2 through 5
budget        at most 3 actions
denied        protected records, South, child derivation
```

The source content then becomes unavailable. The Delegate completes three lawful
actions without rereading it; a fourth action is refused before mutation because its
budget is exhausted.

Every action rechecks admission, control authority, capability, direct scope,
per-action limit, budget, lease, revocation, and resources before constructing a new
Environment.

## Independence vector

The experiment defines no `independent = True` state. Its exact dependency profile
is:

```text
source content   independent
authority        lease-dependent
resources        environment-dependent
scope            fixed
lifecycle        revocable
interpretation   compiled
provenance       retained
```

Source-content independence therefore says nothing automatically about authority,
scope, resources, lifecycle, provenance, responsibility, or consequence extent.

## Reading and authority

The same artifact supports explicit Audit and Control readings. Audit explains the
planned instructions without write authority. Control interpretation remains
possible as structure, but execution separately requires admitted lineage, explicit
authority, Activation, capability, and current lifecycle conditions. An
instructions-only copy is auditable and structurally equal while remaining
inadmissible for control.

This is the hostile boundary needed to narrow contextual reading:

```text
lawful interpretation != authority to act
```

## Lifecycle and delegation

Live-linked revocation blocks the next action immediately. A separately declared
snapshot ignores current principal revocation only until its own lease expires; the
revocation prevents new snapshot derivation. Unspecified cascade-versus-snapshot
behavior returns an owned result. Earlier actions retain the authority and lineage
that governed them.

A parent with explicit delegation capability may derive an attenuated child whose
capabilities, scopes, limits, budget, and lease are subsets of its own. Amplification
or derivation by a parent lacking that capability returns an owned result. This is
one-domain pressure only; no general delegation algebra is promoted.

## Consequences and compensation

A lawful North action may consume a shared resource and produce:

- direct write scope in North;
- observable shortage in South;
- resource loss returning to the Principal.

The spillover and blowback causal chains retain the Delegate action, environment
mechanism, source lineage, and authority. Compensation later restores the South
resource but appends repair records; it does not delete the original action,
shortage, principal loss, or responsibility trace.

## ADR 0010 boundary

Overlapping equal-priority Delegates return one AuthorityConflict. Reversing storage
order preserves the same candidates. A declared higher-priority or preferred-Delegate
policy may select because it supplies an inspectable semantic discriminator.

## Hostile countermodels

The experiment owns rejections for role-grants-authority,
compiled-means-unrestricted, authority-as-instruction-data,
scope-as-consequence-boundary, revocation-erases-history, revocation-always-cascades,
revocation-never-cascades, child-authority amplification,
activation-only lease checks, post-mutation budget checks,
success-justifies-excess-authority, compensation-deletes-harm,
principal-only causation, Delegate-only causation, and
same-artifact-as-same-authority.

## Success signal

The experiment succeeds if executable witnesses preserve source, dependency,
reading, authority, admission, scope, budget, lease, lifecycle, attenuation,
consequence, compensation, causation, history, and conflict-policy boundaries without
importing package types or previous experiments.

## Executable witness

```powershell
.venv\Scripts\python.exe -m experiments.bound_delegation
.venv\Scripts\python.exe -m pytest tests/experiments/test_bound_delegation.py
```

## Result and boundary

Releasing a mechanism from source-content access does not release it from its bounds.
Passing supplies the hostile evidence needed to narrow and accept ADRs 0011 and 0012:
reading remains distinct from authority, and source independence is always relative
to explicit dependencies. It also supplies the third direct prospective-history
domain, justifying a candidate ADR rather than acceptance.

Delegated authority cannot exceed granted authority remains a one-domain provisional
pressure. No capability system, lifecycle representation, shared Delegate type, or
source feature follows.

## Deletion or promotion path

Delete the experiment if reading grants authority, copies inherit permission, checks
happen after mutation, expired or revoked live Delegates continue, snapshots are
silently denied, indirect consequences disappear, or compensation rewrites history.
Promote only the carrier-independent obligations recorded by the synthesis gate.
Never promote these compartments, grants, record values, registry, or Python types.
