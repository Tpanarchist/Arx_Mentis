"""Run the human-readable Ars Grammatica witness."""

from .model import Effect, Equivalent, Inspection, check, make_experiment, read


def main() -> None:
    experiment = make_experiment()
    inspection = read(experiment.form, experiment.examining_context)
    execution = read(experiment.form, experiment.executing_context)
    if isinstance(inspection, Inspection):
        source_preserved = inspection.source is experiment.form
        print(f"examining Reader: source preserved={source_preserved}")
    if isinstance(execution, Effect):
        print(
            "executing Reader: "
            f"{execution.trace.source.subject.text} -> {execution.form.subject.text}; "
            f"predicate={execution.form.predicate.text}"
        )
        comparison = check(execution, experiment.executing_context)
        if isinstance(comparison, Equivalent):
            print(f"separate check: equivalent under {comparison.ars_name}")


if __name__ == "__main__":
    main()
