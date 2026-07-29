"""The exact two-scope world and self-fulfilling environment."""

from __future__ import annotations

from .records import Action, ActionRecord, CausalRecord, Outcome, Scope, WorldCase

AMBER_CASES = (
    WorldCase("A00", Scope.AMBER, Action.LEFT, Action.LEFT, Action.LEFT),
    WorldCase("A01", Scope.AMBER, Action.RIGHT, Action.RIGHT, Action.RIGHT),
    WorldCase("A02", Scope.AMBER, Action.LEFT, Action.RIGHT, Action.LEFT),
    WorldCase("A03", Scope.AMBER, Action.RIGHT, Action.LEFT, Action.RIGHT),
    WorldCase("A04", Scope.AMBER, Action.LEFT, Action.RIGHT, Action.LEFT),
    WorldCase("A05", Scope.AMBER, Action.RIGHT, Action.LEFT, Action.RIGHT),
)

VIOLET_CASES = (
    WorldCase("V00", Scope.VIOLET, Action.LEFT, Action.LEFT, Action.LEFT),
    WorldCase("V01", Scope.VIOLET, Action.RIGHT, Action.RIGHT, Action.RIGHT),
    WorldCase("V02", Scope.VIOLET, Action.RIGHT, Action.LEFT, Action.LEFT),
    WorldCase("V03", Scope.VIOLET, Action.LEFT, Action.RIGHT, Action.RIGHT),
    WorldCase("V04", Scope.VIOLET, Action.RIGHT, Action.LEFT, Action.LEFT),
    WorldCase("V05", Scope.VIOLET, Action.LEFT, Action.RIGHT, Action.RIGHT),
)

CASES = (*AMBER_CASES, *VIOLET_CASES)
SELF_FULFILLING_CASE = WorldCase(
    "S00",
    Scope.AMBER,
    Action.COOPERATE,
    Action.WITHHOLD,
    Action.COOPERATE,
)


def evaluate_action(action: ActionRecord, case: WorldCase, *, order: int) -> Outcome:
    return Outcome(
        f"outcome:{action.identifier}",
        case.identifier,
        action.action is case.required_action,
        "required-action-met" if action.action is case.required_action else "missed",
        CausalRecord(
            action.lineage.model_identifier,
            action.lineage.adoption_identifier,
            action.policy_identifier,
            action.identifier,
            action_participated=True,
        ),
        order,
    )


def cooperative_response(action: ActionRecord, *, order: int) -> Outcome:
    cooperative = action.action is Action.COOPERATE
    return Outcome(
        f"outcome:self-fulfilling:{action.identifier}",
        action.case_identifier,
        cooperative,
        "cooperative-response" if cooperative else "guarded-response",
        CausalRecord(
            action.lineage.model_identifier,
            action.lineage.adoption_identifier,
            action.policy_identifier,
            action.identifier,
            action_participated=True,
        ),
        order,
    )
