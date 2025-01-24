from typing import Any, Optional

from pydantic import ConfigDict, SecretStr, model_validator

from imagine import ImagineAsyncClient, ImagineClient


class BaseLangChainMixin:
    """This mixin adds base functionality common to all the LangChain classes."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: ImagineClient
    async_client: ImagineAsyncClient

    api_key: Optional[SecretStr] = None
    endpoint: Optional[str] = None
    max_retries: int = 5
    timeout: int = 120
    verify: bool = False

    @model_validator(mode="before")
    @classmethod
    def pre_root(cls, values: dict[str, Any]) -> dict[str, Any]:
        client_params = {
            "endpoint": values.pop("endpoint", None),
            "api_key": values.pop("api_key", None),
            "max_retries": values.pop("max_retries", None),
            "timeout": values.pop("timeout", None),
            "verify": values.pop("verify", None),
        }

        values["client"] = ImagineClient(**client_params)
        values["async_client"] = ImagineAsyncClient(**client_params)

        return values
