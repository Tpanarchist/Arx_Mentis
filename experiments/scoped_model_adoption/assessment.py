"""Evidence-sensitive model assessment without operational authority."""

from __future__ import annotations

from .models import model_action
from .records import Assessment, EpistemicAmbiguity, Model, Scope, ScopeScore, WorldCase


def assess_model(
    model: Model,
    cases: tuple[WorldCase, ...],
    *,
    confidence: int,
    created_order: int = 10,
) -> Assessment:
    scores = tuple(
        _scope_score(model, scope, cases) for scope in (Scope.AMBER, Scope.VIOLET)
    )
    return Assessment(
        f"assessment:{model.identifier}",
        model.identifier,
        scores,
        sum(item.accepted_count for item in scores),
        sum(item.total_count for item in scores),
        confidence,
        "required-action-match",
        created_order,
    )


def _scope_score(
    model: Model,
    scope: Scope,
    cases: tuple[WorldCase, ...],
) -> ScopeScore:
    scoped = tuple(case for case in cases if case.scope is scope)
    return ScopeScore(
        scope,
        sum(model_action(model, case) is case.required_action for case in scoped),
        len(scoped),
    )


def compare_assessments(
    assessments: tuple[Assessment, ...],
) -> EpistemicAmbiguity:
    scores = {
        (assessment.global_accepted_count, assessment.global_total_count)
        for assessment in assessments
    }
    if len(scores) != 1:
        raise ValueError("comparison is not score-ambiguous")
    return EpistemicAmbiguity(
        frozenset(item.model_identifier for item in assessments),
        next(iter(scores)),
        "equal assessment score does not identify one model",
    )
