from __future__ import annotations

from dataclasses import fields, replace

from experiments.ars_astronomica_settlement.model import (
    DiagnosticKind,
    ElaboratedSpell,
    ExperimentalDiagnostic,
    Operation,
    Point,
    Potential,
    ProjectionEffect,
    Refused,
    cast,
    elaborate,
    image,
    make_experiment,
    project,
    settle,
    with_observations,
)


def setup() -> tuple[object, ElaboratedSpell, ElaboratedSpell, Potential]:
    experiment = make_experiment()
    discrimination = elaborate(experiment.discrimination.spell, experiment.context.ars)
    projection = elaborate(experiment.projection.spell, experiment.context.ars)
    assert isinstance(discrimination, ElaboratedSpell)
    assert isinstance(projection, ElaboratedSpell)
    potential = cast(experiment.discrimination, discrimination, experiment.context)
    assert isinstance(potential, Potential)
    return experiment, discrimination, projection, potential


def test_requirements_are_derived_and_potential_is_a_family() -> None:
    experiment, discrimination, _, potential = setup()

    assert not hasattr(experiment.discrimination.spell, "requirements")
    assert len(discrimination.derived_capabilities) == 2
    assert [field.name for field in fields(Potential)] == ["family", "settlement"]
    assert not hasattr(potential, "options")
    assert len(image(potential)) == 2


def test_either_recorded_observation_settles_the_same_family() -> None:
    experiment, _, _, potential = setup()

    bright = settle(
        potential,
        with_observations(experiment.context, experiment.bright),
    )
    dark = settle(
        potential,
        with_observations(experiment.context, experiment.dark),
    )

    assert isinstance(bright, Point)
    assert isinstance(dark, Point)
    assert bright.selected != dark.selected
    assert bright.evidence.observation == experiment.bright
    assert dark.evidence.observation == experiment.dark


def test_irrelevant_observation_preserves_identical_potential() -> None:
    experiment, _, _, potential = setup()

    result = settle(
        potential,
        with_observations(experiment.context, experiment.irrelevant),
    )

    assert result is potential


def test_contradictory_evidence_is_owned_diagnostic() -> None:
    experiment, _, _, potential = setup()
    context = with_observations(
        experiment.context,
        experiment.bright,
        experiment.dark,
    )

    result = settle(potential, context)

    assert isinstance(result, ExperimentalDiagnostic)
    assert result.kind is DiagnosticKind.CONTRADICTORY_EVIDENCE


def test_projection_maps_through_family_and_also_accepts_settled_point() -> None:
    experiment, _, projection, potential = setup()

    unsettled = project(
        experiment.projection,
        projection,
        potential,
        experiment.context,
    )
    selected = settle(
        potential,
        with_observations(experiment.context, experiment.bright),
    )
    assert isinstance(selected, Point)
    concrete = project(
        experiment.projection,
        projection,
        selected,
        experiment.context,
    )
    selected_projection = settle(
        unsettled,
        with_observations(experiment.context, experiment.bright),
    )

    assert isinstance(unsettled, Potential)
    assert len(image(unsettled)) == 2
    assert unsettled.family.stabilizer is potential.family.stabilizer
    assert isinstance(concrete, ProjectionEffect)
    assert isinstance(selected_projection, Point)
    assert selected_projection.selected == concrete.prediction


def test_missing_derived_capability_refuses_projection() -> None:
    experiment, _, projection, potential = setup()
    missing = next(
        capability
        for capability in projection.derived_capabilities
        if capability.operation is Operation.PROJECT_MODEL
    )
    context = replace(
        experiment.context,
        capabilities=experiment.context.capabilities - {missing},
    )

    result = project(experiment.projection, projection, potential, context)

    assert isinstance(result, Refused)
    assert result.missing is missing


def test_reversing_candidate_declaration_order_changes_no_observation() -> None:
    experiment = make_experiment()
    discrimination = elaborate(experiment.discrimination.spell, experiment.context.ars)
    projection = elaborate(experiment.projection.spell, experiment.context.ars)
    assert isinstance(discrimination, ElaboratedSpell)
    assert isinstance(projection, ElaboratedSpell)
    direct = cast(experiment.discrimination, discrimination, experiment.context)
    reversed_form = replace(
        experiment.discrimination,
        candidates=tuple(reversed(experiment.discrimination.candidates)),
    )
    reversed_family = cast(reversed_form, discrimination, experiment.context)
    assert isinstance(direct, Potential)
    assert isinstance(reversed_family, Potential)
    assert image(direct) == image(reversed_family)

    for observation in (experiment.bright, experiment.dark):
        observed_context = with_observations(experiment.context, observation)
        direct_point = settle(direct, observed_context)
        reversed_point = settle(reversed_family, observed_context)
        assert isinstance(direct_point, Point)
        assert isinstance(reversed_point, Point)
        assert direct_point.selected == reversed_point.selected
        direct_projection = project(
            experiment.projection,
            projection,
            direct_point,
            experiment.context,
        )
        reversed_projection = project(
            experiment.projection,
            projection,
            reversed_point,
            experiment.context,
        )
        assert isinstance(direct_projection, ProjectionEffect)
        assert isinstance(reversed_projection, ProjectionEffect)
        assert direct_projection.prediction == reversed_projection.prediction
