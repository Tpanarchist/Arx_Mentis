"""Exact contained and consequence scenarios."""

from __future__ import annotations

from .authority import contained_authority, pressure_authority
from .consequences import compensate, derive_consequences
from .derivation import derive_delegate, release_source
from .execution import EMPTY_TRACE, activate_delegate, execute_action
from .plans import pressure_plan, rebalance_plan
from .principals import standard_principal
from .records import (
    Activation,
    CompensationResult,
    ConsequenceResult,
    ContainedSession,
    ControlView,
    Derivation,
    ExecutionResult,
    RevocationMode,
    Role,
)
from .roles import read_as
from .world import initial_environment


def contained_session(
    *,
    revocation_mode: RevocationMode = RevocationMode.LIVE_LINKED,
) -> ContainedSession:
    principal = standard_principal()
    plan = rebalance_plan(principal.identifier)
    derivation = derive_delegate(
        plan,
        principal,
        contained_authority(revocation_mode=revocation_mode),
    )
    assert isinstance(derivation, Derivation)
    snapshot = plan
    availability = release_source(plan, changed_step=2)
    activation = activate_delegate(derivation.delegate, derivation.registry, step=2)
    assert isinstance(activation, Activation)
    control = read_as(derivation.delegate, role=Role.CONTROL)
    assert isinstance(control, ControlView)
    environment = initial_environment()
    trace = EMPTY_TRACE
    for step, spec in zip((2, 3, 4), plan.instructions, strict=True):
        result = execute_action(
            control,
            derivation.delegate,
            activation,
            spec,
            environment,
            trace,
            derivation.registry,
            step=step,
        )
        assert isinstance(result, ExecutionResult)
        environment = result.environment
        trace = result.trace
    assert plan == snapshot
    return ContainedSession(
        plan,
        derivation.delegate,
        derivation.registry,
        availability,
        activation,
        environment,
        trace,
    )


def spillover_session() -> tuple[ConsequenceResult, CompensationResult]:
    principal = standard_principal()
    plan = pressure_plan(principal.identifier)
    derivation = derive_delegate(
        plan,
        principal,
        pressure_authority(),
        identifier="delegate:pressure",
    )
    assert isinstance(derivation, Derivation)
    activation = activate_delegate(derivation.delegate, derivation.registry, step=2)
    assert isinstance(activation, Activation)
    control = read_as(derivation.delegate, role=Role.CONTROL)
    assert isinstance(control, ControlView)
    executed = execute_action(
        control,
        derivation.delegate,
        activation,
        plan.instructions[0],
        initial_environment(),
        EMPTY_TRACE,
        derivation.registry,
        step=2,
    )
    assert isinstance(executed, ExecutionResult)
    consequences = derive_consequences(executed)
    repaired = compensate(consequences, amount=1, performed_step=5)
    return consequences, repaired
