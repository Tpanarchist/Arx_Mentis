from __future__ import annotations

import ast
import subprocess
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

import experiments.bound_delegation.records as records_module
from experiments.bound_delegation.authority import (
    amplified_authority,
    attenuated_authority,
    contained_authority,
    delegating_authority,
    dependency_profile,
)
from experiments.bound_delegation.countermodels import (
    reject_activation_only_lease_check,
    reject_authority_as_instruction_data,
    reject_child_amplification,
    reject_compensation_deletes_harm,
    reject_compiled_as_unrestricted,
    reject_delegate_only_causation,
    reject_post_mutation_budget_check,
    reject_principal_only_causation,
    reject_revocation_always_cascades,
    reject_revocation_erases_history,
    reject_revocation_never_cascades,
    reject_role_grants_authority,
    reject_same_artifact_same_authority,
    reject_scope_as_consequence_boundary,
    reject_success_justifies_excess,
)
from experiments.bound_delegation.derivation import (
    admit_artifact,
    copy_delegate,
    derive_child,
    derive_delegate,
    release_source,
)
from experiments.bound_delegation.execution import (
    EMPTY_TRACE,
    activate_delegate,
    execute_action,
)
from experiments.bound_delegation.foundation_mapping import (
    MappingStatus,
    attempt_mapping,
)
from experiments.bound_delegation.plans import rebalance_plan
from experiments.bound_delegation.principals import standard_principal
from experiments.bound_delegation.records import (
    ActionKind,
    ActionSpec,
    Activation,
    Admission,
    AuditView,
    AuthorityAmplification,
    AuthorityConflict,
    Capability,
    Compartment,
    ConsequenceKind,
    ControlView,
    CountermodelRejection,
    Derivation,
    ExecutionResult,
    InadmissibleArtifact,
    Refusal,
    RefusalKind,
    ResolutionKind,
    ResolutionPolicy,
    ResolvedDelegate,
    RevocationMode,
    Role,
    UnspecifiedRevocation,
)
from experiments.bound_delegation.revocation import record_switch, revoke_principal
from experiments.bound_delegation.roles import read_as
from experiments.bound_delegation.scenarios import contained_session, spillover_session
from experiments.bound_delegation.scopes import reconcile_delegates
from experiments.bound_delegation.world import compartment_state, initial_environment


def require_derivation(result: object) -> Derivation:
    assert isinstance(result, Derivation)
    return result


def standard_derivation(
    *,
    revocation_mode: RevocationMode = RevocationMode.LIVE_LINKED,
    priority: int = 5,
    identifier: str = "delegate:rebalance",
) -> Derivation:
    principal = standard_principal()
    return require_derivation(
        derive_delegate(
            rebalance_plan(principal.identifier),
            principal,
            contained_authority(
                revocation_mode=revocation_mode,
                priority=priority,
            ),
            identifier=identifier,
        )
    )


def activated_control(
    derivation: Derivation,
    *,
    step: int = 2,
) -> tuple[Activation, ControlView]:
    activation = activate_delegate(derivation.delegate, derivation.registry, step=step)
    assert isinstance(activation, Activation)
    control = read_as(derivation.delegate, Role.CONTROL)
    assert isinstance(control, ControlView)
    return activation, control


def test_01_source_plan_derives_separate_delegate() -> None:
    principal = standard_principal()
    plan = rebalance_plan(principal.identifier)

    derivation = require_derivation(
        derive_delegate(plan, principal, contained_authority())
    )

    assert derivation.source_plan is plan
    assert derivation.delegate.identifier != plan.identifier
    assert derivation.delegate.instructions == plan.instructions
    assert derivation.delegate.compiled


def test_02_derivation_leaves_source_plan_unchanged() -> None:
    principal = standard_principal()
    plan = rebalance_plan(principal.identifier)
    snapshot = plan

    derive_delegate(plan, principal, contained_authority())

    assert plan is snapshot
    assert plan == snapshot


