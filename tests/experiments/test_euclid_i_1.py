from __future__ import annotations

from dataclasses import fields, replace

from experiments.euclid_i_1.model import (
    CandidateKind,
    Conforms,
    Effect,
    ElaboratedSpell,
    ElaborationRefusal,
    Failed,
    FrameDependentCheck,
    FramePlacement,
    GroupDiagnostic,
    InvariantWill,
    NonInvariantWill,
    Operation,
    Pair,
    Parity,
    Point,
    Potential,
    Produced,
    Refused,
    Side,
    Verdict,
    Will,
    WillPredicate,
    assess_default,
    assess_group,
    cast,
    check,
    elaborate,
    frame_placement_report,
    image,
    independent,
    independent_copy,
    make_experiment,
    settle,
    shared,
    twisted,
    validate_will,
    with_frame,
)


def produced_potential() -> tuple[object, ElaboratedSpell, Effect, Potential]:
    experiment = make_experiment()
    elaborated = elaborate(experiment.spell, experiment.extended_ars)
    assert isinstance(elaborated, ElaboratedSpell)
    result = cast(elaborated, experiment.context)
    assert isinstance(result, Produced)
    assert isinstance(result.effect.form, Potential)
    return experiment, elaborated, result.effect, result.effect.form


def test_requirements_are_discovered_and_missing_intersection_refuses() -> None:
    experiment = make_experiment()

    first = elaborate(experiment.spell, experiment.initial_ars)
    second = elaborate(experiment.spell, experiment.extended_ars)

    assert not hasattr(experiment.spell, "required_capabilities")
    assert isinstance(first, ElaborationRefusal)
    assert first.source is experiment.spell
    assert first.missing_operation is Operation.INTERSECT_CIRCLES
    assert len(first.elaborated_prefix) == 2
    assert isinstance(second, ElaboratedSpell)
    assert second.source is experiment.spell
    assert len(second.derived_requirements) == 3


def test_potential_is_an_equivariant_family_not_stored_options() -> None:
    _, _, _, potential = produced_potential()

    assert [field.name for field in fields(Potential)] == ["family", "settlement"]
    assert not hasattr(potential, "options")
    assert len(potential.family.torsor.frames) == 2
    assert len(image(potential)) == 2
    assert potential.family.law.verified is Verdict.HOLDS


def test_construction_passes_through_potential_without_settlement() -> None:
    experiment, elaborated, effect, potential = produced_potential()
    result = cast(elaborated, experiment.context)

    assert isinstance(result, Produced)
    assert isinstance(effect.form, Potential)
    assert len(result.trace) == 5
    assert not experiment.context.frame_witnesses
    assert all(len(triangle.sides) == 2 for triangle in image(potential))


def test_direct_twisted_and_independent_composition_are_distinct() -> None:
    _, _, _, potential = produced_potential()
    direct = shared(potential, potential)
    twist = twisted(potential, potential)
    other = independent_copy(potential, "independent reflection")
    product_family = independent(potential, other)

    assert len(image(direct)) == 2
    assert len(image(twist)) == 2
    assert len(image(product_family)) == 4
    assert all(
        isinstance(value, Pair) and value.first == value.second
        for value in image(direct)
    )
    assert all(
        isinstance(value, Pair) and value.first != value.second
        for value in image(twist)
    )


def test_frame_transfer_preserves_potential_until_witnessed() -> None:
    experiment, _, _, potential = produced_potential()

    unchanged = settle(potential, experiment.context)
    witnessed_context = with_frame(experiment.context, potential, Parity.FLIPPED)
    settled = settle(potential, witnessed_context)

    assert unchanged is potential
    assert isinstance(settled, Point)
    assert len(settled.evidence.witnesses) == 1


def test_invariant_will_conforms_without_settling_effect() -> None:
    experiment, _, effect, potential = produced_potential()

    validation = validate_will(
        experiment.spell.will,
        experiment.extended_ars,
        experiment.givens,
    )
    result = check(experiment.spell.will, effect, experiment.context)

    assert isinstance(validation, InvariantWill)
    assert isinstance(result, Conforms)
    assert effect.form is potential
    assert len(result.evidence.proofs) == 2
    assert result.evidence.bridge.target_ars == "Ars Arithmetica"
    assert all(
        equality.ars_name == "Ars Arithmetica"
        for proof in result.evidence.proofs
        for equality in proof.equalities
    )


