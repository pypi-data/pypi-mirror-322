from typing import Optional

from h2o_engine_manager.clients.auth.token_api_client import TokenApiClient
from h2o_engine_manager.clients.connection_config import get_connection
from h2o_engine_manager.gen.api.dai_engine_constraint_set_service_api import (
    DAIEngineConstraintSetServiceApi,
)
from h2o_engine_manager.gen.configuration import Configuration
from h2o_engine_manager.gen.model.v1_dai_engine_constraint_set import (
    V1DAIEngineConstraintSet,
)


class DAIEngineConstraintSetClient:
    """DAIEngineConstraintSetClient manages DAIEngineConstraintSets."""

    def __init__(
        self,
        url: str,
        platform_token: str,
        platform_oidc_url: str,
        platform_oidc_client_id: str,
        platform_oidc_client_secret: Optional[str] = None,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes DAIEngineConstraintSetClient.

        Args:
            url (str): URL of AI Engine Manager Gateway.
            platform_token (str): H2O.ai platform token.
            platform_oidc_url (str): Base URL of the platform_token OIDC issuer.
            platform_oidc_client_id (str): OIDC Client ID associated with the platform_token.
            platform_oidc_client_secret (str, optional): Optional OIDC Client Secret that issued the 'platform_token'.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        cfg = get_connection(
            aiem_url=url,
            refresh_token=platform_token,
            issuer_url=platform_oidc_url,
            client_id=platform_oidc_client_id,
            client_secret=platform_oidc_client_secret,
            verify_ssl=verify_ssl,
            ssl_ca_cert=ssl_ca_cert,
        )

        engine_cfg = Configuration(host=url)
        engine_cfg.verify_ssl = verify_ssl
        engine_cfg.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
            engine_cfg, cfg.token_provider
        ) as engine_service_api_client:
            self.service_api = DAIEngineConstraintSetServiceApi(
                engine_service_api_client
            )

    def get_constraint_set(self, workspace_id: str) -> V1DAIEngineConstraintSet:
        return self.service_api.d_ai_engine_constraint_set_service_get_dai_engine_constraint_set(
            name_1=f"workspaces/{workspace_id}/daiEngineConstraintSet"
        ).dai_engine_constraint_set