def test_03_delegate_executes_after_source_content_release() -> None:
    session = contained_session()

    assert not session.source_availability.available
    assert (
        session.source_availability.source_plan_identifier
        == session.source_plan.identifier
    )
    assert len(session.trace.actions) == 3
    assert all(
        item.delegate_identifier == session.delegate.identifier
        for item in session.trace.actions
    )


def test_04_independence_is_a_dependency_vector_not_boolean() -> None:
    profile = dependency_profile()

    assert profile.source_content.value == "independent"
    assert profile.authority.value == "lease-dependent"
    assert profile.resources.value == "environment-dependent"
    assert profile.scope.value == "fixed"
    assert profile.lifecycle.value == "revocable"
    assert profile.interpretation.value == "compiled"
    assert profile.provenance.value == "retained"
    assert not hasattr(profile, "independent")


def test_05_role_is_distinct_from_authority() -> None:
    derivation = standard_derivation()
    copied = copy_delegate(
        derivation.delegate,
        identifier="copy:instructions-only",
        include_authority=False,
        include_lineage=False,
    )

    audit = read_as(copied, Role.AUDIT)
    control = read_as(copied, Role.CONTROL)

    assert isinstance(audit, AuditView)
    assert audit.explanation
    assert isinstance(control, ControlView)
    assert control.authority is None
    assert control.lineage is None


