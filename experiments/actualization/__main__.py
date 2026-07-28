"""Run the human-readable State Zero Experiment 007 witness."""

from .acceptance import derive_acceptance, evaluate
from .control import (
    compile_controller,
    derive_hidden_weighting,
    run_controller,
    run_criterion_only,
    run_hidden_bias,
)
from .foundation_mapping import attempt_mapping
from .scenarios import safe_target, shortest_target
from .source_model import Outcome
from .world import initial_world


def _path(outcome: Outcome) -> str:
    return " -> ".join(step.transition.identifier for step in outcome.trace.steps)


def main() -> None:
    source = initial_world()
    shortest = shortest_target()
    safe = safe_target()
    criterion = run_criterion_only(source, shortest)
    guided_shortest = run_controller(
        source,
        compile_controller(shortest, sustained=True),
    )
    guided_safe = run_controller(source, compile_controller(safe, sustained=True))
    hidden = run_hidden_bias(source, derive_hidden_weighting(shortest))
    if not all(
        isinstance(item, Outcome)
        for item in (criterion, guided_shortest, guided_safe, hidden)
    ):
        print("a nominal scenario unexpectedly became unreachable")
        return
    assert isinstance(criterion, Outcome)
    assert isinstance(guided_shortest, Outcome)
    assert isinstance(guided_safe, Outcome)
    assert isinstance(hidden, Outcome)
    rule = derive_acceptance(shortest)
    mapping = attempt_mapping()
    print(f"criterion-only path: {_path(criterion)}")
    print(f"shortest guidance: {_path(guided_shortest)}")
    print(f"safe guidance: {_path(guided_safe)}")
    print(
        "same accepted state by three mechanisms: "
        f"{criterion.state == guided_shortest.state == hidden.state}, "
        f"accepted={evaluate(rule, criterion.state).conforms}"
    )
    print(f"foundation boundary: {mapping.finding.conclusion}")


if __name__ == "__main__":
    main()
