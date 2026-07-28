"""Precommitted exact trials with explicit stopping and context schedules."""

from __future__ import annotations

from .kernels import OUTCOME_SPACE, outcome_for_seed
from .outcomes import (
    CausalRecord,
    ComparisonRule,
    ContextSchedule,
    ContextState,
    EventStream,
    InvalidPlan,
    InvalidSeed,
    Kernel,
    MechanismKind,
    ObservationWindow,
    Outcome,
    ReportKind,
    ReportPolicy,
    ScheduledSeed,
    StoppingKind,
    StoppingRule,
    Trial,
    TrialPlan,
)

DEFAULT_SEEDS = tuple(range(60))
DEFAULT_WINDOW = ObservationWindow(0, 60)
DEFAULT_REPORT_POLICY = ReportPolicy("report-all", ReportKind.ALL, None)
DEFAULT_STOPPING_RULE = StoppingRule(StoppingKind.FIXED)


def make_plan(
    identifier: str,
    kernel_identifier: str,
    *,
    target: Outcome | None,
    interventions: tuple[str, ...] = (),
    trial_count: int = 60,
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    contexts: tuple[str, ...] = ("public",),
    window: ObservationWindow = DEFAULT_WINDOW,
    report_policy: ReportPolicy = DEFAULT_REPORT_POLICY,
    stopping_rule: StoppingRule = DEFAULT_STOPPING_RULE,
    comparison_rule: ComparisonRule | None = None,
) -> TrialPlan:
    return TrialPlan(
        identifier,
        recorded_order=0,
        outcome_space=OUTCOME_SPACE,
        target=target,
        kernel_identifier=kernel_identifier,
        intervention_identifiers=interventions,
        trial_count=trial_count,
        seeds=seeds,
        context_identifiers=contexts,
        observation_window=window,
        report_policy=report_policy,
        stopping_rule=stopping_rule,
        comparison_rule=comparison_rule
        or ComparisonRule("compare-declared-kernel", kernel_identifier),
    )


def execute_plan(
    plan: TrialPlan,
    kernel: Kernel,
    context: ContextState,
    *,
    mechanism: MechanismKind,
) -> EventStream | InvalidPlan:
    if plan.kernel_identifier != kernel.identifier:
        return InvalidPlan(plan, "plan and supplied kernel identifiers differ")
    if context.identifier not in plan.context_identifiers or context.kernel != kernel:
        return InvalidPlan(
            plan, "supplied context was not precommitted for this kernel"
        )
    if plan.trial_count > len(plan.seeds):
        return InvalidPlan(plan, "plan declares more trials than seeds")
    if plan.stopping_rule.kind is StoppingKind.FAVORABLE_RUN and (
        plan.target is None or not plan.stopping_rule.favorable_run_length
    ):
        return InvalidPlan(plan, "favorable stopping requires target and run length")

    trials: list[Trial] = []
    favorable_run = 0
    for index, seed in enumerate(plan.seeds[: plan.trial_count]):
        outcome = outcome_for_seed(kernel, seed)
        if isinstance(outcome, InvalidSeed):
            return InvalidPlan(plan, outcome.reason)
        trial = Trial(
            plan.recorded_order + index + 1, seed, context.identifier, outcome
        )
        trials.append(trial)
        if outcome is plan.target:
            favorable_run += 1
        else:
            favorable_run = 0
        if (
            plan.stopping_rule.kind is StoppingKind.FAVORABLE_RUN
            and favorable_run == plan.stopping_rule.favorable_run_length
        ):
            break
    record = CausalRecord(
        mechanism,
        (kernel.identifier,),
        plan.intervention_identifiers,
        (context.identifier,),
        len(trials),
    )
    return EventStream(plan, tuple(trials), record)


def balanced_half_schedule(*contexts: ContextState) -> ContextSchedule:
    entries: list[ScheduledSeed] = []
    for context in contexts:
        boundary = 0
        for weight in context.kernel.weights:
            if weight.mass % 2:
                raise ValueError("mixture witness requires even context weights")
            entries.extend(
                ScheduledSeed(context.identifier, seed)
                for seed in range(boundary, boundary + weight.mass // 2)
            )
            boundary += weight.mass
    return ContextSchedule(tuple(entries))


def execute_mixture(
    plan: TrialPlan,
    contexts: tuple[ContextState, ...],
    schedule: ContextSchedule,
) -> EventStream | InvalidPlan:
    by_identifier = {context.identifier: context for context in contexts}
    if set(plan.context_identifiers) != set(by_identifier):
        return InvalidPlan(plan, "mixture contexts differ from precommitment")
    if plan.trial_count != len(schedule.entries):
        return InvalidPlan(plan, "mixture schedule length differs from trial count")
    if plan.seeds != tuple(entry.seed for entry in schedule.entries):
        return InvalidPlan(plan, "mixture seeds differ from precommitment")

    trials: list[Trial] = []
    for index, entry in enumerate(schedule.entries):
        context = by_identifier.get(entry.context_identifier)
        if context is None:
            return InvalidPlan(plan, "schedule names an undeclared context")
        outcome = outcome_for_seed(context.kernel, entry.seed)
        if isinstance(outcome, InvalidSeed):
            return InvalidPlan(plan, outcome.reason)
        trials.append(
            Trial(
                plan.recorded_order + index + 1,
                entry.seed,
                context.identifier,
                outcome,
            )
        )
    record = CausalRecord(
        MechanismKind.CONTEXT_MIXTURE,
        tuple(context.kernel.identifier for context in contexts),
        (),
        tuple(context.identifier for context in contexts),
        len(trials),
    )
    return EventStream(plan, tuple(trials), record)
