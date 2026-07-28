# State Zero Experiment 010: Bias Without Command

**Status:** Disposable evidence experiment. Nothing here is package API or accepted
language semantics.

## Question

Can an intervention change the distribution of possible outcomes without directly
commanding a particular outcome?

The motivating source is Stephen Mace's
[*Sorcery as Virtual Mechanics*](https://www.scribd.com/doc/96245037/37606530-Stephen-Mace-Sorcery-as-Virtual-Mechanics).
This experiment extracts only an exact representational distinction between influence
and command. It does not test or assert that sorcery changes probability in reality.

## Assumptions

- Sixty declared seeds provide an exact, finite production space with no randomness or
  flaky statistical assertions.
- Kernel weights are symbolic mass, not inferred probabilities or empirical claims.
- Seed order is a declared execution input. It selects within a kernel but does not
  explain why that kernel or an intervention exists.
- Frozen Python records are disposable carriers rather than proposed runtime values.

## Exact mechanics

The baseline kernel assigns ten seeds to each of six outcomes. A declared intervention
changes the target mass to twenty and every other mass to eight:

```text
baseline: 10, 10, 10, 10, 10, 10
biased:   20,  8,  8,  8,  8,  8
```

Both kernels retain the same support. A direct command instead removes alternatives
and is rejected as a model of bias. Every `TrialPlan` records its outcome space,
target, kernel, interventions, count, seeds, contexts, observation window, report
policy, stopping rule, and comparison rule before the first Trial.

## Independent boundaries

- **Support versus weight:** an option bag preserves support and loses weighted
  behavior.
- **Kernel versus sample:** a short uneven window does not mutate its generator.
- **Stream versus report:** target-only reporting preserves the original stream.
- **Bias versus command:** reweighting leaves target and non-target outcomes possible.
- **Target versus acceptance:** no sample is accepted without a separate criterion.
- **World cause versus observer attribution:** a hidden-context mixture retains its
  definite causal record while an observer sees only public outcomes.
- **Probability versus Potential:** unequal weighted production has no declared
  transitive frame or later settlement operation.

Two hidden context kernels are sampled through an explicitly precommitted schedule.
Their public frequencies equal the fixed biased kernel exactly, while their causal
records remain different.

## Hostile countermodels

The experiment owns rejections for option-bag loss, sample-as-kernel,
match-implies-bias, report-as-stream, target-coded command, post-hoc intention, hidden
optional stopping, hidden mixture, seed-only causation, and order-based intervention
resolution.

Two incompatible interventions with equal priority produce one
`InterventionConflict`. Reversing their storage and declaration order preserves the
same unordered candidates. The implementation may not choose a first item, sorted
key, hash, or accidental call order.

## Success signal

The experiment succeeds if exact witnesses cover all required production,
observation, reporting, mixture, precommitment, intervention, conflict, acceptance,
attribution, and hostile-model boundaries without importing foundation types or prior
experiments.

## Executable witness

```powershell
.venv\Scripts\python.exe -m experiments.probability_bias
.venv\Scripts\python.exe -m pytest tests/experiments/test_probability_bias.py
```

## Result and boundary

Bias changes weights without installing an answer. A sample does not rewrite its
kernel, a report does not rewrite its stream, an accepted sample does not reveal its
cause, and a weighted kernel is not automatically Potential. Equal public
distributions can retain distinct causal mechanisms.

The equal-priority hostile witness supplies a fourth independent domain for the
anti-accidental-choice law. It can justify that narrow law only; it does not establish
a probability type, inference calculus, sampling API, source notation, or general
intervention algebra.

## Deletion or promotion path

Delete the experiment if results depend on tuple or dictionary order, if mixture and
fixed production cannot remain causally distinct, or if an option bag preserves all
observable behavior. Promote only the backend-neutral anti-accidental-choice law
after the hostile reversed-order witness passes. Never promote these seeds, kernels,
weights, plans, or harness diagnostics.

