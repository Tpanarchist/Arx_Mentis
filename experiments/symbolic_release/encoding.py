"""Independent encoders, including deliberately lossy and opaque variants."""

from __future__ import annotations

from .source import (
    Carrier,
    DerivationRecord,
    DerivationRegistry,
    EncodedField,
    Encoding,
    EncodingKind,
    EncodingRule,
    PendingCarrier,
    SourceForm,
)

TRANSPARENT_RULE = EncodingRule("transparent-v1", EncodingKind.TRANSPARENT)
COMPILED_RULE = EncodingRule("compiled-v1", EncodingKind.COMPILED)
KEYED_RULE = EncodingRule("keyed-v1", EncodingKind.KEYED)
OPAQUE_RULE = EncodingRule("opaque-v1", EncodingKind.OPAQUE)
LOSSY_RULE = EncodingRule("lossy-destination-v1", EncodingKind.LOSSY)


def _action_fields(source: SourceForm) -> tuple[EncodedField, ...]:
    return tuple(
        EncodedField(f"action:{index:03}", action)
        for index, action in enumerate(source.guidance)
    )


def _finish(
    source: SourceForm,
    rule: EncodingRule,
    carrier: Carrier,
    *,
    authorized: bool = True,
) -> Encoding:
    record = DerivationRecord(source.identifier, carrier, rule, authorized)
    return Encoding(source, rule, carrier, record)


def encode_transparently(source: SourceForm) -> Encoding:
    fields = (
        EncodedField("source", source.identifier),
        *_action_fields(source),
        EncodedField("destination", source.destination),
        EncodedField("minimum-resources", str(source.minimum_resources)),
        EncodedField("explanation", source.explanation),
    )
    carrier = Carrier(
        f"T:{source.identifier}",
        TRANSPARENT_RULE.identifier,
        f"derived:{TRANSPARENT_RULE.identifier}:{source.identifier}",
        fields,
    )
    return _finish(source, TRANSPARENT_RULE, carrier)


def encode_compiled(source: SourceForm) -> Encoding:
    carrier = Carrier(
        f"C:{source.identifier}",
        COMPILED_RULE.identifier,
        f"derived:{COMPILED_RULE.identifier}:{source.identifier}",
        _action_fields(source),
    )
    return _finish(source, COMPILED_RULE, carrier)


def encode_keyed(source: SourceForm) -> Encoding:
    fields = (
        *_action_fields(source),
        EncodedField("destination", source.destination),
        EncodedField("minimum-resources", str(source.minimum_resources)),
    )
    carrier = Carrier(
        f"K:{source.identifier}",
        KEYED_RULE.identifier,
        f"derived:{KEYED_RULE.identifier}:{source.identifier}",
        fields,
    )
    return _finish(source, KEYED_RULE, carrier)


def encode_opaquely(source: SourceForm) -> Encoding:
    carrier = Carrier(
        f"O:{source.identifier}",
        OPAQUE_RULE.identifier,
        f"derived:{OPAQUE_RULE.identifier}:{source.identifier}",
        (EncodedField("opaque", "unread"),),
    )
    return _finish(source, OPAQUE_RULE, carrier)


def encode_lossily(source: SourceForm) -> Encoding:
    symbol = f"Q:{source.destination}"
    carrier = Carrier(
        symbol,
        LOSSY_RULE.identifier,
        f"derived:{LOSSY_RULE.identifier}:{symbol}",
        (EncodedField("destination", source.destination),),
    )
    return _finish(source, LOSSY_RULE, carrier)


def forge_like(encoding: Encoding) -> Carrier:
    return Carrier(
        f"F:{encoding.carrier.symbol}",
        encoding.rule.identifier,
        f"unregistered:{encoding.rule.identifier}",
        encoding.carrier.fields,
    )


def registry_from(*encodings: Encoding) -> DerivationRegistry:
    return DerivationRegistry(frozenset(encoding.derivation for encoding in encodings))


def stage_compilation(source: SourceForm) -> PendingCarrier:
    carrier = Carrier(
        f"P:{source.identifier}",
        COMPILED_RULE.identifier,
        f"pending:{COMPILED_RULE.identifier}:{source.identifier}",
        (),
    )
    return PendingCarrier(carrier, source.identifier, COMPILED_RULE)
