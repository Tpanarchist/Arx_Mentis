"""Named targets and constraints for the executable countermodels."""

from __future__ import annotations

from .source_model import Constraint, Position, Preference, TargetForm


def shortest_target() -> TargetForm:
    return TargetForm("reach-d-shortest", 0, Position.D, 5, Preference.SHORTEST)


def safe_target() -> TargetForm:
    return TargetForm("reach-d-safe", 0, Position.D, 5, Preference.SAFE)


def strict_target() -> TargetForm:
    return TargetForm("reach-d-strict", 0, Position.D, 6, Preference.SHORTEST)


def fully_blocked() -> Constraint:
    return Constraint(frozenset({"short-a-b", "safe-a-c"}))


def partially_blocked_safe_path() -> Constraint:
    return Constraint(frozenset({"safe-e-d"}))
