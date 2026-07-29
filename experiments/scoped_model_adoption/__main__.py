"""Executable witness for State Zero Experiment 012."""

from __future__ import annotations

from .adoption import adopt, reconcile_adoptions
from .models import model_x, model_y
from .records import AdoptionConflict, RevocationPolicy, Scope, UseMode
from .scenarios import execute_scoped_composite, standard_assessments


def main() -> None:
    assessment_x, assessment_y = standard_assessments()
    _, outcomes = execute_scoped_composite()
    overlap_x = adopt(
        "overlap-x",
        model_x(),
        purpose="trial",
        use_mode=UseMode.CONTROL,
        scopes=frozenset({Scope.AMBER}),
        authority=5,
        revocation_policy=RevocationPolicy.LIVE_LINKED,
    )
    overlap_y = adopt(
        "overlap-y",
        model_y(),
        purpose="trial",
        use_mode=UseMode.CONTROL,
        scopes=frozenset({Scope.AMBER}),
        authority=5,
        revocation_policy=RevocationPolicy.LIVE_LINKED,
    )
    conflict = reconcile_adoptions((overlap_x, overlap_y))
    assert isinstance(conflict, AdoptionConflict)

    print(
        "global assessments: "
        f"X={assessment_x.global_accepted_count}/12, "
        f"Y={assessment_y.global_accepted_count}/12"
    )
    print(
        f"scoped composite: successful={sum(item.successful for item in outcomes)}/12"
    )
    print(
        f"overlapping equal authority: conflict={sorted(conflict.adoption_identifiers)}"
    )
    print(
        "foundation boundary: adopting a model for scoped use authorizes operation; "
        "it does not assert world truth"
    )


if __name__ == "__main__":
    main()
