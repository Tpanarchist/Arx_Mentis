"""Run the human-readable State Zero Experiment 008 witness."""

from .activation import execute
from .countermodels import attempt_exact_reconstruction, compare_outcomes
from .encoding import encode_compiled, encode_keyed, registry_from
from .foundation_mapping import attempt_mapping
from .interpretation import (
    AUDIT_DECODER,
    AUDIT_KEY,
    NAVIGATION_DECODER,
    NAVIGATION_KEY,
    interpret,
)
from .release import activate_released, release_after_interpretation
from .scenarios import fast_source, initial_world, navigation_source
from .source import (
    Activation,
    Encoding,
    IncompleteReconstruction,
    Interpretation,
    Outcome,
)


def _interpret_policy(encoding: Encoding) -> Interpretation:
    result = interpret(
        encoding.carrier,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
        registry_from(encoding),
    )
    assert isinstance(result, Interpretation)
    return result


def main() -> None:
    source = navigation_source()
    compiled = encode_compiled(source)
    policy_reading = _interpret_policy(compiled)
    incomplete = attempt_exact_reconstruction(policy_reading)
    released = release_after_interpretation(compiled, policy_reading)
    activation = activate_released(released)
    assert isinstance(activation, Activation)
    outcome = execute(activation, initial_world())
    assert isinstance(outcome, Outcome)

    keyed = encode_keyed(source)
    keyed_registry = registry_from(keyed)
    navigation = interpret(
        keyed.carrier,
        NAVIGATION_DECODER,
        NAVIGATION_KEY,
        keyed_registry,
    )
    audit = interpret(keyed.carrier, AUDIT_DECODER, AUDIT_KEY, keyed_registry)
    assert isinstance(navigation, Interpretation)
    assert isinstance(audit, Interpretation)

    fast_encoding = encode_compiled(fast_source())
    fast_reading = _interpret_policy(fast_encoding)
    fast_release = release_after_interpretation(fast_encoding, fast_reading)
    fast_activation = activate_released(fast_release)
    assert isinstance(fast_activation, Activation)
    fast_outcome = execute(fast_activation, initial_world())
    assert isinstance(fast_outcome, Outcome)
    comparison = compare_outcomes(outcome, fast_outcome)
    mapping = attempt_mapping()

    print(
        "compiled release: "
        f"source-available={released.source_available}, "
        f"position={outcome.state.position}"
    )
    print(
        "operationally sufficient but exact reconstruction: "
        f"{not isinstance(incomplete, IncompleteReconstruction)}"
    )
    print(
        "one carrier readings: "
        f"{type(navigation.artifact).__name__}/{type(audit.artifact).__name__}"
    )
    print(
        "equal outcomes identify decoding: "
        f"state={comparison.same_state}, decoding={comparison.same_decoding}"
    )
    print(f"foundation boundary: {mapping.finding.conclusion}")


if __name__ == "__main__":
    main()