def test_06_audit_interpretation_does_not_authorize_control() -> None:
    derivation = standard_derivation()
    activation, _ = activated_control(derivation)
    audit = read_as(derivation.delegate, Role.AUDIT)
    environment = initial_environment()

    result = execute_action(
        audit,
        derivation.delegate,
        activation,
        derivation.delegate.instructions[0],
        environment,
        EMPTY_TRACE,
        derivation.registry,
        step=2,
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.ROLE_UNAUTHORIZED
    assert result.environment is environment


def test_07_control_requires_explicit_capability() -> None:
    derivation = standard_derivation()
    activation, control = activated_control(derivation)
    environment = initial_environment()
    protected = ActionSpec(
        ActionKind.ALTER_PROTECTED,
        Compartment.NORTH,
        None,
        0,
    )

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        protected,
        environment,
        EMPTY_TRACE,
        derivation.registry,
        step=2,
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.MISSING_CAPABILITY
    assert result.environment is environment


def test_08_scope_escape_is_refused_before_mutation() -> None:
    derivation = standard_derivation()
    activation, control = activated_control(derivation)
    environment = initial_environment()
    snapshot = environment
    escape = ActionSpec(
        ActionKind.TRANSFER,
        Compartment.NORTH,
        Compartment.SOUTH,
        1,
    )

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        escape,
        environment,
        EMPTY_TRACE,
        derivation.registry,
        step=2,
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.SCOPE_ESCAPE
    assert result.environment is snapshot
    assert result.trace is EMPTY_TRACE


def test_09_budget_exhaustion_is_explicit_and_pre_mutation() -> None:
    session = contained_session()
    control = read_as(session.delegate, Role.CONTROL)
    assert isinstance(control, ControlView)
    snapshot = session.environment

    result = execute_action(
        control,
        session.delegate,
        session.activation,
        session.source_plan.instructions[0],
        session.environment,
        session.trace,
        session.registry,
        step=5,
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.BUDGET_EXHAUSTED
    assert result.environment is snapshot
    assert len(result.trace.actions) == 3


def test_10_lease_expiry_blocks_each_future_action() -> None:
    derivation = standard_derivation()
    activation, control = activated_control(derivation)
    environment = initial_environment()

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        derivation.delegate.instructions[0],
        environment,
        EMPTY_TRACE,
        derivation.registry,
        step=6,
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.LEASE_INACTIVE
    assert result.environment is environment


def test_11_expiry_preserves_prior_authorized_action_records() -> None:
    derivation = standard_derivation()
    activation, control = activated_control(derivation)
    first = execute_action(
        control,
        derivation.delegate,
        activation,
        derivation.delegate.instructions[0],
        initial_environment(),
        EMPTY_TRACE,
        derivation.registry,
        step=2,
    )
    assert isinstance(first, ExecutionResult)
    snapshot = first.trace

    expired = execute_action(
        control,
        derivation.delegate,
        activation,
        derivation.delegate.instructions[1],
        first.environment,
        first.trace,
        derivation.registry,
        step=6,
    )

    assert isinstance(expired, Refusal)
    assert expired.trace == snapshot
    assert expired.trace.actions[0].step == 2


def test_12_live_linked_revocation_disables_future_action() -> None:
    principal = standard_principal()
    derivation = require_derivation(
        derive_delegate(
            rebalance_plan(principal.identifier),
            principal,
            contained_authority(revocation_mode=RevocationMode.LIVE_LINKED),
        )
    )
    activation, control = activated_control(derivation)
    revocation = revoke_principal(
        principal, reason="authority withdrawn", revoked_step=3
    )

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        derivation.delegate.instructions[0],
        initial_environment(),
        EMPTY_TRACE,
        derivation.registry,
        step=4,
        revocations=(revocation,),
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.REVOKED


def test_13_declared_snapshot_continues_after_source_revocation() -> None:
    principal = standard_principal()
    derivation = require_derivation(
        derive_delegate(
            rebalance_plan(principal.identifier),
            principal,
            contained_authority(revocation_mode=RevocationMode.SNAPSHOT),
        )
    )
    activation, control = activated_control(derivation)
    revocation = revoke_principal(
        principal, reason="current grant withdrawn", revoked_step=3
    )

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        derivation.delegate.instructions[0],
        initial_environment(),
        EMPTY_TRACE,
        derivation.registry,
        step=4,
        revocations=(revocation,),
    )

    assert isinstance(result, ExecutionResult)
    assert result.action.step == 4


def test_14_unspecified_revocation_behavior_is_rejected() -> None:
    derivation = standard_derivation(revocation_mode=RevocationMode.UNSPECIFIED)

    result = activate_delegate(derivation.delegate, derivation.registry, step=2)

    assert isinstance(result, UnspecifiedRevocation)


def test_15_copying_instructions_does_not_copy_authority() -> None:
    derivation = standard_derivation()
    copied = copy_delegate(
        derivation.delegate,
        identifier="copy:unauthorized",
        include_authority=False,
        include_lineage=False,
    )

    result = admit_artifact(copied, derivation.registry)

    assert copied.instructions == derivation.delegate.instructions
    assert isinstance(result, InadmissibleArtifact)
    assert "no authority" in result.reason


def test_16_forged_lineage_is_inadmissible() -> None:
    derivation = standard_derivation()
    copied = copy_delegate(
        derivation.delegate,
        identifier="copy:forged",
        include_authority=True,
        include_lineage=True,
    )
    assert copied.lineage is not None
    forged = replace(
        copied,
        lineage=replace(copied.lineage, identifier="lineage:forged"),
    )

    result = admit_artifact(forged, derivation.registry)

    assert isinstance(result, InadmissibleArtifact)
    assert "not admitted" in result.reason


def test_17_child_delegation_cannot_amplify_authority() -> None:
    principal = standard_principal()
    parent = require_derivation(
        derive_delegate(
            rebalance_plan(principal.identifier),
            principal,
            delegating_authority(),
            identifier="delegate:parent",
        )
    )

    result = derive_child(
        parent.delegate,
        amplified_authority(parent.delegate.authority),
        parent.registry,
        identifier="delegate:amplified-child",
        derived_step=2,
    )

    assert isinstance(result, AuthorityAmplification)
    assert Capability.ALTER_PROTECTED in result.excess_capabilities
    assert Compartment.SOUTH in result.excess_scopes


def test_18_attenuated_child_delegation_is_lawful() -> None:
    principal = standard_principal()
    parent = require_derivation(
        derive_delegate(
            rebalance_plan(principal.identifier),
            principal,
            delegating_authority(),
            identifier="delegate:parent",
        )
    )

    result = derive_child(
        parent.delegate,
        attenuated_authority(parent.delegate.authority),
        parent.registry,
        identifier="delegate:child",
        derived_step=2,
    )

    assert isinstance(result, Derivation)
    assert (
        result.delegate.authority.capabilities < parent.delegate.authority.capabilities
    )
    assert result.delegate.authority.maximum_transfer_units == 1
    assert (
        result.delegate.lineage.parent_delegate_identifier == parent.delegate.identifier
    )
    assert isinstance(admit_artifact(result.delegate, result.registry), Admission)


def test_19_operation_scope_and_consequence_extent_are_distinct() -> None:
    consequences, _ = spillover_session()

    assert consequences.spillover.direct_scopes == frozenset({Compartment.NORTH})
    assert consequences.spillover.consequence.affected_compartment is Compartment.SOUTH
    assert Compartment.SOUTH not in consequences.spillover.direct_scopes


def test_20_spillover_remains_observable() -> None:
    consequences, _ = spillover_session()
    south = compartment_state(consequences.environment, Compartment.SOUTH)

    assert consequences.spillover.consequence.kind is ConsequenceKind.SOUTH_SHORTAGE
    assert south.resource_units == 2
    assert consequences.spillover.consequence in consequences.trace.consequences


def test_21_blowback_retains_causal_path_to_delegate_action() -> None:
    consequences, _ = spillover_session()

    assert consequences.blowback.kind is ConsequenceKind.PRINCIPAL_RESOURCE_LOSS
    assert consequences.environment.principal_resource_units == 2
    assert (
        consequences.blowback.causal_chain[0]
        == consequences.spillover.action_identifier
    )


def test_22_compensation_does_not_erase_original_consequence() -> None:
    consequences, repaired = spillover_session()

    assert consequences.spillover.consequence in repaired.trace.consequences
    assert consequences.blowback in repaired.trace.consequences
    assert repaired.compensation.original_consequence_identifier == (
        consequences.spillover.consequence.identifier
    )
    assert repaired.repair_consequence.kind is ConsequenceKind.REPAIRED_SHORTAGE
    assert len(repaired.trace.consequences) == 3


def test_23_useful_hypothetical_outcome_does_not_validate_scope_escape() -> None:
    derivation = standard_derivation()
    activation, control = activated_control(derivation)
    environment = initial_environment()
    escape = ActionSpec(
        ActionKind.TRANSFER,
        Compartment.NORTH,
        Compartment.SOUTH,
        1,
    )

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        escape,
        environment,
        EMPTY_TRACE,
        derivation.registry,
        step=2,
    )

    assert compartment_state(environment, Compartment.SOUTH).resource_units == 3
    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.SCOPE_ESCAPE
    assert reject_success_justifies_excess().countermodel == (
        "success-justifies-excess-authority"
    )


