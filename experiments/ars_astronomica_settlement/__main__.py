"""Run the Ars Astronomica equivariant settlement witness."""

from .model import (
    Point,
    Potential,
    ProjectionEffect,
    cast,
    elaborate,
    image,
    make_experiment,
    project,
    settle,
    with_observations,
)


def main() -> None:
    experiment = make_experiment()
    discrimination = elaborate(experiment.discrimination.spell, experiment.context.ars)
    projection = elaborate(experiment.projection.spell, experiment.context.ars)
    potential = cast(experiment.discrimination, discrimination, experiment.context)
    if not isinstance(potential, Potential):
        return
    future = project(experiment.projection, projection, potential, experiment.context)
    if isinstance(future, Potential):
        print(f"unsettled projection image={len(image(future))}")
    for observation in (experiment.bright, experiment.dark):
        selected = settle(
            potential,
            with_observations(experiment.context, observation),
        )
        if isinstance(selected, Point):
            result = project(
                experiment.projection,
                projection,
                selected,
                experiment.context,
            )
            if isinstance(result, ProjectionEffect):
                print(
                    f"observed {observation.state.name}: "
                    f"projected {result.prediction.state.name}"
                )


if __name__ == "__main__":
    main()
