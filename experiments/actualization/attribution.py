"""Outcome-only attribution that deliberately lacks privileged causal history."""

from __future__ import annotations

from .source_model import Mechanism, ObserverAttribution, WorldState


def attribute_from_state(state: WorldState) -> ObserverAttribution:
    return ObserverAttribution(
        state,
        frozenset(
            {
                Mechanism.CRITERION_ONLY,
                Mechanism.POLICY_GUIDANCE,
                Mechanism.HIDDEN_BIAS,
            }
        ),
        selected=None,
    )
