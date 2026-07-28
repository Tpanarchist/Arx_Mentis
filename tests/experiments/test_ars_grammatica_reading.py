from __future__ import annotations

from dataclasses import replace

import experiments.ars_grammatica_reading.model as model
from experiments.ars_grammatica_reading.model import (
    Audience,
    Clause,
    Counterexample,
    DiagnosticKind,
    Effect,
    Equivalent,
    ExperimentalDiagnostic,
    Failed,
    Inspection,
    Inspector,
    Interpreter,
    Name,
    Refused,
    RelationKind,
    check,
    make_experiment,
    read,
)


def test_same_non_spell_form_is_inspected_or_executed_by_typed_reader() -> None:
    experiment = make_experiment()

    inspection = read(experiment.form, experiment.examining_context)
    execution = read(experiment.form, experiment.executing_context)

    assert not hasattr(model, "Spell")
    assert not hasattr(model, "ReaderRole")
    assert isinstance(experiment.examining_context.reader, Inspector)
    assert isinstance(experiment.executing_context.reader, Interpreter)
    assert isinstance(inspection, Inspection)
    assert inspection.source is experiment.form
    assert inspection.nodes == experiment.form.nodes
    assert isinstance(execution, Effect)
    assert execution.source is experiment.form


def test_contexts_differ_only_by_reader() -> None:
    experiment = make_experiment()

    changed_reader = replace(
        experiment.examining_context,
        reader=experiment.executing_context.reader,
    )

    assert changed_reader == experiment.executing_context
    assert experiment.examining_context.reader != experiment.executing_context.reader


def test_execution_preserves_source_and_changes_only_declared_name() -> None:
    experiment = make_experiment()
    source = experiment.source_clause

    result = read(experiment.form, experiment.executing_context)

    assert isinstance(result, Effect)
    assert source is experiment.source_clause
    assert result.form is not source
    assert result.form.subject == result.will.expected_subject
    assert result.form.predicate is source.predicate
    assert result.trace.preserved_predicate is source.predicate
    assert result.trace.replaced == (source.subject, result.form.subject)
    comparison = check(result, experiment.executing_context)
    assert isinstance(comparison, Equivalent)
    assert comparison.ars_name == "Ars Grammatica"
    assert comparison.preserved_relation is source.predicate


def test_missing_permission_is_a_refusal_not_failed_execution() -> None:
    experiment = make_experiment()
    context = replace(experiment.executing_context, permissions=frozenset())

    result = read(experiment.form, context)

    assert isinstance(result, Refused)
    assert result.missing is model.RENAME_PERMISSION


def test_unsupported_reader_is_an_owned_diagnostic() -> None:
    experiment = make_experiment()

    result = read(experiment.form, experiment.unsupported_context)

    assert isinstance(result, ExperimentalDiagnostic)
    assert result.kind is DiagnosticKind.UNSUPPORTED_READER
    assert isinstance(experiment.unsupported_context.reader, Audience)


def test_malformed_relations_are_failed_construction_not_refusal() -> None:
    experiment = make_experiment()
    relation_to_remove = next(
        relation
        for relation in experiment.form.relations
        if relation.kind is RelationKind.TO
    )
    malformed = replace(
        experiment.form,
        relations=experiment.form.relations - {relation_to_remove},
    )

    result = read(malformed, experiment.executing_context)

    assert isinstance(result, Failed)


def test_will_comparison_can_reject_an_effect_after_execution() -> None:
    experiment = make_experiment()
    result = read(experiment.form, experiment.executing_context)
    assert isinstance(result, Effect)
    corrupted = replace(result, form=Clause(Name("apollo"), result.form.predicate))

    comparison = check(corrupted, experiment.executing_context)

    assert isinstance(comparison, Counterexample)
