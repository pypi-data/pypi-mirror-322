from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from azure.identity import ClientSecretCredential

from rasa.shared.providers._configs.oauth_config import OAuth


@dataclass
class AzureEntraIDClientCreds(OAuth):
    client_id: str
    client_secret: str
    tenant_id: str
    scopes: List[str] = field(default_factory=list)

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> AzureEntraIDClientCreds:
        scopes = config.get("scopes")
        if isinstance(scopes, str):
            scopes = [scopes]

        return cls(
            client_id=config.get("client_id"),
            client_secret=config.get("client_secret"),
            tenant_id=config.get("tenant_id"),
            scopes=scopes,
        )

    def get_bearer_token(self) -> str:
        return (
            ClientSecretCredential(
                client_id=self.client_id,
                client_secret=self.client_secret,
                tenant_id=self.tenant_id,
            )
            .get_token(*self.scopes)
            .token
        )
