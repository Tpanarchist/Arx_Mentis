# State Zero Experiment 007: Actualization

**Status:** Disposable evidence experiment. Nothing here is package API or accepted
language semantics.

## Question

Is a target only an acceptance criterion, or can the same target also guide the
production of an outcome? If an outcome conforms, what—if anything—does that prove
about the mechanism that produced it?

The source prompt is Stephen Mace's
[*Sorcery as Virtual Mechanics*](https://www.scribd.com/doc/96245037/37606530-Stephen-Mace-Sorcery-as-Virtual-Mechanics),
subtitled *The Actualization of Unseen Forms in Occult Working*. The experiment takes
only the abstract pressure to distinguish a prior form, a physical result, and a
claimed connection between them. It makes no claim about occult or physical
causation.

## Assumptions

- A finite deterministic transition graph is enough to isolate criterion, guidance,
  and causation without a clock, randomness, network, or external I/O.
- Frozen Python records are disposable carriers, not proposed runtime values.
- A privileged `CausalTrace` records the experimental world mechanism; an observer
  who receives only the final state does not receive that privilege.
- A `TargetForm` can be read into an `AcceptanceRule`, an `ActionPolicy`, both, or
  neither. This is the hypothesis under test, not a foundation decision.

## Competing models

1. **Criterion only:** a target evaluates a state produced by the graph's baseline
   policy and never affects transition choice.
2. **Policy guidance:** the target derives a policy. A sustained controller consults
   target-relative feedback; a released controller continues with only the compiled
   policy and its provenance.
3. **Explicit hidden bias:** a target derives inspectable transition weights. This
   models the logical shape of an indirect causal channel without asserting that
   such a channel exists in nature.
4. **Direct assignment:** setting the world equal to the target is rejected as a
   circular countermodel because it supplies no transition or causal account.

Two targets have the same acceptance rule but choose shortest and safe routes. Two
other targets derive the same shortest-route policy but use different acceptance
thresholds. These counterexamples make criterion and guidance operationally
independent even when both can be derived from one source record.

## Success signal

The experiment succeeds if executable witnesses show that targets precede action,
sources and targets remain immutable, production creates separately owned states,
the same accepted state can arise through three causally distinct mechanisms,
conformity does not identify mechanism, sustained and released control are distinct,
and blocked or partial runs cannot manufacture success.

## Executable witness

```powershell
.venv\Scripts\python.exe -m experiments.actualization
.venv\Scripts\python.exe -m pytest tests/experiments/test_actualization.py
```

## Result and boundary

The neutral model supports a narrow result: acceptance, construction guidance, and
causal attribution are distinct jobs. One `TargetForm` can derive separate records
for the first two, but that fact does not decide whether foundation `Will` names the
source, the acceptance role, both readings, or neither. A conforming state is also
insufficient evidence for how it was produced.

## Deletion or promotion path

Delete this directory if a later counterexample cannot preserve these distinctions
or if the graph assumptions carry the result. Promote only backend-neutral
obligations that recur in at least three independent domains with a negative
boundary. Do not promote these Python records, direct-assignment diagnostic, target
names, or controller mechanics.
