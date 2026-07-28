from __future__ import annotations

import ast
import subprocess
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import experiments.symbolic_release.source as source_module
from experiments.symbolic_release.activation import activate, execute
from experiments.symbolic_release.countermodels import (
    attempt_exact_reconstruction,
    compare_artifacts,
    compare_outcomes,
)
from experiments.symbolic_release.encoding import (
    encode_compiled,
    encode_keyed,
    encode_lossily,
    encode_opaquely,
    encode_transparently,
    forge_like,
    registry_from,
    stage_compilation,
)
from experiments.symbolic_release.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.symbolic_release.interpretation import (
    AUDIT_DECODER,
    AUDIT_KEY,
    EXACT_DECODER,
    EXACT_KEY,
    NAVIGATION_DECODER,
    NAVIGATION_KEY,
    assess_carrier,
    interpret,
)
from experiments.symbolic_release.release import (
    activate_released,
    complete_pending,
    release_after_interpretation,
    retain,
)
from experiments.symbolic_release.scenarios import (
    fast_source,
    initial_world,
    navigation_source,
)
from experiments.symbolic_release.source import (
    AcceptanceRule,
    Activation,
    AvailableSources,
    CompiledPolicy,
    DerivationRecord,
    DerivationRegistry,
    Encoding,
    EncodingCollision,
    ExecutionRefused,
    IncompleteReconstruction,
    Interpretation,
    MissingDependency,
    Outcome,
    RejectedActivation,
    RejectedInterpretation,
    RejectionStage,
    SourceReconstruction,
    UnsupportedInterpretation,
)


def require_interpretation(result: object) -> Interpretation:
    assert isinstance(result, Interpretation)
    return result


def policy_reading(encoding: Encoding) -> Interpretation:
    return require_interpretation(
        interpret(
            encoding.carrier,
            NAVIGATION_DECODER,
            NAVIGATION_KEY,
            registry_from(encoding),
        )
    )


def require_activation(result: object) -> Activation:
    assert isinstance(result, Activation)
    return result


def require_outcome(result: object) -> Outcome:
    assert isinstance(result, Outcome)
    return result


def test_01_source_encodes_to_a_separate_carrier() -> None:
    source = navigation_source()

    encoding = encode_transparently(source)

    assert encoding.source is source
    assert encoding.carrier is not source
    assert encoding.carrier.symbol == f"T:{source.identifier}"
    assert encoding.derivation.carrier is encoding.carrier


def test_02_encoding_preserves_the_immutable_source() -> None:
    source = navigation_source()
    snapshot = navigation_source()

    encode_compiled(source)

    assert source == snapshot
    with pytest.raises(FrozenInstanceError):
        source.explanation = "changed"  # type: ignore[misc]


def test_03_carrier_does_not_act_merely_by_existing() -> None:
    source = navigation_source()
    encoding = encode_compiled(source)
    world = initial_world()

    result = activate(encoding.carrier)

    assert isinstance(result, RejectedActivation)
    assert result.stage is RejectionStage.ACTIVATION
    assert world == initial_world()


def test_04_interpretation_is_distinct_from_activation() -> None:
    interpretation = policy_reading(encode_compiled(navigation_source()))

    activation = activate(interpretation)

    assert isinstance(interpretation.artifact, CompiledPolicy)
    assert isinstance(activation, Activation)
    assert activation.policy is interpretation.artifact
    assert activation is not interpretation


def test_05_activation_is_distinct_from_execution() -> None:
    source_state = initial_world()
    activation = require_activation(
        activate(policy_reading(encode_compiled(navigation_source())))
    )

    assert source_state == initial_world()
    outcome = require_outcome(execute(activation, source_state))

    assert outcome.state.position == "D"
    assert outcome.state is not source_state
    assert outcome.execution.activation_identifier == activation.identifier


def test_06_compiled_policy_operates_after_source_release() -> None:
    source = navigation_source()
    encoding = encode_compiled(source)
    interpretation = policy_reading(encoding)
    released = release_after_interpretation(encoding, interpretation)

    activation = require_activation(activate_released(released))
    outcome = require_outcome(execute(activation, initial_world()))

    assert not released.source_available
    assert not hasattr(released, "source")
    assert outcome.state.position == source.destination


def test_07_release_before_required_derivation_prevents_execution() -> None:
    source = navigation_source()
    pending = stage_compilation(source)

    result = complete_pending(pending, AvailableSources(()))

    assert isinstance(result, MissingDependency)
    assert result.missing_source == source.identifier
    assert not pending.carrier.fields


def test_08_operational_sufficiency_does_not_imply_exact_reconstruction() -> None:
    encoding = encode_compiled(navigation_source())
    interpretation = policy_reading(encoding)
    activation = require_activation(activate(interpretation))

    outcome = require_outcome(execute(activation, initial_world()))
    reconstruction = attempt_exact_reconstruction(interpretation)

    assert outcome.state.position == "D"
    assert isinstance(reconstruction, IncompleteReconstruction)
    assert "explanation" in reconstruction.missing_fields
    assert "minimum-resources" in reconstruction.missing_fields


