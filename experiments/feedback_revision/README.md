# State Zero Experiment 011: Feedback and Model Revision

**Status:** Disposable evidence experiment. Nothing here is package API or accepted
language semantics.

## Question

Can an operative model be revised from observed results while preserving what was
predicted beforehand, what actually occurred, which evidence justified revision,
and whether the revised model performs better outside the evidence used to construct
it?

A secondary synopsis of Stephen Mace's experimental framing in
[*Sorcery as Virtual Mechanics*](https://www.scribd.com/document/988582460/Stephen-Mace-Primer-Sorcery-as-Virtual-Mechanics-Squeezing-Being)
motivates the feedback question. It is not treated as a substitute for the primary
text. This neutral experiment tests record and information boundaries only; it makes
no occult, empirical, causal-inference, or statistical claim.

## Assumptions

- Twelve fixed cases replace randomness and statistical inference.
- Features are exposed to prediction while outcomes become available only after all
  corresponding predictions have been committed.
- Six calibration cases are admissible revision evidence; six sealed holdout cases
  are available only for independent evaluation.
- Exact-match scores are finite harness comparisons, not probability estimates or a
  general account of model validity.
- Frozen Python records and integer record order are disposable carriers.

## Exact finite world

Cases `C00` through `C05` form calibration and `C06` through `C11` form holdout. Each
has two declared binary features and one fixed binary outcome. Initial Model A reads
feature X; initial Model B reads feature Y. All models receive `CaseInput`, which
contains no outcome.

The exact assessment results are:

```text
                         calibration   holdout
Model A, feature X           3/6         4/6
overfit memorizer            6/6         2/6
generalized XOR              6/6         6/6
equivalent lookup            6/6         6/6
```

The memorizer stores only admitted calibration outcomes and uses a deliberately poor
fallback on unseen cases. The XOR and lookup revisions are structurally different
but make the same predictions in this finite world.

## Persistent history

A `TrialPlan` precedes every `Prediction`; an outcome-producing occurrence follows;
an `Observation` records what became available; and an `Assessment` separately
compares committed predictions with observations under a declared rule.

Revision constructs a new version:

```text
V0 + EvidenceSet + RevisionRule -> Revision -> V1
```

`Lineage` records the source version, admitted evidence set, revision rule, and new
version. V0, its predictions, its observations, and its assessment remain unchanged.
`Replay` records what a selected version *would predict* on historical inputs while
retaining identifiers for what the historical version *did predict*.

The central provisional finding is therefore prospective:

> Learning changes future models. It does not change past predictions.

## Independent boundaries

- **Observation versus assessment versus revision:** availability neither judges nor
  mutates by itself.
- **Calibration versus holdout:** revision rules admit only `C00`-`C05`; holdout
  leakage returns an owned result.
- **Fit versus improvement:** perfect calibration fit can coincide with worse
  holdout behavior.
- **Historical prediction versus replay:** `did predict` and `would predict` remain
  different records.
- **Correction versus erasure:** correction creates a new evidence set and
  assessment while retaining the erroneous observation and original assessment.
- **Current behavior versus lineage:** equal models can retain different derivation
  histories.
- **Passive prediction versus adaptive intervention:** a revised model can change an
  intervention and thereby change later outcomes. Self-fulfilled accuracy is not
  passive confirmation.
- **Working selection versus truth:** selection under a declared evaluation policy
  does not install a model as the world's causal structure.

## ADR 0010 boundary

Equal calibration and holdout scores leave the XOR and lookup revisions as distinct
admissible alternatives with no score discriminator. Forward and reversed candidate
storage return the same owned conflict. A separately declared lower-complexity policy
may select XOR because complexity is then semantic. The experiment therefore adds a
hostile witness for ADR 0010 without imposing one universal ambiguity response.

## Hostile countermodels

The experiment owns rejections for prediction rewriting, failure deletion,
outcome-defined success, holdout evidence leakage, one-event validation,
overfit-as-improvement, current-version identity, replay-as-history,
self-fulfillment-as-prediction, revision-order tie-breaking, contradiction erasure,
and model-as-truth.

## Success signal

The experiment succeeds if executable witnesses preserve all prediction, outcome,
observation, assessment, evidence, revision, replay, holdout, correction, lineage,
attribution, intervention, and selection-policy boundaries without importing package
types or earlier experiments.

## Executable witness

```powershell
.venv\Scripts\python.exe -m experiments.feedback_revision
.venv\Scripts\python.exe -m pytest tests/experiments/test_feedback_revision.py
```

## Result and boundary

The finite witness demonstrates prospective revision without retroactive mutation.
It also demonstrates overfit, independent holdout improvement, correction history,
lineage-sensitive identity pressure, and adaptive self-fulfillment. These results do
not establish statistical learning theory, model truth, a general revision algebra,
or any foundation mapping.

Passing does **not** earn another ADR. The prospective-not-retroactive finding remains
provisional until the same semantic job appears independently in unrelated domains.

## Deletion or promotion path

Delete the experiment if revision can see holdout outcomes, if replay replaces
historical predictions, if correction deletes contrary records, if equal-score
selection depends on candidate order, or if old versions mutate. Promote only a
backend-neutral historical obligation after it independently passes the synthesis
gate. Never promote these cases, models, scores, rule enums, record orders, or Python
carriers.
