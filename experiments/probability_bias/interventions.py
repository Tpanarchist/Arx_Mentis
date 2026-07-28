"""Declared weight transformations and order-independent conflict handling."""

from __future__ import annotations

from .kernels import build_kernel, kernel_mass
from .outcomes import (
    ContextState,
    Intervention,
    InterventionConflict,
    InvalidWeights,
    Kernel,
    KernelTransformation,
    Outcome,
    UnchangedKernel,
    Weight,
    WeightChange,
)


def bias_intervention(
    target: Outcome,
    *,
    identifier: str | None = None,
    priority: int = 1,
    context_identifier: str | None = "public",
) -> Intervention:
    return Intervention(
        identifier or f"bias-{target.value}",
        target,
        delta=10,
        priority=priority,
        context_identifier=context_identifier,
    )


def apply_intervention(
    kernel: Kernel,
    intervention: Intervention,
    context: ContextState,
) -> KernelTransformation | UnchangedKernel | InvalidWeights:
    if (
        intervention.context_identifier is not None
        and intervention.context_identifier != context.identifier
    ):
        return UnchangedKernel(
            kernel,
            intervention,
            "intervention concerns another context",
        )
    if intervention.target is None:
        return UnchangedKernel(kernel, intervention, "intervention declares no target")
    alternatives = len(kernel.outcome_space.outcomes) - 1
    if intervention.delta <= 0 or intervention.delta % alternatives:
        return InvalidWeights(
            f"{kernel.identifier}+{intervention.identifier}",
            kernel.weights,
            "bias delta must divide evenly across non-target outcomes",
        )
    decrement = intervention.delta // alternatives
    supplied = tuple(
        Weight(
            outcome,
            kernel_mass(kernel, outcome)
            + (intervention.delta if outcome is intervention.target else -decrement),
        )
        for outcome in Outcome
    )
    result = build_kernel(
        f"{kernel.identifier}+{intervention.identifier}",
        supplied,
    )
    if isinstance(result, InvalidWeights):
        return result
    changes = tuple(
        WeightChange(
            outcome,
            kernel_mass(kernel, outcome),
            kernel_mass(result, outcome),
        )
        for outcome in Outcome
        if kernel_mass(kernel, outcome) != kernel_mass(result, outcome)
    )
    return KernelTransformation(kernel, result, intervention, changes)


def compose_interventions(
    kernel: Kernel,
    interventions: tuple[Intervention, ...],
    context: ContextState,
) -> KernelTransformation | UnchangedKernel | InvalidWeights | InterventionConflict:
    applicable = tuple(
        intervention
        for intervention in interventions
        if intervention.context_identifier in {None, context.identifier}
    )
    if not applicable:
        placeholder = Intervention("none-applicable", None, 0, 0, None)
        return UnchangedKernel(kernel, placeholder, "no intervention applies")
    maximum = max(item.priority for item in applicable)
    leaders = tuple(item for item in applicable if item.priority == maximum)
    if len(leaders) > 1:
        return InterventionConflict(
            kernel,
            maximum,
            frozenset(item.identifier for item in leaders),
            "equal-priority transformations have no declared composition policy",
        )
    return apply_intervention(kernel, leaders[0], context)