def test_09_lossy_collisions_are_explicit() -> None:
    safe = encode_lossily(navigation_source())
    fast = encode_lossily(fast_source())
    registry = registry_from(safe, fast)

    result = interpret(
        safe.carrier,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
        registry,
    )

    assert safe.carrier == fast.carrier
    assert isinstance(result, EncodingCollision)
    assert result.source_identifiers == ("source-fast", "source-safe")


def test_10_carrier_identity_does_not_establish_semantic_equality() -> None:
    safe_source = navigation_source()
    fast = fast_source()
    safe = encode_lossily(safe_source)
    fast_encoding = encode_lossily(fast)

    assert safe.carrier == fast_encoding.carrier
    assert safe_source.guidance != fast.guidance
    assert safe_source.explanation != fast.explanation


def test_11_different_keys_read_one_carrier_in_different_roles() -> None:
    encoding = encode_keyed(navigation_source())
    registry = registry_from(encoding)

    navigation = require_interpretation(
        interpret(
            encoding.carrier,
            NAVIGATION_DECODER,
            NAVIGATION_KEY,
            registry,
        )
    )
    audit = require_interpretation(
        interpret(encoding.carrier, AUDIT_DECODER, AUDIT_KEY, registry)
    )

    assert navigation.carrier is audit.carrier
    assert isinstance(navigation.artifact, CompiledPolicy)
    assert isinstance(audit.artifact, AcceptanceRule)


def test_12_unsupported_interpretation_is_an_owned_result() -> None:
    encoding = encode_compiled(navigation_source())

    result = interpret(
        encoding.carrier,
        AUDIT_DECODER,
        AUDIT_KEY,
        registry_from(encoding),
    )

    assert isinstance(result, UnsupportedInterpretation)
    assert result.carrier is encoding.carrier
    assert result.decoder is AUDIT_DECODER


def test_13_forged_well_shaped_carrier_is_not_derived() -> None:
    encoding = encode_compiled(navigation_source())
    forged = forge_like(encoding)
    registry = registry_from(encoding)

    assessment = assess_carrier(
        forged,
        registry,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
    )
    result = interpret(forged, NAVIGATION_DECODER, NAVIGATION_KEY, registry)

    assert assessment.well_shaped
    assert not assessment.derivable
    assert not assessment.authorized
    assert not assessment.meaningful
    assert isinstance(result, RejectedInterpretation)
    assert result.stage is RejectionStage.DERIVATION


def test_14_equal_outcome_does_not_prove_policy_or_decoding_equality() -> None:
    safe = policy_reading(encode_compiled(navigation_source()))
    fast = policy_reading(encode_compiled(fast_source()))
    safe_outcome = require_outcome(
        execute(require_activation(activate(safe)), initial_world())
    )
    fast_outcome = require_outcome(
        execute(require_activation(activate(fast)), initial_world())
    )

    comparison = compare_outcomes(safe_outcome, fast_outcome)

    assert comparison.same_state
    assert not comparison.same_policy
    assert not comparison.same_decoding


def test_15_provenance_survives_release() -> None:
    source = navigation_source()
    encoding = encode_compiled(source)
    released = release_after_interpretation(encoding, policy_reading(encoding))

    activation = require_activation(activate_released(released))
    outcome = require_outcome(execute(activation, initial_world()))

    assert not released.source_available
    assert released.provenance.source_identifiers == (source.identifier,)
    assert "source-released" in outcome.execution.provenance.history
    assert outcome.execution.provenance.history[-1] == "executed"


def test_16_guidance_and_acceptance_from_one_source_are_separate_artifacts() -> None:
    encoding = encode_keyed(navigation_source())
    registry = registry_from(encoding)
    navigation = require_interpretation(
        interpret(
            encoding.carrier,
            NAVIGATION_DECODER,
            NAVIGATION_KEY,
            registry,
        )
    )
    audit = require_interpretation(
        interpret(encoding.carrier, AUDIT_DECODER, AUDIT_KEY, registry)
    )

    assert navigation.artifact is not audit.artifact
    assert type(navigation.artifact) is not type(audit.artifact)
    assert (
        navigation.artifact.provenance.source_identifiers
        == audit.artifact.provenance.source_identifiers
    )


def test_17_shared_derivation_differs_from_accidental_local_equality() -> None:
    original = encode_keyed(navigation_source("origin"))
    same_local = encode_keyed(navigation_source("copy"))
    original_policy = require_interpretation(
        interpret(
            original.carrier,
            NAVIGATION_DECODER,
            NAVIGATION_KEY,
            registry_from(original),
        )
    )
    copied_policy = require_interpretation(
        interpret(
            same_local.carrier,
            NAVIGATION_DECODER,
            NAVIGATION_KEY,
            registry_from(same_local),
        )
    )
    original_audit = require_interpretation(
        interpret(
            original.carrier,
            AUDIT_DECODER,
            AUDIT_KEY,
            registry_from(original),
        )
    )

    accidental = compare_artifacts(
        original_policy.artifact,
        copied_policy.artifact,
    )
    shared = compare_artifacts(original_policy.artifact, original_audit.artifact)

    assert accidental.same_local_value
    assert not accidental.shared_source
    assert not accidental.same_provenance
    assert shared.shared_source


