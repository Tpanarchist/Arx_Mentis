"""Run the human-readable Ars Dialectica witness."""

from .model import (
    Conforms,
    Effect,
    ElaboratedSpell,
    VerifiedDemonstration,
    elaborate,
    make_experiment,
)
from .production import cast
from .verification import check_will, verify_demonstration


def main() -> None:
    experiment = make_experiment()
    elaborated = elaborate(experiment.spell, experiment.ars)
    if not isinstance(elaborated, ElaboratedSpell):
        print("elaboration refused")
        return
    result = cast(elaborated, experiment.context)
    if not isinstance(result, Effect):
        print(f"Cast outcome: {type(result).__name__}")
        return
    verification = verify_demonstration(result, experiment.context)
    conformity = check_will(result, experiment.ars)
    if isinstance(verification, VerifiedDemonstration):
        print(f"verified applications={verification.checked_applications}")
    if isinstance(conformity, Conforms):
        print(f"separate Will check: conforms under {conformity.law.ars_name}")


if __name__ == "__main__":
    main()