def test_24_equal_delegate_values_retain_different_authority_lineage() -> None:
    first = standard_derivation(identifier="delegate:first")
    second = standard_derivation(identifier="delegate:second")

    assert first.delegate.instructions == second.delegate.instructions
    assert first.delegate.lineage != second.delegate.lineage
    assert first.delegate.identifier != second.delegate.identifier


def test_25_revocation_and_switch_preserve_earlier_trace() -> None:
    principal = standard_principal()
    first = standard_derivation(identifier="delegate:first")
    activation, control = activated_control(first)
    executed = execute_action(
        control,
        first.delegate,
        activation,
        first.delegate.instructions[0],
        initial_environment(),
        EMPTY_TRACE,
        first.registry,
        step=2,
    )
    assert isinstance(executed, ExecutionResult)
    snapshot = executed.trace
    second = standard_derivation(identifier="delegate:second")

    revoke_principal(principal, reason="switch", revoked_step=3)
    switch = record_switch(
        first.delegate, second.delegate, switched_step=3, reason="switch"
    )

    assert executed.trace == snapshot
    assert snapshot.actions[0].delegate_identifier == first.delegate.identifier
    assert switch.previous_delegate_identifier == first.delegate.identifier
    assert switch.next_delegate_identifier == second.delegate.identifier


