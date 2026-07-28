"""Release source availability only after a lawful derivation boundary."""

from __future__ import annotations

from .activation import activate
from .encoding import encode_compiled
from .source import (
    Activation,
    AvailableSources,
    Encoding,
    Interpretation,
    MissingDependency,
    PendingCarrier,
    Provenance,
    RejectedActivation,
    ReleasedBundle,
    RetainedBundle,
    SourceForm,
)


def retain(
    source: SourceForm,
    encoding: Encoding,
    interpretation: Interpretation,
) -> RetainedBundle:
    return RetainedBundle(source, encoding.carrier, interpretation)


def release_after_interpretation(
    encoding: Encoding,
    interpretation: Interpretation,
) -> ReleasedBundle:
    artifact_provenance = interpretation.artifact.provenance
    provenance = Provenance(
        artifact_provenance.source_identifiers,
        artifact_provenance.encoding_rule,
        artifact_provenance.carrier_symbol,
        (*artifact_provenance.history, "source-released"),
    )
    return ReleasedBundle(
        encoding.carrier,
        interpretation,
        source_available=False,
        provenance=provenance,
    )


def activate_released(
    bundle: ReleasedBundle,
) -> Activation | RejectedActivation:
    result = activate(bundle.interpretation)
    if isinstance(result, RejectedActivation):
        return result
    provenance = Provenance(
        bundle.provenance.source_identifiers,
        bundle.provenance.encoding_rule,
        bundle.provenance.carrier_symbol,
        (*bundle.provenance.history, "activated"),
    )
    return Activation(result.identifier, result.policy, provenance)


def complete_pending(
    pending: PendingCarrier,
    available: AvailableSources,
) -> Encoding | MissingDependency:
    source = next(
        (
            candidate
            for candidate in available.sources
            if candidate.identifier == pending.source_identifier
        ),
        None,
    )
    if source is None:
        return MissingDependency(
            pending,
            pending.source_identifier,
            "source was released before the carrier acquired executable content",
        )
    return encode_compiled(source)
