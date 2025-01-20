import pytest

from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.dai_engine_profile.config_editability import (
    ConfigEditability,
)
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile import (
    DAIEngineProfile,
)


@pytest.fixture(scope="function")
def dai_engine_profile_p1(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 1",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin", "super_admin"],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
        ),
        dai_engine_profile_id="p1",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p2(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 2",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
        ),
        dai_engine_profile_id="p2",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p3(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 3",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin", "super_admin"],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
        ),
        dai_engine_profile_id="p3",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p4(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 4",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            assigned_oidc_roles=[],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
        ),
        dai_engine_profile_id="p4",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p5(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 5",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            assigned_oidc_roles=[],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "bar"},
            base_configuration={"alice": "bob"},
        ),
        dai_engine_profile_id="p5",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)


@pytest.fixture(scope="function")
def dai_engine_profile_p6(dai_engine_profile_client_super_admin):
    created_profile = dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent="workspaces/global",
        dai_engine_profile=DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1", maximum="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="1", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            display_name="profile 6",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=False,
            assigned_oidc_roles=[],
            max_running_engines=10,
            max_non_interaction_duration="10m",
            max_unused_duration="10m",
            configuration_override={"foo": "new-bar"},
            base_configuration={"alice": "new-bob"},
        ),
        dai_engine_profile_id="p6",
    )
    name = created_profile.name

    yield created_profile

    dai_engine_profile_client_super_admin.delete_dai_engine_profile(name=name)
