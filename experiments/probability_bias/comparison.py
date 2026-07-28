"""Exact comparisons among support, weights, samples, and acceptance."""

from __future__ import annotations

from .kernels import kernel_mass, support
from .outcomes import (
    Correspondence,
    Distribution,
    DistributionComparison,
    EventStream,
    Frequency,
    Kernel,
    KernelComparison,
    Outcome,
    Sample,
    SampleAcceptance,
    SampleCriterion,
    Trial,
    WeightChange,
)


def compare_kernels(left: Kernel, right: Kernel) -> KernelComparison:
    changes = tuple(
        WeightChange(
            outcome,
            kernel_mass(left, outcome),
            kernel_mass(right, outcome),
        )
        for outcome in Outcome
        if kernel_mass(left, outcome) != kernel_mass(right, outcome)
    )
    return KernelComparison(support(left) == support(right), changes)


def distribution(stream: EventStream) -> Distribution:
    frequencies = tuple(
        Frequency(
            outcome,
            sum(trial.outcome is outcome for trial in stream.trials),
        )
        for outcome in Outcome
    )
    return Distribution(frequencies, len(stream.trials))


def compare_distributions(
    left: EventStream,
    right: EventStream,
) -> DistributionComparison:
    left_distribution = distribution(left)
    right_distribution = distribution(right)
    return DistributionComparison(
        left_distribution == right_distribution,
        left_distribution,
        right_distribution,
    )


def compare_trial(trial: Trial, target: Outcome) -> Correspondence:
    return Correspondence(trial, target, trial.outcome is target)


def assess_sample(sample: Sample, criterion: SampleCriterion) -> SampleAcceptance:
    count = sum(trial.outcome is criterion.target for trial in sample.trials)
    return SampleAcceptance(sample, criterion, count >= criterion.minimum_count)
