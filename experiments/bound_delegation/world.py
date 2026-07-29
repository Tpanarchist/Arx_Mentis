"""Exact three-compartment environment."""

from __future__ import annotations

from dataclasses import replace

from .records import Compartment, CompartmentState, Environment


def initial_environment() -> Environment:
    return Environment(
        tuple(
            CompartmentState(
                compartment,
                (f"{compartment.value}:inventory",),
                (f"{compartment.value}:operations",),
                (f"{compartment.value}:protected",),
                resource_units=resources,
                external_connections=(f"{compartment.value}:external",),
            )
            for compartment, resources in (
                (Compartment.NORTH, 6),
                (Compartment.CENTER, 2),
                (Compartment.SOUTH, 3),
            )
        ),
        shared_resource_units=4,
        principal_resource_units=3,
    )


def compartment_state(
    environment: Environment,
    compartment: Compartment,
) -> CompartmentState:
    return next(
        item for item in environment.compartments if item.compartment is compartment
    )


def replace_compartment(
    environment: Environment,
    replacement: CompartmentState,
) -> Environment:
    return replace(
        environment,
        compartments=tuple(
            replacement if item.compartment is replacement.compartment else item
            for item in environment.compartments
        ),
    )
