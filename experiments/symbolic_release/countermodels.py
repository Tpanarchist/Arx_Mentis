"""Hostile comparisons for identity, completeness, and provenance claims."""

from __future__ import annotations

from .source import (
    AcceptanceRule,
    ArtifactComparison,
    CompiledPolicy,
    IncompleteReconstruction,
    Interpretation,
    Outcome,
    OutcomeComparison,
    SourceReconstruction,
)


def attempt_exact_reconstruction(
    interpretation: Interpretation,
) -> SourceReconstruction | IncompleteReconstruction:
    if isinstance(interpretation.artifact, SourceReconstruction):
        return interpretation.artifact
    preserved = tuple(field.name for field in interpretation.carrier.fields)
    required = {
        "source",
        "destination",
        "minimum-resources",
        "explanation",
    }
    missing = tuple(sorted(required.difference(preserved)))
    return IncompleteReconstruction(interpretation.carrier, preserved, missing)


def _local_value(
    artifact: SourceReconstruction | CompiledPolicy | AcceptanceRule,
) -> tuple[object, ...]:
    if isinstance(artifact, SourceReconstruction):
        return (
            artifact.source.guidance,
            artifact.source.destination,
            artifact.source.minimum_resources,
            artifact.source.explanation,
        )
    if isinstance(artifact, CompiledPolicy):
        return artifact.actions
    return (artifact.destination, artifact.minimum_resources)


def compare_artifacts(
    left: SourceReconstruction | CompiledPolicy | AcceptanceRule,
    right: SourceReconstruction | CompiledPolicy | AcceptanceRule,
) -> ArtifactComparison:
    left_sources = set(left.provenance.source_identifiers)
    right_sources = set(right.provenance.source_identifiers)
    return ArtifactComparison(
        same_local_value=_local_value(left) == _local_value(right),
        shared_source=bool(left_sources.intersection(right_sources)),
        same_provenance=left.provenance == right.provenance,
    )


def compare_outcomes(left: Outcome, right: Outcome) -> OutcomeComparison:
    return OutcomeComparison(
        same_state=left.state == right.state,
        same_policy=(
            tuple(step.action for step in left.execution.steps)
            == tuple(step.action for step in right.execution.steps)
        ),
        same_decoding=(
            left.execution.provenance.source_identifiers
            == right.execution.provenance.source_identifiers
            and left.execution.provenance.encoding_rule
            == right.execution.provenance.encoding_rule
        ),
    )
