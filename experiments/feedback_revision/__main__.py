"""Executable witness for State Zero Experiment 011."""

from __future__ import annotations

from .cases import CALIBRATION_CASES, HOLDOUT_CASES
from .models import initial_model_a, initial_version
from .records import Revision, RevisionKind, Split
from .revision import revise, revision_rule
from .scenarios import assess_bundle, calibration_evidence, run_cases


def main() -> None:
    version_zero = initial_version(initial_model_a(), "V0")
    calibration, initial_assessment, evidence = calibration_evidence(version_zero)
    holdout = run_cases("V0-holdout", version_zero, HOLDOUT_CASES, Split.HOLDOUT)
    initial_holdout = assess_bundle("assessment:V0-holdout", holdout)

    general = revise(
        version_zero,
        evidence,
        revision_rule("generalize-xor", RevisionKind.GENERALIZE_XOR),
    )
    overfit = revise(
        version_zero,
        evidence,
        revision_rule("memorize-calibration", RevisionKind.OVERFIT_MEMORIZE),
    )
    assert isinstance(general, Revision)
    assert isinstance(overfit, Revision)

    general_calibration = assess_bundle(
        "assessment:general-calibration",
        run_cases(
            "general-calibration",
            general.result_version,
            CALIBRATION_CASES,
            Split.CALIBRATION,
        ),
    )
    general_holdout = assess_bundle(
        "assessment:general-holdout",
        run_cases(
            "general-holdout",
            general.result_version,
            HOLDOUT_CASES,
            Split.HOLDOUT,
        ),
    )
    overfit_calibration = assess_bundle(
        "assessment:overfit-calibration",
        run_cases(
            "overfit-calibration",
            overfit.result_version,
            CALIBRATION_CASES,
            Split.CALIBRATION,
        ),
    )
    overfit_holdout = assess_bundle(
        "assessment:overfit-holdout",
        run_cases(
            "overfit-holdout",
            overfit.result_version,
            HOLDOUT_CASES,
            Split.HOLDOUT,
        ),
    )

    print(
        "V0 scores: "
        f"calibration={initial_assessment.accepted_count}/6, "
        f"holdout={initial_holdout.accepted_count}/6"
    )
    print(
        "generalizing revision: "
        f"calibration={general_calibration.accepted_count}/6, "
        f"holdout={general_holdout.accepted_count}/6"
    )
    print(
        "overfit revision: "
        f"calibration={overfit_calibration.accepted_count}/6, "
        f"holdout={overfit_holdout.accepted_count}/6"
    )
    print(
        "history preserved: "
        f"V0-predictions={len(calibration.predictions)}, "
        f"V1-lineage={general.result_version.lineage is not None}"
    )
    print(
        "foundation boundary: feedback constructs prospective versions; it does not "
        "rewrite committed predictions, observations, assessments, or rules"
    )


if __name__ == "__main__":
    main()
