"""Run the human-readable State Zero Experiment 005 witness."""

from .composition import correlated_image, independent, product_image, shared, twisted
from .foundation_mapping import attempt_mapping
from .mediation import (
    ENDPOINT_REACHED,
    MediationRecord,
    assess,
    lift_aggregate,
    lift_signatures,
    make_interaction,
    mediate,
)
from .observation import IdentifiedPair, identify_correlated, signature_observation
from .source_model import Channel, Intervention, Permission, Situation


def main() -> None:
    situation = Situation(frozenset({Permission.MEDIATE_TRANSFER}))
    first = mediate(
        Intervention(make_interaction("first", "stress-a", "event-a", 7)),
        situation,
    )
    second = mediate(
        Intervention(make_interaction("second", "stress-b", "event-b", 7)),
        situation,
    )
    if not isinstance(first, MediationRecord) or not isinstance(
        second,
        MediationRecord,
    ):
        print("neutral mediation did not run")
        return

    shared_pair = shared(first.traces, second.traces)
    twisted_pair = twisted(first.traces, second.traces)
    product = independent(first.traces, second.traces)
    aggregate = lift_aggregate(first.traces)
    signatures = lift_signatures(first.traces)
    beta = frozenset({signature_observation("first", Channel.BETA)})
    shared_identified = identify_correlated(shared_pair, beta)
    twisted_identified = identify_correlated(twisted_pair, beta)
    assessment = assess(ENDPOINT_REACHED, first)
    mapping = attempt_mapping(first, assessment)

    print(
        "composition outcomes: "
        f"shared={len(correlated_image(shared_pair))}, "
        f"twisted={len(correlated_image(twisted_pair))}, "
        f"independent={len(product_image(product))}"
    )
    print(
        f"aggregate={aggregate.transfer.units}; "
        f"signature-family={len(signatures.assignments)}"
    )
    if isinstance(shared_identified, IdentifiedPair):
        print(
            "shared beta evidence: "
            f"{shared_identified.first.mediator.channel.value}/"
            f"{shared_identified.second.mediator.channel.value}"
        )
    if isinstance(twisted_identified, IdentifiedPair):
        print(
            "twisted beta evidence: "
            f"{twisted_identified.first.mediator.channel.value}/"
            f"{twisted_identified.second.mediator.channel.value}"
        )
    print(f"mapping pressure: {mapping.result_shape.pressure}")


if __name__ == "__main__":
    main()
