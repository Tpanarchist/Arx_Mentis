from __future__ import annotations

from dataclasses import fields, replace

from experiments.euclid_i_1.model import (
    Conformity,
    Construction,
    Effect,
    ExperimentRefusal,
    Form,
    IntersectionPoint,
    OrientationTrigger,
    Potential,
    Side,
    cast,
    make_context,
    make_proposition,
)


def apex(effect: Effect) -> IntersectionPoint:
    return next(
        point for point in effect.form.points if isinstance(point, IntersectionPoint)
    )


def test_same_spell_is_inspectable_data_and_castable_instructions() -> None:
    line_ab, spell = make_proposition()

    assert isinstance(spell, Form)
    assert spell.name == "Euclid I.1"
    assert len(spell.steps) == 5
    assert all(isinstance(step, Form) for step in spell.steps)

    result = cast(spell, make_context(line_ab, selected_side=Side.LEFT))

    assert isinstance(result, Effect)
    assert result.comparison.will is spell.will


def test_unoriented_cast_preserves_both_options_without_a_default() -> None:
    line_ab, spell = make_proposition()

    result = cast(spell, make_context(line_ab))

    assert isinstance(result, Potential)
    assert [field.name for field in fields(Potential)] == ["options", "trigger"]
    assert isinstance(result.options, frozenset)
    assert len(result.options) == 2
    assert {apex(effect).side for effect in result.options} == {
        Side.LEFT,
        Side.RIGHT,
    }
    assert isinstance(result.trigger, OrientationTrigger)
    assert not hasattr(result, "selected")


def test_context_orientation_settles_the_corresponding_effect() -> None:
    line_ab, spell = make_proposition()

    left = cast(spell, make_context(line_ab, selected_side=Side.LEFT))
    right = cast(spell, make_context(line_ab, selected_side=Side.RIGHT))

    assert isinstance(left, Effect)
    assert isinstance(right, Effect)
    assert apex(left).side is Side.LEFT
    assert apex(right).side is Side.RIGHT
    assert left != right


def test_cast_preserves_source_and_produces_a_new_form() -> None:
    line_ab, spell = make_proposition()
    original = line_ab

    result = cast(spell, make_context(line_ab, selected_side=Side.LEFT))

    assert isinstance(result, Effect)
    assert line_ab is original
    assert line_ab in result.form.lines
    assert result.form is not line_ab
    assert len(result.form.points) == 3
    assert len(result.form.lines) == 3


def test_spell_names_every_construction_and_context_supplies_it() -> None:
    line_ab, spell = make_proposition()
    context = make_context(line_ab)

    used = {step.postulate.construction for step in spell.steps}
    required = {postulate.construction for postulate in spell.requirements.postulates}
    available = {postulate.construction for postulate in context.postulates}

    assert used == required
    assert {step.postulate for step in spell.steps} == spell.requirements.postulates
    assert {
        spell.demonstration.radius_definition,
        spell.demonstration.equilateral_definition,
    } == spell.requirements.definitions
    assert {
        spell.demonstration.equality_common_notion
    } == spell.requirements.common_notions
    assert used == {
        Construction.CIRCLE_FROM_CENTER_AND_POINT,
        Construction.CIRCLE_INTERSECTIONS,
        Construction.LINE_BETWEEN_POINTS,
    }
    assert required <= available

    result = cast(spell, make_context(line_ab, selected_side=Side.LEFT))
    assert isinstance(result, Effect)
    assert all(entry.basis in context.postulates for entry in result.trace.entries)
    assert {entry.basis.construction for entry in result.trace.entries} == required


def test_demonstration_is_traceable_to_context_rules_and_will() -> None:
    line_ab, spell = make_proposition()
    context = make_context(line_ab, selected_side=Side.LEFT)

    result = cast(spell, context)

    assert isinstance(result, Effect)
    available_rules = context.definitions | context.common_notions
    assert all(step.basis in available_rules for step in result.demonstration.steps)
    assert len(result.demonstration.steps) == 4
    assert all(result.demonstration.steps[index].witnesses for index in (0, 1))
    assert result.demonstration.conclusion.lines == result.form.lines
    assert result.comparison.evidence == result.demonstration.conclusion
    assert result.comparison.judgement is Conformity.CONFORMS


def test_missing_primitive_returns_an_owned_harness_refusal() -> None:
    line_ab, spell = make_proposition()
    context = make_context(line_ab)
    omitted = next(iter(context.postulates))
    incomplete = replace(context, postulates=context.postulates - {omitted})

    result = cast(spell, incomplete)

    assert isinstance(result, ExperimentRefusal)
    assert omitted in result.missing
    assert isinstance(result, Form)
