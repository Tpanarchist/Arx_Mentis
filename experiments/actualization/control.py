"""Policy-guided, criterion-only, and explicit hidden-weighting models."""

from __future__ import annotations

from collections.abc import Callable

from .acceptance import derive_acceptance, evaluate
from .source_model import (
    ActionPolicy,
    CausalStep,
    CausalTrace,
    Constraint,
    Controller,
    Feedback,
    HiddenWeighting,
    Mechanism,
    Outcome,
    Preference,
    RejectedMechanism,
    TargetForm,
    Transition,
    TransitionWeight,
    Unreachable,
    WorldState,
)
from .world import apply_transition, available_transitions

BASELINE_POLICY = ActionPolicy(
    "baseline-shortest",
    "transition-system",
    ("short-a-b", "unsafe-b-d", "safe-a-c", "safe-c-e", "safe-e-d"),
)
NO_CONSTRAINT = Constraint()


def derive_policy(target: TargetForm) -> ActionPolicy:
    if target.preference is Preference.SAFE:
        order = (
            "safe-a-c",
            "safe-c-e",
            "safe-e-d",
            "short-a-b",
            "unsafe-b-d",
        )
    else:
        order = BASELINE_POLICY.transition_order
    return ActionPolicy(f"policy:{target.identifier}", target.identifier, order)


def compile_controller(target: TargetForm, *, sustained: bool) -> Controller:
    return Controller(
        derive_policy(target),
        target if sustained else None,
        sustained_feedback=sustained,
    )


def derive_hidden_weighting(target: TargetForm) -> HiddenWeighting:
    if target.preference is Preference.SAFE:
        weighted = (
            TransitionWeight("safe-a-c", 5),
            TransitionWeight("safe-c-e", 5),
            TransitionWeight("safe-e-d", 5),
            TransitionWeight("short-a-b", 2),
            TransitionWeight("unsafe-b-d", 1),
        )
    else:
        weighted = (
            TransitionWeight("short-a-b", 5),
            TransitionWeight("unsafe-b-d", 5),
            TransitionWeight("safe-a-c", 2),
            TransitionWeight("safe-c-e", 2),
            TransitionWeight("safe-e-d", 2),
        )
    return HiddenWeighting(
        f"weighting:{target.identifier}",
        target.identifier,
        weighted,
    )


def _choose_by_policy(
    available: tuple[Transition, ...],
    policy: ActionPolicy,
) -> Transition | None:
    by_name = {transition.identifier: transition for transition in available}
    return next(
        (by_name[name] for name in policy.transition_order if name in by_name),
        None,
    )


def _run(
    source: WorldState,
    constraint: Constraint,
    *,
    mechanism: Mechanism,
    target_identifier: str | None,
    policy_identifier: str | None,
    weighting_identifier: str | None,
    target_available: bool,
    choose: Callable[[tuple[Transition, ...]], Transition | None],
    live_target: TargetForm | None = None,
) -> Outcome | Unreachable:
    state = source
    steps: list[CausalStep] = []
    feedback: list[Feedback] = []
    for index in range(constraint.maximum_steps + 1):
        if live_target is not None:
            accepted = evaluate(derive_acceptance(live_target), state).conforms
            feedback.append(Feedback(state, accepted, target_consulted=True))
            if accepted:
                return Outcome(
                    state,
                    _trace(
                        mechanism,
                        target_identifier,
                        policy_identifier,
                        weighting_identifier,
                        target_available,
                        steps,
                        feedback,
                    ),
                )
        elif state.gate_open:
            return Outcome(
                state,
                _trace(
                    mechanism,
                    target_identifier,
                    policy_identifier,
                    weighting_identifier,
                    target_available,
                    steps,
                    feedback,
                ),
            )

        if index == constraint.maximum_steps:
            break
        transition = choose(available_transitions(state, constraint))
        if transition is None:
            break
        next_state = apply_transition(state, transition)
        steps.append(
            CausalStep(
                index + 1,
                state,
                transition,
                next_state,
                target_consulted=live_target is not None,
            )
        )
        state = next_state

    trace = _trace(
        mechanism,
        target_identifier,
        policy_identifier,
        weighting_identifier,
        target_available,
        steps,
        feedback,
    )
    return Unreachable(state, trace, "no permitted transition reaches acceptance")


def _trace(
    mechanism: Mechanism,
    target_identifier: str | None,
    policy_identifier: str | None,
    weighting_identifier: str | None,
    target_available: bool,
    steps: list[CausalStep],
    feedback: list[Feedback],
) -> CausalTrace:
    return CausalTrace(
        mechanism,
        target_identifier,
        policy_identifier,
        weighting_identifier,
        target_available,
        tuple(steps),
        tuple(feedback),
    )


def run_criterion_only(
    source: WorldState,
    target: TargetForm,
    constraint: Constraint = NO_CONSTRAINT,
) -> Outcome | Unreachable:
    del target
    return _run(
        source,
        constraint,
        mechanism=Mechanism.CRITERION_ONLY,
        target_identifier=None,
        policy_identifier=BASELINE_POLICY.identifier,
        weighting_identifier=None,
        target_available=False,
        choose=lambda available: _choose_by_policy(available, BASELINE_POLICY),
    )


def run_controller(
    source: WorldState,
    controller: Controller,
    constraint: Constraint = NO_CONSTRAINT,
) -> Outcome | Unreachable:
    return _run(
        source,
        constraint,
        mechanism=Mechanism.POLICY_GUIDANCE,
        target_identifier=controller.policy.derived_from,
        policy_identifier=controller.policy.identifier,
        weighting_identifier=None,
        target_available=controller.live_target is not None,
        choose=lambda available: _choose_by_policy(available, controller.policy),
        live_target=controller.live_target if controller.sustained_feedback else None,
    )


def run_hidden_bias(
    source: WorldState,
    weighting: HiddenWeighting,
    constraint: Constraint = NO_CONSTRAINT,
) -> Outcome | Unreachable:
    weights = {item.transition: item.weight for item in weighting.weights}

    def choose(available: tuple[Transition, ...]) -> Transition | None:
        if not available:
            return None
        return max(available, key=lambda transition: weights[transition.identifier])

    return _run(
        source,
        constraint,
        mechanism=Mechanism.HIDDEN_BIAS,
        target_identifier=weighting.derived_from,
        policy_identifier=None,
        weighting_identifier=weighting.identifier,
        target_available=False,
        choose=choose,
    )


def reject_direct_assignment(
    source: WorldState,
    target: TargetForm,
) -> RejectedMechanism:
    proposed = WorldState(
        target.desired_position,
        target.minimum_resources,
        gate_open=target.desired_position.value == "d",
    )
    return RejectedMechanism(
        Mechanism.DIRECT_ASSIGNMENT,
        source,
        proposed,
        "assigning the acceptance state supplies no transition or causal account",
    )
