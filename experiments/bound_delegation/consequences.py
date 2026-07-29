"""Explicit spillover, blowback, and non-erasing compensation."""

from __future__ import annotations

from dataclasses import replace

from .records import (
    Compartment,
    Compensation,
    CompensationResult,
    Consequence,
    ConsequenceKind,
    ConsequenceResult,
    ExecutionResult,
    Spillover,
)
from .world import compartment_state, replace_compartment


def derive_consequences(result: ExecutionResult) -> ConsequenceResult:
    action = result.action
    if action.kind.value != "consume-shared":
        raise ValueError("only shared-resource consumption has this consequence law")
    shortage = Consequence(
        f"consequence:south-shortage:{action.identifier}",
        ConsequenceKind.SOUTH_SHORTAGE,
        Compartment.SOUTH,
        amount=1,
        causal_chain=(action.identifier, "shared-resource-pressure", "south-shortage"),
    )
    blowback = Consequence(
        f"consequence:principal-loss:{action.identifier}",
        ConsequenceKind.PRINCIPAL_RESOURCE_LOSS,
        affected_compartment=None,
        amount=1,
        causal_chain=(action.identifier, "shared-resource-pressure", "principal-loss"),
    )
    south = compartment_state(result.environment, Compartment.SOUTH)
    environment = replace_compartment(
        result.environment,
        replace(south, resource_units=south.resource_units - shortage.amount),
    )
    environment = replace(
        environment,
        principal_resource_units=environment.principal_resource_units - blowback.amount,
    )
    trace = replace(
        result.trace,
        consequences=(*result.trace.consequences, shortage, blowback),
    )
    return ConsequenceResult(
        environment,
        Spillover(action.identifier, action.direct_scopes, shortage),
        blowback,
        trace,
    )


def compensate(
    result: ConsequenceResult,
    *,
    amount: int,
    performed_step: int,
) -> CompensationResult:
    compensation = Compensation(
        f"compensation:{result.spillover.consequence.identifier}:{performed_step}",
        result.spillover.consequence.identifier,
        amount,
        performed_step,
    )
    repair = Consequence(
        f"consequence:repair:{compensation.identifier}",
        ConsequenceKind.REPAIRED_SHORTAGE,
        Compartment.SOUTH,
        amount,
        causal_chain=(
            result.spillover.action_identifier,
            result.spillover.consequence.identifier,
            compensation.identifier,
        ),
    )
    south = compartment_state(result.environment, Compartment.SOUTH)
    environment = replace_compartment(
        result.environment,
        replace(south, resource_units=south.resource_units + amount),
    )
    trace = replace(
        result.trace,
        consequences=(*result.trace.consequences, repair),
        compensations=(*result.trace.compensations, compensation),
    )
    return CompensationResult(environment, compensation, repair, trace)
