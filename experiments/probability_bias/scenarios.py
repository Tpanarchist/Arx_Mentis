"""Named exact kernels, interventions, contexts, and trial plans."""

from __future__ import annotations

from .interventions import apply_intervention, bias_intervention
from .kernels import baseline_kernel, context_kernel_x, context_kernel_y
from .outcomes import (
    ContextState,
    Kernel,
    KernelTransformation,
    ObservationWindow,
    Outcome,
    ReportKind,
    ReportPolicy,
    StoppingKind,
    StoppingRule,
)
from .trials import balanced_half_schedule, make_plan

PUBLIC_CONTEXT_ID = "public"


def public_baseline() -> tuple[Kernel, ContextState]:
    kernel = baseline_kernel()
    return kernel, ContextState(PUBLIC_CONTEXT_ID, kernel, True)


def public_bias(
    target: Outcome = Outcome.A,
) -> tuple[KernelTransformation, ContextState]:
    baseline, context = public_baseline()
    intervention = bias_intervention(target)
    result = apply_intervention(baseline, intervention, context)
    assert isinstance(result, KernelTransformation)
    return result, ContextState(PUBLIC_CONTEXT_ID, result.after, True)


def baseline_plan(*, window: ObservationWindow | None = None):
    kernel, _ = public_baseline()
    return make_plan(
        "baseline-plan",
        kernel.identifier,
        target=Outcome.A,
        window=window or ObservationWindow(0, 60),
    )


def biased_plan():
    transformation, _ = public_bias()
    return make_plan(
        "biased-plan",
        transformation.after.identifier,
        target=Outcome.A,
        interventions=(transformation.intervention.identifier,),
    )


def selective_plan():
    kernel, _ = public_baseline()
    return make_plan(
        "selective-plan",
        kernel.identifier,
        target=Outcome.A,
        report_policy=ReportPolicy(
            "report-target-only",
            ReportKind.MATCH_TARGET,
            Outcome.A,
        ),
    )


def optional_stopping_plan():
    kernel, _ = public_baseline()
    return make_plan(
        "optional-stopping-plan",
        kernel.identifier,
        target=Outcome.A,
        stopping_rule=StoppingRule(StoppingKind.FAVORABLE_RUN, 2),
    )


def mixture_scenario():
    x_kernel = context_kernel_x()
    y_kernel = context_kernel_y()
    x = ContextState("context-x", x_kernel, False)
    y = ContextState("context-y", y_kernel, False)
    schedule = balanced_half_schedule(x, y)
    plan = make_plan(
        "hidden-mixture-plan",
        "mixture:context-x+context-y",
        target=Outcome.A,
        trial_count=len(schedule.entries),
        seeds=tuple(entry.seed for entry in schedule.entries),
        contexts=(x.identifier, y.identifier),
    )
    return plan, (x, y), schedule
