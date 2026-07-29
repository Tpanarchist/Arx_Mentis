"""Executable witness for State Zero Experiment 013."""

from __future__ import annotations

from .authority import dependency_profile
from .execution import execute_action
from .records import ControlView, Refusal, Role
from .roles import read_as
from .scenarios import contained_session, spillover_session


def main() -> None:
    session = contained_session()
    profile = dependency_profile()
    control = read_as(session.delegate, Role.CONTROL)
    assert isinstance(control, ControlView)
    exhausted = execute_action(
        control,
        session.delegate,
        session.activation,
        session.source_plan.instructions[0],
        session.environment,
        session.trace,
        session.registry,
        step=5,
    )
    assert isinstance(exhausted, Refusal)
    consequences, repaired = spillover_session()

    print(
        "source released, bounded actions: "
        f"available={session.source_availability.available}, "
        f"actions={len(session.trace.actions)}, fourth={exhausted.kind.value}"
    )
    print(
        "dependency vector: "
        f"content={profile.source_content.value}, "
        f"authority={profile.authority.value}, resources={profile.resources.value}"
    )
    print(
        "consequence extent: "
        "direct="
        f"{sorted(item.value for item in consequences.spillover.direct_scopes)}, "
        f"spillover={consequences.spillover.consequence.affected_compartment.value}"
    )
    print(
        "compensation history: "
        f"consequences={len(repaired.trace.consequences)}, "
        f"repairs={len(repaired.trace.compensations)}"
    )
    print(
        "foundation boundary: source-content independence preserves explicit "
        "authority, scope, resource, lifecycle, provenance, and consequence bounds"
    )


if __name__ == "__main__":
    main()
