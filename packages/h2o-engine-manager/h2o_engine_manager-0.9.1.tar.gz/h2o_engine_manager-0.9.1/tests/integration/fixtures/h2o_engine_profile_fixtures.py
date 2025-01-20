import pytest

from h2o_engine_manager.clients.constraint.profile_constraint_duration import (
    ProfileConstraintDuration,
)
from h2o_engine_manager.clients.constraint.profile_constraint_numeric import (
    ProfileConstraintNumeric,
)
from h2o_engine_manager.clients.h2o_engine_profile.h2o_engine_profile import (
    H2OEngineProfile,
)


@pytest.fixture(scope="function")
def h2o_engine_profile_p1(h2o_engine_profile_client_super_admin):
    created_profile = h2o_engine_profile_client_super_admin.create_h2o_engine_profile(
        parent="workspaces/global",
        h2o_engine_profile=H2OEngineProfile(
            node_count_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="20Mi", default="20Mi"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="5m", default="4h", maximum="200h"),
            display_name="profile 1",
            priority=1,
            enabled=True,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin", "super_admin"],
            max_running_engines=10,
        ),
        h2o_engine_profile_id="p1",
    )
    name = created_profile.name

    yield created_profile

    h2o_engine_profile_client_super_admin.delete_h2o_engine_profile(name=name)
