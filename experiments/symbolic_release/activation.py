"""Activation and execution are separate state transitions."""

from __future__ import annotations

from dataclasses import dataclass

from .source import (
    Activation,
    Carrier,
    CompiledPolicy,
    Execution,
    ExecutionRefused,
    ExecutionStep,
    Interpretation,
    Outcome,
    Provenance,
    RejectedActivation,
    RejectionStage,
    WorldState,
)


@dataclass(frozen=True, slots=True)
class Transition:
    action: str
    source: str
    destination: str


TRANSITIONS = (
    Transition("safe-a-c", "A", "C"),
    Transition("safe-c-d", "C", "D"),
    Transition("fast-a-d", "A", "D"),
)


def activate(
    subject: Carrier | Interpretation,
) -> Activation | RejectedActivation:
    if isinstance(subject, Carrier):
        return RejectedActivation(
            subject,
            RejectionStage.ACTIVATION,
            "a stored carrier must be lawfully interpreted before activation",
        )
    if not isinstance(subject.artifact, CompiledPolicy):
        return RejectedActivation(
            subject,
            RejectionStage.ACTIVATION,
            "only a policy interpretation is activatable in this experiment",
        )
    provenance = Provenance(
        subject.artifact.provenance.source_identifiers,
        subject.artifact.provenance.encoding_rule,
        subject.artifact.provenance.carrier_symbol,
        (*subject.artifact.provenance.history, "activated"),
    )
    return Activation(
        f"activation:{subject.artifact.identifier}",
        subject.artifact,
        provenance,
    )


def execute(
    subject: Activation | Interpretation,
    source_state: WorldState,
) -> Outcome | ExecutionRefused:
    if isinstance(subject, Interpretation):
        return ExecutionRefused(
            subject,
            RejectionStage.EXECUTION,
            "an interpreted policy must be activated before execution",
        )

    state = source_state
    steps: list[ExecutionStep] = []
    by_action = {transition.action: transition for transition in TRANSITIONS}
    for action in subject.policy.actions:
        transition = by_action.get(action)
        if transition is None or transition.source != state.position:
            return ExecutionRefused(
                subject,
                RejectionStage.EXECUTION,
                f"action {action!r} is not available from {state.position!r}",
            )
        next_state = WorldState(transition.destination, state.resources)
        steps.append(ExecutionStep(action, state, next_state))
        state = next_state

    provenance = Provenance(
        subject.provenance.source_identifiers,
        subject.provenance.encoding_rule,
        subject.provenance.carrier_symbol,
        (*subject.provenance.history, "executed"),
    )
    execution = Execution(
        subject.identifier,
        subject.policy.identifier,
        source_state,
        tuple(steps),
        provenance,
    )
    return Outcome(state, execution)