def test_26_reversing_storage_order_preserves_authority_conflict() -> None:
    first = standard_derivation(identifier="delegate:first")
    second = standard_derivation(identifier="delegate:second")

    forward = reconcile_delegates((first.delegate, second.delegate))
    reversed_result = reconcile_delegates((second.delegate, first.delegate))

    assert isinstance(forward, AuthorityConflict)
    assert forward == reversed_result


def test_27_declared_priority_policy_resolves_conflict() -> None:
    lower = standard_derivation(priority=3, identifier="delegate:lower")
    higher = standard_derivation(priority=8, identifier="delegate:higher")
    policy = ResolutionPolicy("higher-priority-wins", ResolutionKind.HIGHER_PRIORITY)

    result = reconcile_delegates((lower.delegate, higher.delegate), policy)

    assert isinstance(result, ResolvedDelegate)
    assert result.delegate is higher.delegate
    assert result.policy is policy


def test_28_foundation_mapping_occurs_after_neutral_probe() -> None:
    report = attempt_mapping()
    role = next(item for item in report.mappings if item.neutral_term == "Role")
    unrestricted = next(
        item
        for item in report.mappings
        if item.neutral_term == "Compiled as unrestricted"
    )

    assert role.status is MappingStatus.PRESSURE
    assert unrestricted.status is MappingStatus.REJECTED
    assert not report.finding.role_grants_authority
    assert not report.finding.total_independence
    assert report.finding.prospective_history_recurs
    assert report.finding.attenuation_is_general is None


def test_29_neutral_mechanics_define_no_foundation_named_classes() -> None:
    experiment_root = Path(records_module.__file__).parent
    forbidden = {"Form", "Will", "Ars", "Spell", "Cast", "Effect", "Demonstration"}
    defined: set[str] = set()
    for module_path in experiment_root.glob("*.py"):
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        defined.update(
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        )

    assert defined.isdisjoint(forbidden)


