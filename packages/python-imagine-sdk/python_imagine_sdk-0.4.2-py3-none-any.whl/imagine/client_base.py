from __future__ import annotations

import logging
import os
import posixpath

from typing import Any, Sequence

import orjson

import imagine

from imagine.constants import USER_AGENT_NAME
from imagine.logging import logger
from imagine.types.chat_completions import ChatMessage
from imagine.types.models import ModelType
from imagine.utils import env_var_to_bool


class ClientBase:
    _default_model = {
        ModelType.TEXT_TO_IMAGE: "sdxl-turbo",
        ModelType.TRANSLATE: "Helsinki-NLP/opus-mt-en-es",
        ModelType.LLM: "Llama-3.1-8B",
        ModelType.TRANSCRIBE: "whisper-tiny",
        ModelType.EMBEDDING: "BAAI/bge-large-en-v1.5",
        ModelType.RERANKER: "BAAI/bge-reranker-base",
    }
    _version = imagine.__version__
    _user_agent = f"{USER_AGENT_NAME}/{_version}"
    _logger = logger

    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        max_retries: int = 3,
        timeout: int = 120,
        proxy: str | None = None,
        debug: bool = False,
    ):
        self._max_retries = max_retries
        self._timeout = timeout

        api_key = api_key or os.environ.get("IMAGINE_API_KEY", None)

        if not api_key:
            raise ValueError(
                "API key must be provided. Please set the IMAGINE_API_KEY environment "
                "variable or pass it as the api_key input argument."
            )

        self._api_key = api_key

        endpoint = endpoint or os.environ.get("IMAGINE_API_ENDPOINT", None)

        if not endpoint:
            raise ValueError(
                "Server endpoint must be provided. Please set the IMAGINE_API_ENDPOINT environment "
                "variable or pass it as the endpoint input argument."
            )

        self._endpoint = endpoint

        self._proxy = proxy or os.environ.get("IMAGINE_API_PROXY", None)

        debug = debug or env_var_to_bool("IMAGINE_DEBUG")
        if debug:
            self._logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            self._logger.addHandler(handler)

    @property
    def default_model_tti(self) -> str:
        return self._default_model[ModelType.TEXT_TO_IMAGE]

    @property
    def default_model_translate(self) -> str:
        return self._default_model[ModelType.TRANSLATE]

    @property
    def default_model_llm(self) -> str:
        return self._default_model[ModelType.LLM]

    @property
    def default_model_transcribe(self) -> str:
        return self._default_model[ModelType.TRANSCRIBE]

    @property
    def default_model_embedding(self) -> str:
        return self._default_model[ModelType.EMBEDDING]

    @property
    def default_model_reranker(self) -> str:
        return self._default_model[ModelType.RERANKER]

    @staticmethod
    def _parse_messages_to_chat_message(
        messages: Sequence[ChatMessage | dict[str, str]],
    ) -> list[ChatMessage]:
        parsed_messages: list[ChatMessage] = []

        for message in messages:
            if isinstance(message, ChatMessage):
                parsed_messages.append(message)
            else:
                parsed_messages.append(ChatMessage(**message))

        return parsed_messages

    @staticmethod
    def _process_line(line: str) -> dict[str, Any] | None:
        if line.startswith("data: "):
            line = line[6:].strip()
            if line != "[DONE]":
                json_streamed_response: dict[str, Any] = orjson.loads(line)
                return json_streamed_response
        return None

    def _get_headers(
        self, accept_header: str, json_content: bool = False
    ) -> dict[str, str]:
        headers = {
            "Accept": accept_header,
            "User-Agent": self._user_agent,
            "Authorization": f"Bearer {self._api_key}",
        }
        if json_content:
            headers["Content-Type"] = "application/json"
        return headers

    def _get_url(self, path: str) -> str:
        return posixpath.join(self._endpoint, path)

    @staticmethod
    def _is_client_error(code: int) -> bool:
        return 400 <= code < 500

    @staticmethod
    def _is_server_error(code: int) -> bool:
        return code >= 500
