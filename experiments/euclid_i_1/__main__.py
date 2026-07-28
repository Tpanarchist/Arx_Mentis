"""Run the equivariant Euclid I.1 evidence witness."""

from .model import (
    Conforms,
    Effect,
    ElaborationRefusal,
    FrameDependentCheck,
    Parity,
    Potential,
    Produced,
    cast,
    check,
    elaborate,
    image,
    make_experiment,
)


def main() -> None:
    experiment = make_experiment()
    first = elaborate(experiment.spell, experiment.initial_ars)
    if isinstance(first, ElaborationRefusal):
        print(
            "initial elaboration: Refused at "
            f"{first.missing_operation.value}; prefix={len(first.elaborated_prefix)}"
        )
    second = elaborate(experiment.spell, experiment.extended_ars)
    if isinstance(second, ElaborationRefusal):
        return
    result = cast(second, experiment.context)
    if not isinstance(result, Produced) or not isinstance(result.effect, Effect):
        return
    if not isinstance(result.effect.form, Potential):
        return
    print(f"extended Cast: Potential image={len(image(result.effect.form))}")
    conformity = check(experiment.spell.will, result.effect, experiment.context)
    if isinstance(conformity, Conforms):
        print("equilateral Will: Conforms without settlement")
    side_will = experiment.spell.will.__class__(
        "apex on positive side",
        experiment.extended_ars.will_fragment.predicates
        and next(
            predicate
            for predicate in experiment.extended_ars.will_fragment.predicates
            if predicate.value == "apex-positive"
        ),
        experiment.givens.base,
    )
    side_result = check(side_will, result.effect, experiment.context)
    if isinstance(side_result, FrameDependentCheck):
        print(
            "side-dependent Will: frame-dependent truth image="
            f"{len(image(side_result.family))}"
        )
    print(f"frame remains unsettled: {Parity.IDENTITY.value}/{Parity.FLIPPED.value}")


if __name__ == "__main__":
    main()
