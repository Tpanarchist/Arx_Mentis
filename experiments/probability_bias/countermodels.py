"""Hostile reductions of weighted production, observation, and causation."""

from __future__ import annotations

from .kernels import support
from .outcomes import (
    CausalRecord,
    CountermodelRejection,
    DirectCommand,
    EventStream,
    Kernel,
    MechanismKind,
    OptionBag,
    OptionBagLoss,
    Outcome,
    ProbabilityBoundary,
    Report,
    Sample,
)


def command(target: Outcome) -> DirectCommand:
    return DirectCommand(
        target,
        frozenset({target}),
        CausalRecord(
            MechanismKind.DIRECT_COMMAND,
            (),
            (),
            (),
            seed_count=0,
        ),
    )


def reject_command_as_bias(target: Outcome) -> CountermodelRejection:
    result = command(target)
    return CountermodelRejection(
        "target-coded-command",
        f"command installs support {result.installed_support!r} instead of reweighting",
    )


def option_bag(kernel: Kernel) -> OptionBag:
    return OptionBag(support(kernel))


def report_option_bag_loss(baseline: Kernel, biased: Kernel) -> OptionBagLoss:
    baseline_bag = option_bag(baseline)
    biased_bag = option_bag(biased)
    return OptionBagLoss(
        baseline_bag,
        biased_bag,
        kernels_differ=baseline.weights != biased.weights,
        behavior_lost=baseline_bag == biased_bag and baseline.weights != biased.weights,
    )


def reject_sample_as_kernel(sample: Sample) -> CountermodelRejection:
    return CountermodelRejection(
        "sample-is-kernel",
        f"{len(sample.trials)} observed trials do not rewrite the declared kernel",
    )


def reject_match_as_bias() -> CountermodelRejection:
    return CountermodelRejection(
        "match-implies-bias",
        "one correspondence is compatible with baseline and intervened production",
    )


def reject_report_as_stream(report: Report) -> CountermodelRejection:
    return CountermodelRejection(
        "report-is-stream",
        (
            f"report shows {len(report.trials)} of "
            f"{len(report.source_stream.trials)} events"
        ),
    )


def reject_post_hoc_intention() -> CountermodelRejection:
    return CountermodelRejection(
        "post-hoc-target",
        "a target selected after the stream is not a prior causal input",
    )


def reject_hidden_optional_stopping() -> CountermodelRejection:
    return CountermodelRejection(
        "hidden-optional-stopping",
        "collection stopping must be committed in TrialPlan before execution",
    )


def reject_hidden_mixture_as_one_cause(stream: EventStream) -> CountermodelRejection:
    return CountermodelRejection(
        "hidden-mixture-as-one-kernel",
        f"world record retains contexts {stream.causal_record.context_identifiers!r}",
    )


def reject_seed_only_causation() -> CountermodelRejection:
    return CountermodelRejection(
        "seed-only-causation",
        "a seed selects within a kernel but does not explain kernel or intervention",
    )


def reject_order_based_resolution() -> CountermodelRejection:
    return CountermodelRejection(
        "order-based-intervention-resolution",
        "storage or declaration order is not a declared intervention policy",
    )


def reject_probability_as_potential(kernel: Kernel) -> ProbabilityBoundary:
    masses = {weight.mass for weight in kernel.weights}
    return ProbabilityBoundary(
        weighted=True,
        unequal_mass=len(masses) > 1,
        transitive_frame_declared=False,
        settlement_operation_declared=False,
        conclusion=(
            "a weighted production rule is neither an unresolved frame nor a "
            "settlement process"
        ),
    )