def test_30_package_source_remains_untouched() -> None:
    repository_root = Path(records_module.__file__).parents[2]
    result = subprocess.run(
        ["git", "status", "--short", "--", "src/arx_mentis"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert not result.stdout.strip()


def test_31_per_action_transfer_limit_is_checked_before_mutation() -> None:
    derivation = standard_derivation()
    activation, control = activated_control(derivation)
    environment = initial_environment()
    oversized = ActionSpec(
        ActionKind.TRANSFER,
        Compartment.NORTH,
        Compartment.CENTER,
        3,
    )

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        oversized,
        environment,
        EMPTY_TRACE,
        derivation.registry,
        step=2,
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.TRANSFER_LIMIT
    assert result.environment is environment


def test_32_activation_does_not_waive_later_lease_check() -> None:
    derivation = standard_derivation()
    activation, control = activated_control(derivation, step=2)

    result = execute_action(
        control,
        derivation.delegate,
        activation,
        derivation.delegate.instructions[0],
        initial_environment(),
        EMPTY_TRACE,
        derivation.registry,
        step=6,
    )

    assert isinstance(result, Refusal)
    assert result.kind is RefusalKind.LEASE_INACTIVE
    assert reject_activation_only_lease_check().countermodel == (
        "lease-checked-only-at-activation"
    )


def test_33_principal_revocation_blocks_new_snapshot_derivation() -> None:
    principal = standard_principal()
    plan = rebalance_plan(principal.identifier)
    revocation = revoke_principal(principal, reason="withdrawn", revoked_step=3)

    result = derive_delegate(
        plan,
        principal,
        contained_authority(revocation_mode=RevocationMode.SNAPSHOT),
        identifier="delegate:late-snapshot",
        derived_step=4,
        revocations=(revocation,),
    )

    assert isinstance(result, InadmissibleArtifact)
    assert "blocks new" in result.reason


def test_34_standard_delegate_cannot_manufacture_child_capability() -> None:
    parent = standard_derivation(identifier="delegate:non-delegating")

    result = derive_child(
        parent.delegate,
        attenuated_authority(parent.delegate.authority),
        parent.registry,
        identifier="delegate:forbidden-child",
        derived_step=2,
    )

    assert isinstance(result, AuthorityAmplification)
    assert Capability.DERIVE_DELEGATE in result.excess_capabilities


def test_35_compensation_restores_state_without_rewriting_trace() -> None:
    consequences, repaired = spillover_session()

    before = compartment_state(consequences.environment, Compartment.SOUTH)
    after = compartment_state(repaired.environment, Compartment.SOUTH)
    assert (before.resource_units, after.resource_units) == (2, 3)
    assert repaired.trace.actions == consequences.trace.actions
    assert repaired.trace.consequences[:2] == consequences.trace.consequences


def test_36_source_release_and_principal_revocation_are_distinct() -> None:
    principal = standard_principal()
    plan = rebalance_plan(principal.identifier)
    availability = release_source(plan, changed_step=2)
    revocation = revoke_principal(principal, reason="authority ended", revoked_step=4)

    assert availability.source_plan_identifier == plan.identifier
    assert not availability.available
    assert revocation.principal_identifier == principal.identifier
    assert availability.changed_step != revocation.revoked_step


def test_37_all_hostile_countermodels_are_owned() -> None:
    rejections = (
        reject_role_grants_authority(),
        reject_compiled_as_unrestricted(),
        reject_authority_as_instruction_data(),
        reject_scope_as_consequence_boundary(),
        reject_revocation_erases_history(),
        reject_revocation_always_cascades(),
        reject_revocation_never_cascades(),
        reject_child_amplification(),
        reject_activation_only_lease_check(),
        reject_post_mutation_budget_check(),
        reject_success_justifies_excess(),
        reject_compensation_deletes_harm(),
        reject_principal_only_causation(),
        reject_delegate_only_causation(),
        reject_same_artifact_same_authority(),
    )

    assert all(isinstance(item, CountermodelRejection) for item in rejections)
    assert len({item.countermodel for item in rejections}) == 15


def test_38_experiment_imports_no_package_or_previous_experiment() -> None:
    experiment_root = Path(records_module.__file__).parent
    forbidden_prefixes = (
        "arx_mentis",
        "experiments.euclid_i_1",
        "experiments.ars_astronomica_settlement",
        "experiments.ars_grammatica_reading",
        "experiments.ars_dialectica_verification",
        "experiments.virtual_mediation",
        "experiments.omen_attribution",
        "experiments.actualization",
        "experiments.symbolic_release",
        "experiments.stress_discharge",
        "experiments.probability_bias",
        "experiments.feedback_revision",
        "experiments.scoped_model_adoption",
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


def test_39_source_delegate_and_trace_are_immutable() -> None:
    session = contained_session()

    with pytest.raises(FrozenInstanceError):
        session.delegate.compiled = False  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        session.trace.actions = ()  # type: ignore[misc]


def test_40_environment_exposes_declared_compartment_structure() -> None:
    environment = initial_environment()

    assert tuple(item.compartment for item in environment.compartments) == (
        Compartment.NORTH,
        Compartment.CENTER,
        Compartment.SOUTH,
    )
    assert all(item.readable_records for item in environment.compartments)
    assert all(item.writable_records for item in environment.compartments)
    assert all(item.protected_records for item in environment.compartments)
    assert all(item.external_connections for item in environment.compartments)
