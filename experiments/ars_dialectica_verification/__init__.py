"""Disposable Ars Dialectica production-and-verification experiment."""

from .model import (
    Conforms,
    Counterexample,
    Effect,
    Failed,
    InvalidDemonstration,
    Open,
    Refused,
    VerifiedDemonstration,
    elaborate,
    make_experiment,
)
from .production import cast
from .verification import check_will, decide, verify_demonstration

__all__ = [
    "Conforms",
    "Counterexample",
    "Effect",
    "Failed",
    "InvalidDemonstration",
    "Open",
    "Refused",
    "VerifiedDemonstration",
    "cast",
    "check_will",
    "decide",
    "elaborate",
    "make_experiment",
    "verify_demonstration",
]
