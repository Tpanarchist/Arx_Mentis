"""Run the human-readable State Zero Experiment 009 witness."""

from .assessment import assess_acceptance, assess_progress, assess_resolution
from .countermodels import report_scalar_loss
from .discharge import discharge, oscillate
from .foundation_mapping import attempt_mapping
from .loading import total_stress
from .network import default_network
from .scenarios import (
    B_TRIGGER,
    C_TRIGGER,
    DELIVERY_ACCEPTANCE,
    DELIVERY_PROGRESS,
    FORCE_DISSIPATION,
    OPEN,
    SAFE_RESOLUTION,
    SOURCE_ONLY,
    SOURCE_TRIGGER,
    dissipation_load,
    gradual_source_load,
    north_obstructed_distribution,
    oscillation_law,
    oscillation_load,
    south_obstructed_distribution,
)
from .source_model import Discharge


def main() -> None:
    network = default_network()
    north = discharge(
        north_obstructed_distribution(),
        network,
        SOURCE_ONLY,
        SOURCE_TRIGGER,
        maximum_steps=1,
    )
    south = discharge(
        south_obstructed_distribution(),
        network,
        SOURCE_ONLY,
        SOURCE_TRIGGER,
        maximum_steps=1,
    )
    complete = discharge(
        gradual_source_load(),
        network,
        OPEN,
        SOURCE_TRIGGER,
    )
    dissipated = discharge(
        dissipation_load(),
        network,
        FORCE_DISSIPATION,
        C_TRIGGER,
    )
    oscillation = oscillate(
        oscillation_load(),
        network,
        OPEN,
        B_TRIGGER,
        oscillation_law(),
    )
    assert isinstance(north, Discharge)
    assert isinstance(south, Discharge)
    assert isinstance(complete, Discharge)
    assert isinstance(dissipated, Discharge)
    assert isinstance(oscillation, Discharge)

    scalar_loss = report_scalar_loss(
        north.before.field,
        south.before.field,
        north.trace.steps[0].link.identifier,
        south.trace.steps[0].link.identifier,
    )
    resolution = assess_resolution(dissipated.after, SAFE_RESOLUTION)
    acceptance = assess_acceptance(dissipated.after, DELIVERY_ACCEPTANCE)
    progress = assess_progress(dissipated.after, DELIVERY_PROGRESS)
    mapping = attempt_mapping()
    print(
        "equal scalar, different paths: "
        f"total={scalar_loss.scalar.total}, "
        f"paths={north.trace.steps[0].link.identifier}/"
        f"{south.trace.steps[0].link.identifier}"
    )
    print(
        "complete release: "
        f"delivered={complete.after.delivered}, "
        f"remaining-stress={total_stress(complete.after.field)}"
    )
    print(
        "dissipation boundary: "
        f"resolved={resolution.resolved}, accepted={acceptance.accepted}, "
        f"progressed={progress.progressed}"
    )
    print(
        "oscillation residue: "
        f"steps={len(oscillation.trace.steps)}, "
        f"reversals={oscillation.residue.oscillation_reversals}"
    )
    print(f"foundation boundary: {mapping.finding.conclusion}")


if __name__ == "__main__":
    main()
