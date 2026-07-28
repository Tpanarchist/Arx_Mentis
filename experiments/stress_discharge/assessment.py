"""Resolution, acceptance, and progress remain separate assessments."""

from __future__ import annotations

from .loading import load_at
from .source_model import (
    AcceptanceAssessment,
    AcceptanceCriterion,
    NetworkState,
    ProgressAssessment,
    ProgressCriterion,
    ResolutionAssessment,
    ResolutionRule,
    Site,
)


def assess_resolution(
    state: NetworkState,
    rule: ResolutionRule,
) -> ResolutionAssessment:
    maximum = max(load_at(state.field, site) for site in Site)
    resolved = maximum <= rule.maximum_site_load and (
        rule.rupture_allowed or not state.ruptured_links
    )
    return ResolutionAssessment(state, rule, resolved)


def assess_acceptance(
    state: NetworkState,
    criterion: AcceptanceCriterion,
) -> AcceptanceAssessment:
    accepted = (
        state.delivered >= criterion.minimum_delivered
        and state.dissipated <= criterion.maximum_dissipated
        and (criterion.rupture_allowed or not state.ruptured_links)
    )
    return AcceptanceAssessment(state, criterion, accepted)


def assess_progress(
    state: NetworkState,
    criterion: ProgressCriterion,
) -> ProgressAssessment:
    return ProgressAssessment(
        state,
        criterion,
        state.delivered >= criterion.minimum_delivered,
    )
