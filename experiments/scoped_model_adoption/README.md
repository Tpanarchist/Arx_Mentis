# State Zero Experiment 012: Scoped Model Adoption

**Status:** Disposable evidence experiment. Nothing here is package API or accepted
language semantics.

## Question

Can a model be adopted as a temporary, purpose-specific, scope-bound instrument
without being asserted as world truth?

A secondary synopsis of Stephen Mace's experimental framing in
[*Sorcery as Virtual Mechanics*](https://www.scribd.com/document/988582460/Stephen-Mace-Primer-Sorcery-as-Virtual-Mechanics-Squeezing-Being)
motivates the instrumental-model question. It is not treated as a substitute for the
primary text. This experiment tests neutral authority, scope, role, lifecycle, and
history boundaries only; it makes no occult, empirical, or ontological claim.

## Assumptions

- Twelve fixed cases replace randomness and empirical inference.
- A case exposes two action signals while its required action remains available only
  to assessment.
- Integer authority, confidence, cost, and record order are declared harness values,
  not proposed semantics.
- Frozen Python records are disposable carriers.

## Exact finite world

Amber contains `A00` through `A05`; Violet contains `V00` through `V05`. Model X
reads signal X and Model Y reads signal Y:

```text
                  Amber   Violet   Global
Model X             6/6      2/6     8/12
Model Y             2/6      6/6     8/12
Scoped X + Y         6/6      6/6    12/12
```

Neither model is globally adequate. Both can be lawful instruments because Model X
is adopted only for Amber and Model Y only for Violet. Their disjoint adoptions do
not compete over one operation.

## Independently observable stages

The experiment keeps `Model`, `Assessment`, `Adoption`, `Activation`, derived
artifact, action, outcome, `TruthAssertion`, `Revocation`, and `Lineage` separate.

An Adoption declares model, purpose, `UseMode`, scopes, authority, start and end
conditions, inactive initial state, revocation policy, provenance, and record order.
Availability or a high score does not create one. Activation creates a new active
record and does not mutate Adoption.

The same Model can be adopted under two explicit uses:

```text
predictive Adoption -> PredictionRule -> Prediction
control Adoption    -> DerivedPolicy  -> ActionRecord
```

Crossing these paths is refused at runtime, and an unsupported audit use returns an
owned result. The Model contains neither use as an intrinsic field.

## Scope, ambiguity, and policy

An Amber policy is unavailable in Violet. Overlapping same-purpose adoptions with no
resolution policy return `AdoptionConflict`; reversing candidate order preserves the
same conflict. Declared higher-authority or preferred-model policies may resolve the
overlap because they supply visible semantic discriminators.

Equal 8/12 assessments remain `EpistemicAmbiguity`. A limited-trial policy may still
create `OperationalCommitment` to one model without altering confidence or resolving
the assessment tie. Action can therefore proceed while knowledge remains unsettled,
but only through declared authority.

## Truth and self-fulfillment

Adoption never constructs `TruthAssertion`. Model X and Model Y can derive the same
successful local action while retaining different lineage, so success does not
identify an explanation.

A separate cooperation case records a model-derived cooperative action and an
environmental cooperative response. The outcome succeeds, but its `CausalRecord`
states that the action participated. It is self-fulfilled operational evidence, not
passive model validation.

## Revocation and switching

Two declared lifecycle policies remain lawful and distinct:

- **Live-linked:** revoking Adoption makes its existing derived artifact unavailable.
- **Snapshot:** revocation prevents new derivation while an existing artifact keeps
  independent authority until its declared expiry.

Unspecified cascade-versus-snapshot behavior returns an owned result. Revocation
blocks later Activation and never deletes Adoption, earlier actions, or their
lineage. Model switches create prospective `SwitchRecord` values; they do not rewrite
which model governed an earlier action.

## Hostile countermodels

The experiment owns rejections for model-is-adoption, assessment-is-authority,
adoption-is-truth, global-current-model, local-usefulness-as-universal-validity,
post-hoc scope, silent switching, first-adoption-wins, success-proves-model,
revocation-erases-history, implicit revocation policy, confidence-is-commitment,
commitment-is-confidence, self-fulfillment-as-validation, and
same-policy-as-same-origin.

## Success signal

The experiment succeeds if witnesses preserve all model, assessment, role, adoption,
activation, scope, authority, conflict, policy, truth, outcome, self-fulfillment,
revocation, snapshot, switching, and lineage boundaries without importing package
types or previous experiments.

## Executable witness

```powershell
.venv\Scripts\python.exe -m experiments.scoped_model_adoption
.venv\Scripts\python.exe -m pytest tests/experiments/test_scoped_model_adoption.py
```

## Result and boundary

Scoped adoption authorizes a model as an instrument without declaring it true. Local
usefulness does not widen scope; confidence does not grant authority; authority does
not raise confidence; and successful action does not recover model origin.

The experiment adds a third direct domain for explicit contextual roles after
Grammatica and Symbolic Release, and a third direct domain for declared
source-independent derived operation after Actualization and Symbolic Release. Those
recurrences justify narrowly scoped ADR candidates only. Neither is accepted here.

Scoped-instrumental adoption is itself one direct domain. Prospective model switching
is a second direct domain after Feedback and Model Revision. Both remain provisional.

## Deletion or promotion path

Delete the experiment if authority leaks across scopes, assessment silently activates
a model, truth follows from adoption or success, overlap depends on candidate order,
revocation erases history, or lifecycle behavior is guessed. Discuss promotion only
for carrier-independent obligations that independently satisfy the synthesis gate.
Never promote these cases, scores, enum values, policies, record orders, or Python
carriers.
