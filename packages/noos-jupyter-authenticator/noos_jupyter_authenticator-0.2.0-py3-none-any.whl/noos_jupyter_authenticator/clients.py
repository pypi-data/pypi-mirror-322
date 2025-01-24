from http import client as http_client
from typing import Any, Dict

from noos_pyk.clients import auth, json


class NoosGatewayAuth(auth.HTTPTokenAuth):
    """Authentication class for the Noos gateway REST API."""

    default_header = "Authorization"
    default_value = "Bearer"


class NoosGatewayClient(json.JSONClient, auth.AuthClient):
    """Client for the Noos gateway REST API."""

    default_auth_class = NoosGatewayAuth

    def whoami(self) -> Dict[str, Any]:
        """Return infos about the authenticated user."""
        return self.get(path="v1/accounts/whoami/", statuses=(http_client.OK,))
