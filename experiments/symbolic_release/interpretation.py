"""Lawful keyed interpretation with explicit derivation and collision checks."""

from __future__ import annotations

from .encoding import COMPILED_RULE, KEYED_RULE, TRANSPARENT_RULE
from .source import (
    AcceptanceRule,
    Activation,
    Carrier,
    CarrierAssessment,
    CompiledPolicy,
    Decoder,
    DerivationRecord,
    DerivationRegistry,
    EncodingCollision,
    Interpretation,
    InterpretationKey,
    Provenance,
    ReadingRole,
    RejectedInterpretation,
    RejectionStage,
    SourceForm,
    SourceReconstruction,
    UnsupportedInterpretation,
)

EXACT_KEY = InterpretationKey("exact-source", ReadingRole.EXACT)
NAVIGATION_KEY = InterpretationKey("navigation", ReadingRole.NAVIGATION)
AUDIT_KEY = InterpretationKey("audit", ReadingRole.AUDIT)

EXACT_DECODER = Decoder(
    "exact-decoder",
    frozenset({(TRANSPARENT_RULE.identifier, ReadingRole.EXACT)}),
)
NAVIGATION_DECODER = Decoder(
    "navigation-decoder",
    frozenset(
        {
            (COMPILED_RULE.identifier, ReadingRole.NAVIGATION),
            (KEYED_RULE.identifier, ReadingRole.NAVIGATION),
        }
    ),
)
AUDIT_DECODER = Decoder(
    "audit-decoder",
    frozenset({(KEYED_RULE.identifier, ReadingRole.AUDIT)}),
)


def _matching_records(
    carrier: Carrier,
    registry: DerivationRegistry,
) -> tuple[DerivationRecord, ...]:
    return tuple(
        sorted(
            (record for record in registry.records if record.carrier == carrier),
            key=lambda record: record.source_identifier,
        )
    )


def _field(carrier: Carrier, name: str) -> str:
    return next(field.value for field in carrier.fields if field.name == name)


def _actions(carrier: Carrier) -> tuple[str, ...]:
    return tuple(
        field.value for field in carrier.fields if field.name.startswith("action:")
    )


def _provenance(
    records: tuple[DerivationRecord, ...],
    carrier: Carrier,
    key: InterpretationKey,
) -> Provenance:
    return Provenance(
        tuple(record.source_identifier for record in records),
        carrier.rule_identifier,
        carrier.symbol,
        ("encoded", f"interpreted:{key.identifier}"),
    )


def interpret(
    carrier: Carrier,
    decoder: Decoder,
    key: InterpretationKey,
    registry: DerivationRegistry,
) -> (
    Interpretation
    | UnsupportedInterpretation
    | RejectedInterpretation
    | EncodingCollision
):
    if not carrier.symbol or not carrier.rule_identifier or not carrier.derivation_tag:
        return RejectedInterpretation(
            carrier,
            RejectionStage.SHAPE,
            "carrier lacks a required structural field",
        )
    records = _matching_records(carrier, registry)
    if not records:
        return RejectedInterpretation(
            carrier,
            RejectionStage.DERIVATION,
            "no declared encoding derivation produces this carrier",
        )
    source_ids = tuple(record.source_identifier for record in records)
    if len(set(source_ids)) > 1:
        return EncodingCollision(
            carrier,
            source_ids,
            "lossy encoding maps distinct sources to one carrier",
        )
    if not all(record.authorized for record in records):
        return RejectedInterpretation(
            carrier,
            RejectionStage.AUTHORIZATION,
            "the derivation exists but is not authorized",
        )
    if (carrier.rule_identifier, key.role) not in decoder.supported_readings:
        return UnsupportedInterpretation(
            carrier,
            decoder,
            key,
            "decoder does not declare this rule and reading role",
        )

    provenance = _provenance(records, carrier, key)
    if key.role is ReadingRole.EXACT:
        source = SourceForm(
            _field(carrier, "source"),
            _actions(carrier),
            _field(carrier, "destination"),
            int(_field(carrier, "minimum-resources")),
            _field(carrier, "explanation"),
        )
        artifact = SourceReconstruction(source, provenance)
    elif key.role is ReadingRole.NAVIGATION:
        artifact = CompiledPolicy(
            f"policy:{carrier.symbol}",
            _actions(carrier),
            provenance,
        )
    else:
        artifact = AcceptanceRule(
            f"acceptance:{carrier.symbol}",
            _field(carrier, "destination"),
            int(_field(carrier, "minimum-resources")),
            provenance,
        )
    return Interpretation(carrier, decoder.identifier, key, artifact)


def assess_carrier(
    carrier: Carrier,
    registry: DerivationRegistry,
    decoder: Decoder,
    key: InterpretationKey,
    activation: Activation | None = None,
) -> CarrierAssessment:
    well_shaped = bool(
        carrier.symbol and carrier.rule_identifier and carrier.derivation_tag
    )
    records = _matching_records(carrier, registry)
    derivable = bool(records)
    authorized = derivable and all(record.authorized for record in records)
    meaningful = (
        authorized
        and len({record.source_identifier for record in records}) == 1
        and (carrier.rule_identifier, key.role) in decoder.supported_readings
    )
    operative = (
        activation is not None
        and activation.provenance.carrier_symbol == carrier.symbol
    )
    return CarrierAssessment(
        well_shaped,
        derivable,
        authorized,
        meaningful,
        operative,
    )
