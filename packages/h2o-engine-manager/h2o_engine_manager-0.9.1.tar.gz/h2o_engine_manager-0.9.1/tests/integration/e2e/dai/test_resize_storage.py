import http

import pytest

from h2o_engine_manager.clients.exception import CustomApiException
from tests.integration.api.dai.create_dai_request import CreateDAIEngineRequest
from tests.integration.api.dai.create_dai_request import create_dai_from_request


@pytest.mark.timeout(100)
@pytest.mark.skip(reason="storage class in local cluster does not support resizing")
def test_resize_storage(dai_client):
    workspace_id = "61ed1ec2-8d94-4ecd-8dbc-4b8e309d5b12"
    engine_id = "resize"

    req = CreateDAIEngineRequest(
        workspace_id=workspace_id,
        engine_id=engine_id,
        memory_bytes="8Gi",
        storage_bytes="8Gi",
        version="1.10.5"
    )

    eng = create_dai_from_request(dai_client, req)
    try:
        eng.wait()
        eng.pause()
        eng.wait()

        # Cannot exceed the maximum storage size.
        with pytest.raises(CustomApiException) as exc:
            eng.resize_storage(new_storage="2000Gi")
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST

        # Resize storage
        eng.resize_storage(new_storage="9Gi")
        assert eng.storage_bytes == "9Gi"

        eng.resume()
        eng.wait()
        eng.connect()

        assert eng.storage_resizing is False

    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name_1=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