def test_noninvariant_will_is_detected_and_yields_potential_truth() -> None:
    experiment, _, effect, _ = produced_potential()
    side_will = Will(
        "apex on positive side",
        WillPredicate.APEX_POSITIVE,
        experiment.givens.base,
    )

    validation = validate_will(
        side_will,
        experiment.extended_ars,
        experiment.givens,
    )
    result = check(side_will, effect, experiment.context)

    assert isinstance(validation, NonInvariantWill)
    assert isinstance(result, FrameDependentCheck)
    assert {truth.verdict for truth in image(result.family)} == {
        Verdict.HOLDS,
        Verdict.DOES_NOT_HOLD,
    }


def test_default_legitimacy_requires_fixed_and_constructible() -> None:
    experiment = make_experiment()

    intersection = assess_default(
        CandidateKind.POSITIVE_INTERSECTION,
        experiment.extended_ars,
        experiment.givens,
    )
    midpoint = assess_default(
        CandidateKind.MIDPOINT,
        experiment.extended_ars,
        experiment.givens,
    )

    assert intersection.fixed_by_stabilizer is Verdict.DOES_NOT_HOLD
    assert intersection.constructible is Verdict.HOLDS
    assert intersection.legitimate_default is Verdict.DOES_NOT_HOLD
    assert midpoint.fixed_by_stabilizer is Verdict.HOLDS
    assert midpoint.constructible is Verdict.DOES_NOT_HOLD
    assert midpoint.legitimate_default is Verdict.DOES_NOT_HOLD
    assert midpoint.equivariance_hypothesis is Verdict.HOLDS


def test_ambient_group_is_declared_by_ars_and_must_act_informatively() -> None:
    experiment = make_experiment()
    informative = assess_group(experiment.extended_ars, experiment.givens)
    small_group = replace(
        experiment.extended_ars.transformation_group,
        elements=frozenset({Parity.IDENTITY}),
    )
    too_small = assess_group(
        replace(experiment.extended_ars, transformation_group=small_group),
        experiment.givens,
    )

    assert informative.diagnostic is GroupDiagnostic.INFORMATIVE
    assert too_small.diagnostic is GroupDiagnostic.TRIVIAL_ACTION


def test_direction_chirality_and_frame_placement_obey_xor() -> None:
    _, _, _, potential = produced_potential()
    direct = shared(potential, potential)
    twist = twisted(potential, potential)
    product_family = independent(
        potential,
        independent_copy(potential, "second segment"),
    )

    report = frame_placement_report(direct, twist, product_family)

    assert report.original is Side.POSITIVE
    assert report.direction_flipped is Side.NEGATIVE
    assert report.chirality_flipped is Side.NEGATIVE
    assert report.both_flipped is Side.POSITIVE
    assert report.direct_joint_outcomes == 2
    assert report.twisted_joint_outcomes == 2
    assert report.independent_joint_outcomes == 4
    assert report.favored is FramePlacement.POTENTIAL


def test_context_capability_refusal_and_permitted_failure_are_owned() -> None:
    experiment = make_experiment()
    elaborated = elaborate(experiment.spell, experiment.extended_ars)
    assert isinstance(elaborated, ElaboratedSpell)
    intersection_capability = next(
        capability
        for capability in experiment.context.capabilities
        if capability.operation is Operation.INTERSECT_CIRCLES
    )
    missing_context = replace(
        experiment.context,
        capabilities=experiment.context.capabilities - {intersection_capability},
    )
    refused = cast(elaborated, missing_context)

    degenerate = make_experiment(degenerate=True)
    degenerate_spell = elaborate(degenerate.spell, degenerate.extended_ars)
    assert isinstance(degenerate_spell, ElaboratedSpell)
    failed = cast(degenerate_spell, degenerate.context)

    assert isinstance(refused, Refused)
    assert refused.missing.operation is Operation.INTERSECT_CIRCLES
    assert isinstance(failed, Failed)