def test_18_neutral_mechanics_define_no_foundation_named_classes() -> None:
    experiment_root = Path(source_module.__file__).parent
    forbidden = {"Form", "Will", "Spell", "Reader", "Cast", "Effect", "Potential"}
    defined: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        defined.update(
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

    assert defined.isdisjoint(forbidden)


def test_19_post_hoc_mapping_preserves_failed_and_open_matches() -> None:
    report = attempt_mapping()

    activation = next(
        item for item in report.mappings if item.neutral_term == "Activation"
    )
    assert activation.status is MappingStatus.UNMAPPED
    assert not report.finding.representation_self_interprets
    assert not report.finding.release_erases_provenance
    assert report.open_questions


def test_20_package_source_remains_untouched() -> None:
    repository_root = Path(source_module.__file__).parents[2]
    result = subprocess.run(
        ["git", "status", "--short", "--", "src/arx_mentis"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert not result.stdout.strip()


def test_21_transparent_encoding_round_trips_exactly() -> None:
    source = navigation_source()
    encoding = encode_transparently(source)

    interpretation = require_interpretation(
        interpret(
            encoding.carrier,
            EXACT_DECODER,
            EXACT_KEY,
            registry_from(encoding),
        )
    )
    reconstruction = attempt_exact_reconstruction(interpretation)

    assert isinstance(reconstruction, SourceReconstruction)
    assert reconstruction.source == source
    assert reconstruction.source is not source


def test_22_retained_bundle_keeps_source_carrier_and_policy_available() -> None:
    source = navigation_source()
    encoding = encode_compiled(source)
    interpretation = policy_reading(encoding)

    bundle = retain(source, encoding, interpretation)

    assert bundle.source is source
    assert bundle.carrier is encoding.carrier
    assert bundle.interpretation is interpretation


def test_23_opaque_carrier_is_derived_but_inert_and_unsupported() -> None:
    encoding = encode_opaquely(navigation_source())
    registry = registry_from(encoding)

    assessment = assess_carrier(
        encoding.carrier,
        registry,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
    )
    reading = interpret(
        encoding.carrier,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
        registry,
    )
    activation = activate(encoding.carrier)

    assert assessment.derivable
    assert assessment.authorized
    assert not assessment.meaningful
    assert not assessment.operative
    assert isinstance(reading, UnsupportedInterpretation)
    assert isinstance(activation, RejectedActivation)


def test_24_execution_requires_activation_not_only_interpretation() -> None:
    interpretation = policy_reading(encode_compiled(navigation_source()))

    result = execute(interpretation, initial_world())

    assert isinstance(result, ExecutionRefused)
    assert result.stage is RejectionStage.EXECUTION
    assert initial_world().position == "A"


def test_25_pending_compilation_succeeds_while_source_is_available() -> None:
    source = navigation_source()
    pending = stage_compilation(source)

    result = complete_pending(pending, AvailableSources((source,)))

    assert isinstance(result, Encoding)
    assert result.source is source
    assert result.carrier.fields


def test_26_carrier_assessment_changes_only_at_declared_stages() -> None:
    encoding = encode_compiled(navigation_source())
    registry = registry_from(encoding)
    before = assess_carrier(
        encoding.carrier,
        registry,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
    )
    interpretation = policy_reading(encoding)
    activation = require_activation(activate(interpretation))
    after = assess_carrier(
        encoding.carrier,
        registry,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
        activation,
    )

    assert before.well_shaped
    assert before.derivable
    assert before.authorized
    assert before.meaningful
    assert not before.operative
    assert after.operative


def test_27_experiment_imports_no_package_or_other_experiment() -> None:
    experiment_root = Path(source_module.__file__).parent
    forbidden_prefixes = (
        "arx_mentis",
        "experiments.euclid_i_1",
        "experiments.ars_astronomica_settlement",
        "experiments.ars_grammatica_reading",
        "experiments.ars_dialectica_verification",
        "experiments.virtual_mediation",
        "experiments.omen_attribution",
        "experiments.actualization",
    )
    imported: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)

    assert not any(
        name.startswith(prefix) for name in imported for prefix in forbidden_prefixes
    )


def test_28_derivable_but_unauthorized_is_distinct_from_forgery() -> None:
    encoding = encode_compiled(navigation_source())
    record = DerivationRecord(
        encoding.source.identifier,
        encoding.carrier,
        encoding.rule,
        authorized=False,
    )
    registry = DerivationRegistry(frozenset({record}))

    assessment = assess_carrier(
        encoding.carrier,
        registry,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
    )
    result = interpret(
        encoding.carrier,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
        registry,
    )

    assert assessment.well_shaped
    assert assessment.derivable
    assert not assessment.authorized
    assert not assessment.meaningful
    assert isinstance(result, RejectedInterpretation)
    assert result.stage is RejectionStage.AUTHORIZATION
