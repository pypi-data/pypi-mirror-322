import abc
from typing import Any, Dict, TypeVar

OAUTH_TYPE_FIELD = "type"
OAUTH_KEY = "oauth"

OAuthType = TypeVar("OAuthType", bound="OAuth")


class OAuth(abc.ABC):
    """Interface for OAuth configuration."""

    @classmethod
    @abc.abstractmethod
    def from_config(cls: OAuthType, config: Dict[str, Any]) -> OAuthType:
        """Initializes a dataclass from the passed config.

        Args:
            config: (dict) The config from which to initialize.

        Returns:
            OAuth
        """
        ...

    @abc.abstractmethod
    def get_bearer_token(self) -> str:
        """Returns a bearer token.

        Bear token is used to authenticate requests to the Azure Oopen AI instance's API protected
        by the Gateway.
        """
        ...
