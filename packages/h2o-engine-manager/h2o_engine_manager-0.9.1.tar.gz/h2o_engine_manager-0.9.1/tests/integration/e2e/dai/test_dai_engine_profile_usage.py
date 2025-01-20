import datetime
import http

import pytest

from h2o_engine_manager.clients.dai_engine.profile_info import DAIEngineProfileInfo
from h2o_engine_manager.clients.dai_engine_profile.dai_engine_profile import (
    DAIEngineProfile,
)
from h2o_engine_manager.clients.exception import CustomApiException


@pytest.mark.timeout(60)
def test_dai_engine_profile_usage(dai_client, dai_admin_client, dai_engine_profile_p1):
    workspace_id = "687cc72b-8061-4e59-a866-5bcad26aa4b7"
    engine_id = "e1"

    # Regular user does not have matching OIDC roles -> cannot create engine with this profile.
    with pytest.raises(CustomApiException) as exc:
        dai_client.create_engine(
            workspace_id=workspace_id,
            engine_id=engine_id,
            profile=dai_engine_profile_p1.name,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST

    # Admin client has matching OIDC role -> can create engine with this profile.
    eng = dai_admin_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        profile=dai_engine_profile_p1.name,
    )

    try:
        assert eng.name == f"workspaces/{workspace_id}/daiEngines/e1"
        assert eng.profile == "workspaces/global/daiEngineProfiles/p1"

        original_profile = dai_engine_profile_p1
        assert_profile_equal_profile_info(profile=original_profile, profile_info=eng.profile_info)

        eng.pause()
        eng.wait()

        eng.resume()
        assert_profile_equal_profile_info(profile=original_profile, profile_info=eng.profile_info)
    finally:
        dai_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True
        )


def assert_profile_equal_profile_info(profile: DAIEngineProfile, profile_info: DAIEngineProfileInfo):
    assert profile.cpu_constraint == profile_info.cpu_constraint
    assert profile.gpu_constraint == profile_info.gpu_constraint
    assert profile.memory_bytes_constraint == profile_info.memory_bytes_constraint
    assert profile.storage_bytes_constraint == profile_info.storage_bytes_constraint
    assert profile.max_idle_duration_constraint == profile_info.max_idle_duration_constraint
    assert profile.max_running_duration_constraint == profile_info.max_running_duration_constraint
    assert profile.config_editability == profile_info.config_editability
    assert profile.name == profile_info.name
    assert profile.display_name == profile_info.display_name
    assert profile.priority == profile_info.priority
    assert profile.enabled == profile_info.enabled
    assert profile.assigned_oidc_roles_enabled == profile_info.assigned_oidc_roles_enabled
    assert profile.assigned_oidc_roles == profile_info.assigned_oidc_roles
    assert profile.max_running_engines == profile_info.max_running_engines
    assert profile.max_non_interaction_duration == profile_info.max_non_interaction_duration
    assert profile.max_unused_duration == profile_info.max_unused_duration
    assert profile.configuration_override == profile_info.configuration_override
    assert profile.base_configuration == profile_info.base_configuration
    assert profile.yaml_pod_template_spec == profile_info.yaml_pod_template_spec
    assert profile.yaml_gpu_tolerations == profile_info.yaml_gpu_tolerations
    assert profile.triton_enabled == profile_info.triton_enabled
    assert_equal_datetimes_up_to_seconds(profile.create_time, profile_info.create_time)
    assert_equal_datetimes_up_to_seconds(profile.update_time, profile_info.update_time)
    assert profile.creator == profile_info.creator
    assert profile.updater == profile_info.updater
    assert profile.creator_display_name == profile_info.creator_display_name
    assert profile.updater_display_name == profile_info.updater_display_name


def assert_equal_datetimes_up_to_seconds(dt1: datetime.datetime, dt2: datetime.datetime):
    dt1_trimmed = None
    dt2_trimmed = None

    if dt1 is not None:
        dt1_trimmed = dt1.replace(microsecond=0)

    if dt2 is not None:
        dt2_trimmed = dt2.replace(microsecond=0)

    assert dt1_trimmed == dt2_trimmed
