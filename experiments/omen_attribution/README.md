# State Zero Experiment 006: Omen, Correspondence, and Attribution

**Question:** When an observed event corresponds to a previously recorded aim, how
do occurrence, correspondence, apparent surprise, and competing causal explanations
remain distinct when those explanations have no honest transitive symmetry?

Stephen Mace's motivating analogy connects virtual mediation to both successful
conjurations and omens in
[*Sorcery as Virtual Mechanics*](https://www.scribd.com/doc/96245037/37606530-Stephen-Mace-Sorcery-as-Virtual-Mechanics).
This experiment does not test that occult claim. It uses attribution as an adversarial
boundary for the algebra discussed in ADR 0008.

## Neutral model first

The executable mechanics begin with `RecordedAim`, `Event`, `Observation`,
`MatchRule`, `Correspondence`, `Baseline`, `Hypothesis`, `Evidence`, `Intervention`,
and `AttributionReport`. They import neither another experiment nor `src/arx_mentis`.
Foundation correspondence is attempted afterward in `foundation_mapping.py`.

The model independently records:

```text
event occurred
!= event corresponds to recorded aim
!= correspondence exceeds baseline
!= operation caused event
```

## Assumptions

- Every stream and intervention result is declared deterministic evidence, not a
  random or empirical simulator.
- Integer support scores demonstrate unequal hypotheses but are not probabilities or
  proposed language semantics.
- A world record contains one definite cause; its observer view deliberately omits
  that cause.
- Match rules are exact symbolic predicates used only by this probe.

## Success signal and executable witness

- Ordinary chance can produce a real correspondence without anomalous attribution.
- Reporting only matches raises apparent correspondence without changing production.
- A recorded aim can mediate an outcome through operator attention and behavior.
- The same public event can arise through several definite causal channels.
- Relevant evidence changes attribution support; irrelevant evidence is inert and
  contradictory evidence remains explicit.
- Blocking operator behavior distinguishes operator-dependent and autonomous
  hypotheses while several explanations remain supported.
- A forced cyclic permutation of the six hypotheses is transitive only by destroying
  their causal variables, evidence requirements, and unequal prior support. The
  structure-preserving relation has multiple disconnected orbits.
- A world cause can be definite and hidden while Reader-relative attribution remains
  underdetermined; occurrence remains settled throughout.

Run with:

```console
python -m experiments.omen_attribution
python -m pytest tests/experiments/test_omen_attribution.py
```

## Foundation mapping and friction

The result narrows rather than rejects ADR 0008. Symmetric unresolved constructions
retain their algebraic obligations. Unequal epistemic hypotheses are a counterexample
to treating unresolvedness itself as an equivariant family. Names such as Potential,
Uncertainty, Chance, Open, and Search remain provisional; this experiment establishes
only that their semantic jobs cannot be collapsed without evidence.

## Deletion or promotion path

Delete the attribution model if one declared structure-preserving transitive action
honestly relates all hypotheses. Retain the counterexample if forced symmetry changes
their evidence laws or causal structure. Promote no score, carrier, foundation type,
or claim about omens from this experiment.
