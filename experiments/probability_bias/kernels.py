"""Exact normalized kernels over a declared sixty-seed space."""

from __future__ import annotations

from .outcomes import (
    InvalidSeed,
    InvalidWeights,
    Kernel,
    Outcome,
    OutcomeSpace,
    Weight,
)

SEED_SPACE = range(60)
OUTCOME_SPACE = OutcomeSpace(frozenset(Outcome))
OUTCOME_ORDER = tuple(Outcome)


def build_kernel(
    identifier: str,
    supplied: tuple[Weight, ...],
) -> Kernel | InvalidWeights:
    outcomes = tuple(item.outcome for item in supplied)
    if len(set(outcomes)) != len(outcomes):
        return InvalidWeights(identifier, supplied, "duplicate outcome weight")
    if set(outcomes) != set(OUTCOME_SPACE.outcomes):
        return InvalidWeights(
            identifier, supplied, "weights must cover the outcome space"
        )
    if any(item.mass < 0 for item in supplied):
        return InvalidWeights(identifier, supplied, "weights must be nonnegative")
    if sum(item.mass for item in supplied) != len(SEED_SPACE):
        return InvalidWeights(identifier, supplied, "weights must normalize to sixty")
    by_outcome = {item.outcome: item.mass for item in supplied}
    weights = tuple(Weight(outcome, by_outcome[outcome]) for outcome in OUTCOME_ORDER)
    return Kernel(identifier, OUTCOME_SPACE, weights, len(SEED_SPACE))


def baseline_kernel() -> Kernel:
    result = build_kernel(
        "baseline-six-way",
        tuple(Weight(outcome, 10) for outcome in OUTCOME_ORDER),
    )
    assert isinstance(result, Kernel)
    return result


def kernel_mass(kernel: Kernel, outcome: Outcome) -> int:
    return next(item.mass for item in kernel.weights if item.outcome is outcome)


def support(kernel: Kernel) -> frozenset[Outcome]:
    return frozenset(item.outcome for item in kernel.weights if item.mass > 0)


def outcome_for_seed(kernel: Kernel, seed: int) -> Outcome | InvalidSeed:
    if seed not in SEED_SPACE:
        return InvalidSeed(
            seed, SEED_SPACE, "seed lies outside the declared seed space"
        )
    boundary = 0
    for weight in kernel.weights:
        boundary += weight.mass
        if seed < boundary:
            return weight.outcome
    raise AssertionError("normalized kernel did not cover its seed space")


def context_kernel_x() -> Kernel:
    result = build_kernel(
        "context-x",
        tuple(
            Weight(outcome, mass)
            for outcome, mass in zip(
                OUTCOME_ORDER,
                (24, 12, 8, 8, 4, 4),
                strict=True,
            )
        ),
    )
    assert isinstance(result, Kernel)
    return result


def context_kernel_y() -> Kernel:
    result = build_kernel(
        "context-y",
        tuple(
            Weight(outcome, mass)
            for outcome, mass in zip(
                OUTCOME_ORDER,
                (16, 4, 8, 8, 12, 12),
                strict=True,
            )
        ),
    )
    assert isinstance(result, Kernel)
    return result
