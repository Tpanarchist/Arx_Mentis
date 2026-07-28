from __future__ import annotations

from dataclasses import replace

import experiments.ars_dialectica_verification.model as model
from experiments.ars_dialectica_verification.model import (
    Conforms,
    Counterexample,
    Effect,
    ElaboratedSpell,
    Failed,
    FailureKind,
    InvalidDemonstration,
    Open,
    Refused,
    VerifiedDemonstration,
    elaborate,
    make_experiment,
)
from experiments.ars_dialectica_verification.production import cast
from experiments.ars_dialectica_verification.verification import (
    check_will,
    decide,
    verify_demonstration,
)


def _cast_valid_effect() -> tuple[model.Experiment, Effect]:
    experiment = make_experiment()
    elaborated = elaborate(experiment.spell, experiment.ars)
    assert isinstance(elaborated, ElaboratedSpell)
    result = cast(elaborated, experiment.context)
    assert isinstance(result, Effect)
    return experiment, result


def test_valid_proof_and_conforming_effect_are_separate_results() -> None:
    experiment, effect = _cast_valid_effect()

    verification = verify_demonstration(effect, experiment.context)
    conformity = check_will(effect, experiment.ars)

    assert isinstance(verification, VerifiedDemonstration)
    assert verification.checked_premises == experiment.spell.starting_premises
    assert verification.checked_applications == 2
    assert verification.checked_conclusion == experiment.bloom
    assert isinstance(conformity, Conforms)


def test_valid_construction_can_diverge_from_will() -> None:
    experiment = make_experiment()
    divergent_spell = replace(
        experiment.spell,
        will=model.Will("derive sprout", experiment.sprout),
    )
    elaborated = elaborate(divergent_spell, experiment.ars)
    assert isinstance(elaborated, ElaboratedSpell)
    effect = cast(elaborated, experiment.context)
    assert isinstance(effect, Effect)

    verification = verify_demonstration(effect, experiment.context)
    assert isinstance(verification, VerifiedDemonstration)
    assert isinstance(check_will(effect, experiment.ars), Counterexample)


def test_missing_starting_premise_is_failed_cast() -> None:
    experiment = make_experiment()
    context = replace(
        experiment.context,
        premises=experiment.context.premises - {experiment.rain},
    )
    elaborated = elaborate(experiment.spell, experiment.ars)
    assert isinstance(elaborated, ElaboratedSpell)

    result = cast(elaborated, context)

    assert isinstance(result, Failed)
    assert result.kind is FailureKind.MISSING_PREMISE
    assert result.related == frozenset({experiment.rain})


def test_available_but_unpermitted_rule_is_refused_cast() -> None:
    experiment = make_experiment()
    context = replace(experiment.context, permissions=frozenset())
    elaborated = elaborate(experiment.spell, experiment.ars)
    assert isinstance(elaborated, ElaboratedSpell)

    result = cast(elaborated, context)

    assert isinstance(result, Refused)
    assert result.missing_capability is model.MODUS_PONENS_CAPABILITY


def test_corrupted_proof_is_invalid_demonstration() -> None:
    experiment, effect = _cast_valid_effect()
    applications = effect.demonstration.applications
    corrupted_application = replace(applications[1], conclusion=experiment.sprout)
    corrupted_demonstration = replace(
        effect.demonstration,
        applications=(applications[0], corrupted_application),
    )
    corrupted_effect = replace(effect, demonstration=corrupted_demonstration)

    result = verify_demonstration(corrupted_effect, experiment.context)

    assert isinstance(result, InvalidDemonstration)
    assert result.step_index == 1


def test_open_proposition_is_not_a_potential() -> None:
    experiment = make_experiment()

    result = decide(experiment.sprout, experiment.context)

    assert isinstance(result, Open)
    assert not hasattr(model, "Potential")


def test_sources_are_immutable_and_effect_is_new() -> None:
    experiment, effect = _cast_valid_effect()

    assert effect is not experiment.spell
    assert effect.source is experiment.spell
    assert experiment.spell.starting_premises == experiment.context.premises
