import http
import re

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
from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.conftest import GLOBAL_WORKSPACE


def test_get_dai_engine_profile(
    dai_engine_profile_client_super_admin,
    dai_engine_profile_client_admin,
    dai_engine_profile_client,
    delete_all_dai_engine_profiles_before_after,
):
    dai_engine_profile_client_super_admin.create_dai_engine_profile(
        parent=GLOBAL_WORKSPACE,
        dai_engine_profile=(DAIEngineProfile(
            cpu_constraint=ProfileConstraintNumeric(minimum="1", default="1"),
            gpu_constraint=ProfileConstraintNumeric(minimum="0", default="0", maximum="10", cumulative_maximum="100"),
            memory_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            storage_bytes_constraint=ProfileConstraintNumeric(minimum="100", default="100"),
            max_idle_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s"),
            max_running_duration_constraint=ProfileConstraintDuration(minimum="100s", default="200s", maximum="400s"),
            config_editability=ConfigEditability.CONFIG_EDITABILITY_FULL,
            assigned_oidc_roles_enabled=True,
            assigned_oidc_roles=["admin"]
        )),
        dai_engine_profile_id="p1",
    )

    # Roles assigned to users are defined in helm/ai-engine-manager/templates/secret-keycloak.yaml.
    # test-super-admin has roles ["super_admin", "offline_access", "default-roles-hac-dev", "uma_authorization"]
    # test-admin has roles ["admin", "offline_access", "default-roles-hac-dev", "uma_authorization"]
    # test-user has roles ["offline_access", "default-roles-hac-dev", "uma_authorization"]

    # Super admin can get any profile regardless profile's assigned_oidc_roles.
    profile_by_super_admin = dai_engine_profile_client_super_admin.get_dai_engine_profile(
        name="workspaces/global/daiEngineProfiles/p1"
    )

    # Admin can get this profile because has assigned role.
    profile_by_admin = dai_engine_profile_client_admin.get_dai_engine_profile(
        name="workspaces/global/daiEngineProfiles/p1"
    )

    # User cannot get profile because does not have assigned role "admin" and is not super_admin.
    # Use gets NOT FOUND (user will not know that profile exists).
    with pytest.raises(CustomApiException) as exc:
        dai_engine_profile_client.get_dai_engine_profile(name="workspaces/global/daiEngineProfiles/p1")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    # Both admin and superAdmin should get the same response.
    assert profile_by_admin == profile_by_super_admin
    # Check that Get method returns correct data.
    assert profile_by_admin.cpu_constraint == ProfileConstraintNumeric(minimum="1", default="1")
    assert profile_by_admin.gpu_constraint == ProfileConstraintNumeric(
        minimum="0", default="0", maximum="10", cumulative_maximum="100"
    )
    assert profile_by_admin.memory_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert profile_by_admin.storage_bytes_constraint == ProfileConstraintNumeric(minimum="100", default="100")
    assert profile_by_admin.max_idle_duration_constraint == ProfileConstraintDuration(minimum="100s", default="200s")
    assert profile_by_admin.max_running_duration_constraint == ProfileConstraintDuration(
        minimum="100s", default="200s", maximum="400s"
    )
    assert profile_by_admin.config_editability == ConfigEditability.CONFIG_EDITABILITY_FULL
    assert profile_by_admin.name == "workspaces/global/daiEngineProfiles/p1"
    assert profile_by_admin.display_name == ""
    assert profile_by_admin.priority == 0
    assert profile_by_admin.enabled is True
    assert profile_by_admin.assigned_oidc_roles_enabled is True
    assert profile_by_admin.assigned_oidc_roles == ["admin"]
    assert profile_by_admin.max_running_engines is None
    assert profile_by_admin.max_non_interaction_duration is None
    assert profile_by_admin.max_unused_duration is None
    assert profile_by_admin.configuration_override == {}
    assert profile_by_admin.base_configuration == {}
    assert profile_by_admin.yaml_pod_template_spec == ""
    assert profile_by_admin.yaml_gpu_tolerations == ""
    assert profile_by_admin.triton_enabled is False
    assert profile_by_admin.create_time is not None
    assert profile_by_admin.update_time is None
    assert re.match(r"^users/.+$", profile_by_admin.creator)
    assert profile_by_admin.updater == ""
    assert profile_by_admin.creator_display_name == "test-super-admin"
    assert profile_by_admin.updater_display_name == ""
