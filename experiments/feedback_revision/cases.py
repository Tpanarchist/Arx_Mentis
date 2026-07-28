"""The fixed twelve-case world and its information boundaries."""

from __future__ import annotations

from .records import CaseInput, Holdout, Outcome, WorldCase

CASES = (
    WorldCase("C00", False, False, Outcome.NEGATIVE),
    WorldCase("C01", False, True, Outcome.POSITIVE),
    WorldCase("C02", True, False, Outcome.POSITIVE),
    WorldCase("C03", True, True, Outcome.NEGATIVE),
    WorldCase("C04", False, False, Outcome.NEGATIVE),
    WorldCase("C05", True, True, Outcome.NEGATIVE),
    WorldCase("C06", False, False, Outcome.NEGATIVE),
    WorldCase("C07", True, False, Outcome.POSITIVE),
    WorldCase("C08", False, False, Outcome.NEGATIVE),
    WorldCase("C09", True, False, Outcome.POSITIVE),
    WorldCase("C10", False, True, Outcome.POSITIVE),
    WorldCase("C11", True, True, Outcome.NEGATIVE),
)

CALIBRATION_CASES = CASES[:6]
HOLDOUT_CASES = CASES[6:]
CALIBRATION_IDS = frozenset(case.identifier for case in CALIBRATION_CASES)
HOLDOUT_IDS = frozenset(case.identifier for case in HOLDOUT_CASES)
SEALED_HOLDOUT = Holdout("holdout-C06-C11", HOLDOUT_IDS, sealed=True)


def case_inputs(cases: tuple[WorldCase, ...]) -> tuple[CaseInput, ...]:
    return tuple(
        CaseInput(case.identifier, case.feature_x, case.feature_y) for case in cases
    )


def case_by_identifier(identifier: str) -> WorldCase:
    return next(case for case in CASES if case.identifier == identifier)
