"""Run the human-readable State Zero Experiment 010 witness."""

from .comparison import compare_distributions, compare_kernels, distribution
from .interventions import bias_intervention, compose_interventions
from .kernels import kernel_mass
from .observation import hide_context, observe
from .outcomes import (
    EventStream,
    InterventionConflict,
    MechanismKind,
    Outcome,
)
from .scenarios import (
    baseline_plan,
    biased_plan,
    mixture_scenario,
    public_baseline,
    public_bias,
)
from .trials import execute_mixture, execute_plan


def main() -> None:
    baseline, baseline_context = public_baseline()
    transformation, biased_context = public_bias()
    biased = transformation.after
    baseline_stream = execute_plan(
        baseline_plan(),
        baseline,
        baseline_context,
        mechanism=MechanismKind.BASELINE,
    )
    biased_stream = execute_plan(
        biased_plan(),
        biased,
        biased_context,
        mechanism=MechanismKind.INTERVENED,
    )
    mixture_plan, contexts, schedule = mixture_scenario()
    mixture_stream = execute_mixture(mixture_plan, contexts, schedule)
    assert isinstance(baseline_stream, EventStream)
    assert isinstance(biased_stream, EventStream)
    assert isinstance(mixture_stream, EventStream)

    intervention_a = bias_intervention(
        Outcome.A,
        identifier="equal-priority-a",
        priority=5,
    )
    intervention_b = bias_intervention(
        Outcome.B,
        identifier="equal-priority-b",
        priority=5,
    )
    conflict = compose_interventions(
        baseline,
        (intervention_a, intervention_b),
        baseline_context,
    )
    assert isinstance(conflict, InterventionConflict)
    kernel_comparison = compare_kernels(baseline, biased)
    public_comparison = compare_distributions(biased_stream, mixture_stream)
    hidden_observation = hide_context(observe(mixture_stream))
    print(
        "target mass: "
        f"baseline={kernel_mass(baseline, Outcome.A)}/60, "
        f"biased={kernel_mass(biased, Outcome.A)}/60"
    )
    print(
        "same support, changed weights: "
        f"support={kernel_comparison.same_support}, "
        f"changes={len(kernel_comparison.weight_changes)}"
    )
    print(
        "fixed bias versus hidden mixture: "
        f"public-equal={public_comparison.same_public_distribution}, "
        "contexts-visible="
        f"{all(t.context_available for t in hidden_observation.trials)}"
    )
    print(
        "equal-priority interventions: "
        f"conflict={sorted(conflict.intervention_identifiers)}"
    )
    print(
        "biased exact frequency: "
        f"A={distribution(biased_stream).frequencies[0].count}/60"
    )


if __name__ == "__main__":
    main()
