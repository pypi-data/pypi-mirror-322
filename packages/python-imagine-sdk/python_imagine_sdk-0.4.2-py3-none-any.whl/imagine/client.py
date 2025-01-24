from __future__ import annotations

import datetime as dt
import posixpath
import time

from http import HTTPStatus
from json import JSONDecodeError
from typing import Any, BinaryIO, Iterable, Iterator, Sequence

from httpx import Client, ConnectError, HTTPTransport, RequestError, Response

from imagine.client_base import ClientBase
from imagine.constants import RETRY_STATUS_CODES
from imagine.exceptions import (
    ImagineAPIException,
    ImagineAPIStatusException,
    ImagineAPITooManyRequestsException,
    ImagineConnectionException,
    ImagineException,
)
from imagine.types.chat_completions import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
    ChatMessage,
)
from imagine.types.completions import (
    CompletionRequest,
    CompletionResponse,
    CompletionStreamResponse,
)
from imagine.types.embeddings import EmbeddingRequest, EmbeddingResponse
from imagine.types.healthcheck import HealthResponse, PingResponse
from imagine.types.images import ImageRequest, ImageResponse
from imagine.types.models import ModelType
from imagine.types.reranker import ReRankerRequest, ReRankerResponse
from imagine.types.transcribe import TranscribeResponse
from imagine.types.translate import TranslateResponse
from imagine.types.usage import UsageResponse
from imagine.utils import URLLib3Transport


class ImagineClient(ClientBase):
    """
    Synchronous Imagine client. Provides methods for communicating with the Imagine API.
    """

    def __init__(
        self,
        endpoint: str | None = None,
        api_key: str | None = None,
        max_retries: int = 3,
        timeout: int = 60,
        verify: bool | str = False,
        proxy: str | None = None,
        debug: bool = False,
        ctx: str | None = None,
    ):
        """
        The constructor for ImagineClient class.

        :param endpoint: Endpoint of the Imagine API. It defaults to the production endpoint of the Imagine API.
        :param api_key: API key to use on the requests to the Imagine API. If not set, it will load it from the environment variable IMAGINE_API_KEY. If that's not set either, it will raise a ValueError.
        :param max_retries: Maximum number of retries before giving up.
        :param timeout: Timeout in seconds.
        :param verify: Whether to verify SSL certificate.
        :param debug: Whether to enable debug mode. If not set, it will load it from the environment variable IMAGINE_DEBUG. If that's not set either, debug mode is disabled.
        """

        super().__init__(endpoint, api_key, max_retries, timeout, proxy, debug)

        if ctx == "browser":
            self._transport = URLLib3Transport()
        else:
            self._transport = HTTPTransport(
                retries=self._max_retries, verify=verify, proxy=self._proxy
            )

        self._client: Client = Client(
            verify=verify,
            follow_redirects=True,
            timeout=self._timeout,
            transport=self._transport,
            proxy=self._proxy,
        )

    def __del__(self) -> None:
        try:
            self._client.close()
        except AttributeError:
            pass

    def _check_response_status_codes(self, response: Response) -> None:
        status_code = response.status_code
        if status_code in RETRY_STATUS_CODES:
            if response.stream:
                response.read()
            raise ImagineAPIStatusException.from_response(
                response,
                message=f"Status: {status_code}. Message: {response.text}",
            )
        elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise ImagineAPITooManyRequestsException.from_response(
                response,
                message=f"Status: {status_code}. Message: {response.text}",
            )
        elif self._is_client_error(status_code):
            if response.stream:
                response.read()
            raise ImagineAPIException.from_response(
                response,
                message=f"Status: {status_code}. Message: {response.text}",
            )
        elif self._is_server_error(status_code):
            if response.stream:
                response.read()
            raise ImagineException(
                message=f"Status: {status_code}. Message: {response.text}",
            )

    def _check_streaming_response(self, response: Response) -> None:
        self._check_response_status_codes(response)

    def _check_response(self, response: Response) -> dict[str, Any]:
        self._check_response_status_codes(response)

        json_response: dict[str, Any] = response.json()
        return json_response

    def _stream_request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None,
        attempt: int = 1,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Iterator[dict[str, Any]]:
        headers = self._get_headers("text/event-stream", json_content=bool(json))
        url = self._get_url(path)

        self._logger.debug(f"Sending request: {method} {url} {json}")

        response: Response

        try:
            with self._client.stream(
                method,
                url,
                headers=headers,
                json=json,
                data=data,
                **kwargs,
            ) as response:
                self._check_streaming_response(response)

                for line in response.iter_lines():
                    json_streamed_response = self._process_line(line)
                    if json_streamed_response:
                        yield json_streamed_response
        except ConnectError as e:
            raise ImagineConnectionException(str(e)) from e
        except RequestError as e:
            raise ImagineException(
                f"Unexpected exception ({e.__class__.__name__}): {e}"
            ) from e
        except JSONDecodeError as e:
            raise ImagineAPIException.from_response(
                response,
                message=f"Failed to decode json body: {response.text}",
            ) from e
        except ImagineAPIStatusException as e:
            attempt += 1
            if attempt > self._max_retries:
                raise ImagineAPIStatusException.from_response(
                    response, message=str(e)
                ) from e
            backoff = 2.0**attempt  # exponential backoff
            self._logger.debug(f"Retrying in {backoff} seconds... attempt #{attempt}")
            time.sleep(backoff)

            # Retry as a generator
            for r in self._stream_request(method, path, json, attempt=attempt):
                yield r

    def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        attempt: int = 1,
        data: dict[str, Any] | None = None,
        files: dict[str, BinaryIO] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | list:
        headers = self._get_headers("application/json", json_content=bool(json))
        url = self._get_url(path)

        if json:
            self._logger.debug(f"Sending request: {method} {url} {json}")
        elif data:
            self._logger.debug(f"Sending request: {method} {url} {data}")
        else:
            self._logger.debug(f"Sending request: {method} {url}")

        response: Response

        try:
            response = self._client.request(
                method,
                url,
                headers=headers,
                json=json,
                data=data,
                files=files,
                **kwargs,
            )
        except ConnectError as e:
            raise ImagineConnectionException(str(e)) from e
        except RequestError as e:
            raise ImagineException(
                f"Unexpected exception ({e.__class__.__name__}): {e}"
            ) from e

        try:
            return self._check_response(response)
        except JSONDecodeError as e:
            raise ImagineAPIException.from_response(
                response,
                message=f"Failed to decode json body: {response.text}",
            ) from e
        except ImagineAPIStatusException as e:
            attempt += 1
            if attempt > self._max_retries:
                raise ImagineAPIStatusException.from_response(
                    response, message=str(e)
                ) from e
            backoff = 2.0**attempt  # exponential backoff
            self._logger.debug(f"Retrying in {backoff} seconds... attempt #{attempt}")
            time.sleep(backoff)

            return self._request(method, path, json, attempt=attempt)

    def get_available_models_by_type(
        self, model_type: ModelType | None = None
    ) -> dict[ModelType, list[str]]:
        """
        Returns a mapping of available models by model type.

        :param model_type: :class:`imagine.ModelType` Filter models by model type.

        :raises: ImagineException :class:`imagine.ImagineException`

        :return: Available models grouped by model type.
        """
        response = self._request(
            "get",
            "models",
            {},
            params={"model_type": model_type.value} if model_type else None,
        )
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        if model_type:
            return {model_type: response.get(model_type, [])}

        model_types = [member.value for member in ModelType]
        return {
            ModelType[type_.upper()]: models
            for type_, models in response.items()
            if type_ in model_types
        }

    def get_available_models(self, model_type: ModelType | None = None) -> list[str]:
        """
        Returns a list of available models.

        :param model_type: Filter models by model type.

        :raises: ImagineException :class:`imagine.ImagineException`

        :return: Available models.
        """
        response = self.get_available_models_by_type(model_type)
        return [model for models in response.values() for model in models]

    def ping(self) -> PingResponse:
        """
        Ping the API to check if the Imagine server is reachable.

        :raises: ImagineException :class:`imagine.ImagineException`

        :return: A PingResponse object containing status of the server.
        """
        response = self._request("get", "ping", {})
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return PingResponse(**response)

    def health_check(self) -> HealthResponse:
        """
        Check the health of the server, including databases ands models.

        :raises: ImagineException :class:`imagine.ImagineException`

        :return: A HealthResponse object containing status of the server.
        """

        response = self._request("get", "health", {})
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return HealthResponse(**response)

    def usage(
        self,
        aggregation_duration: str | None = None,
        since: dt.datetime | None = None,
        until: dt.datetime | None = None,
        model: str | None = None,
    ) -> UsageResponse:
        """
        Report usage statistics for the user.

        :param aggregation_duration:
        :param since: Since date to report usage statistics for.
        :param until: Until date to report usage statistics for.
        :param model: Filter usage statistics by model type.

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            The usage report as a UsageRespone object

        """

        params = {}

        if aggregation_duration is not None:
            params["aggregation_duration"] = aggregation_duration
        if since is not None:
            params["from"] = str(since)
        if until is not None:
            params["to"] = str(until)
        if model is not None:
            params["model"] = model

        response = self._request("get", "usage", {}, params=params)
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return UsageResponse(**response)

    def embeddings(
        self, texts: str | list[str], model: str | None = None
    ) -> EmbeddingResponse:
        """An embeddings endpoint that returns embeddings for a single text

        :param text: The text to embed
        :param model: The embedding model to use

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            EmbeddingResponse: A response object containing the embeddings.
        """
        if not model:
            model = self.default_model_embedding
        request = {"model": model, "input": texts}
        response = self._request("post", "embeddings", request)
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return EmbeddingResponse(**response)

    # add documents, query specifications | limits
    def reranker(
        self,
        query: str,
        documents: list[str],
        model: str | None = None,
        top_n: int | None = None,
        return_documents: bool | None = None,
    ) -> ReRankerResponse:
        """Reranker endpoint receives as input a query, a list of documents, and other arguments such as the model name, and returns a response containing the reranking results.

        :param query: The query as a string
        :param documents: The documents to be reranked as a list of strings.
        :param model: The reranker model to use.
        :param top_n: The number of most relevant documents to return. If not specified, the reranking results of all documents will be returned.
        :param return_documents: Whether to return the documents in the response. Defaults to false

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            ReRankerResponse object: A response object containing the Similarity Score.

        """
        if not model:
            model = self.default_model_reranker

        request_body = ReRankerRequest(
            query=query,
            documents=documents,
            top_n=top_n,
            model=model,
            return_documents=return_documents,
        ).model_dump(exclude_none=True)

        response = self._request("post", "reranker", request_body)
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return ReRankerResponse(**response)

    def translate(
        self,
        prompt: str,
        model: str,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        repetition_penalty: float | None = None,
        stop: list[str] | None = None,
        max_seconds: int | None = None,
        ignore_eos: bool | None = None,
        skip_special_tokens: bool | None = None,
        stop_token_ids: list[list[int]] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
    ) -> TranslateResponse:
        """Invokes translate endpoint that returns TranslateResponse for a given prompt

        :param prompt: prompt text that needs to be translated
        :param model: the model to use for translation
        :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim, defaults to None
        :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics, defaults to None
        :param repetition_penalty: Float that penalizes new tokens based on whether they appear in the prompt and the generated text so far. Values > 1 encourage the model to use new tokens, while values < 1 encourage the model to repeat tokens., defaults to None
        :param stop:  Sequences where the API will stop generating further tokens. The returned text will contain the stop sequence., defaults to None
        :param max_seconds: TBD, defaults to None
        :param ignore_eos: Whether to ignore the EOS token and continue generating tokens after the EOS token is generated., defaults to None
        :param skip_special_tokens: Whether to skip special tokens in the output., defaults to None
        :param stop_token_ids: List of tokens that stop the generation when they are generated. The returned output will contain the stop tokens unless the stop tokens are special tokens., defaults to None
        :param max_tokens: The maximum number of tokens that can be generated in translation, defaults to None
        :param temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic., defaults to None
        :param top_k: Integer that controls the number of top tokens to consider. Set to -1 to consider all tokens., defaults to None
        :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both., defaults to None

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            TranslateResponse object

        """

        request_body = CompletionRequest(
            prompt=prompt,
            model=model,
            stream=False,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repetition_penalty=repetition_penalty,
            stop=stop,
            max_seconds=max_seconds,
            ignore_eos=ignore_eos,
            skip_special_tokens=skip_special_tokens,
            stop_token_ids=stop_token_ids,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        ).model_dump(exclude_none=True)

        response = self._request("post", "translate", request_body)
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return TranslateResponse(**response)

    def completion(
        self,
        prompt: str,
        model: str | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        repetition_penalty: float | None = None,
        stop: list[str] | None = None,
        max_seconds: int | None = None,
        ignore_eos: bool | None = None,
        skip_special_tokens: bool | None = None,
        stop_token_ids: list[list[int]] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
    ) -> CompletionResponse:
        """Invokes completions endpoint non-streaming version that returns CompletionResponse for a given prompt

        :param prompt: prompt text for which completion needs to be generated
        :param model: the model to use for completion
        :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim, defaults to None
        :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics, defaults to None
        :param repetition_penalty: Float that penalizes new tokens based on whether they appear in the prompt and the generated text so far. Values > 1 encourage the model to use new tokens, while values < 1 encourage the model to repeat tokens., defaults to None
        :param stop:  Sequences where the API will stop generating further tokens. The returned text will contain the stop sequence., defaults to None
        :param max_seconds: TBD, defaults to None
        :param ignore_eos: Whether to ignore the EOS token and continue generating tokens after the EOS token is generated., defaults to None
        :param skip_special_tokens: Whether to skip special tokens in the output., defaults to None
        :param stop_token_ids: List of tokens that stop the generation when they are generated. The returned output will contain the stop tokens unless the stop tokens are special tokens., defaults to None
        :param max_tokens: The maximum number of tokens that can be generated in translation, defaults to None
        :param temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic., defaults to None
        :param top_k: Integer that controls the number of top tokens to consider. Set to -1 to consider all tokens., defaults to None
        :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both., defaults to None

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            CompletionResponse object

        """
        if not model:
            model = self.default_model_llm

        request_body = CompletionRequest(
            prompt=prompt,
            model=model,
            stream=False,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repetition_penalty=repetition_penalty,
            stop=stop,
            max_seconds=max_seconds,
            ignore_eos=ignore_eos,
            skip_special_tokens=skip_special_tokens,
            stop_token_ids=stop_token_ids,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        ).model_dump(exclude_none=True)

        response = self._request("post", "completions", request_body)
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return CompletionResponse(**response)

    def completion_stream(
        self,
        prompt: str,
        model: str | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        repetition_penalty: float | None = None,
        stop: list[str] | None = None,
        max_seconds: int | None = None,
        ignore_eos: bool | None = None,
        skip_special_tokens: bool | None = None,
        stop_token_ids: list[list[int]] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
    ) -> Iterable[CompletionStreamResponse]:
        """Invokes completions endpoint streaming version that returns CompletionResponse for a given prompt

        :param prompt: prompt text for which completion needs to be generated
        :param model: the model to use for completion
        :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim, defaults to None
        :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics, defaults to None
        :param repetition_penalty: Float that penalizes new tokens based on whether they appear in the prompt and the generated text so far. Values > 1 encourage the model to use new tokens, while values < 1 encourage the model to repeat tokens., defaults to None
        :param stop:  Sequences where the API will stop generating further tokens. The returned text will contain the stop sequence., defaults to None
        :param max_seconds: TBD, defaults to None
        :param ignore_eos: Whether to ignore the EOS token and continue generating tokens after the EOS token is generated., defaults to None
        :param skip_special_tokens: Whether to skip special tokens in the output., defaults to None
        :param stop_token_ids: List of tokens that stop the generation when they are generated. The returned output will contain the stop tokens unless the stop tokens are special tokens., defaults to None
        :param max_tokens: The maximum number of tokens that can be generated in translation, defaults to None
        :param temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic., defaults to None
        :param top_k: Integer that controls the number of top tokens to consider. Set to -1 to consider all tokens., defaults to None
        :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both., defaults to None

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            CompletionStreamResponse object

        """
        if not model:
            model = self.default_model_llm

        request_body = CompletionRequest(
            prompt=prompt,
            model=model,
            stream=True,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repetition_penalty=repetition_penalty,
            stop=stop,
            max_seconds=max_seconds,
            ignore_eos=ignore_eos,
            skip_special_tokens=skip_special_tokens,
            stop_token_ids=stop_token_ids,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        ).model_dump(exclude_none=True)

        response = self._stream_request("post", "completions", request_body)

        for json_streamed_response in response:
            yield CompletionStreamResponse(**json_streamed_response)

    def chat(
        self,
        messages: Sequence[ChatMessage | dict[str, str]],
        model: str | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        repetition_penalty: float | None = None,
        stop: list[str] | None = None,
        max_seconds: int | None = None,
        ignore_eos: bool | None = None,
        skip_special_tokens: bool | None = None,
        stop_token_ids: list[list[int]] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
        tools: list[dict[str, str | dict[str, Any]]] | None = None,
    ) -> ChatCompletionResponse:
        """Invokes chat endpoint non-streaming version that returns ChatCompletionResponse for a given prompt

        :param messages: A list of chat-messages comprising the conversation so far
        :param model: the model to use for chat
        :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim, defaults to None
        :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics, defaults to None
        :param repetition_penalty: Float that penalizes new tokens based on whether they appear in the prompt and the generated text so far. Values > 1 encourage the model to use new tokens, while values < 1 encourage the model to repeat tokens., defaults to None
        :param stop:  Sequences where the API will stop generating further tokens. The returned text will contain the stop sequence., defaults to None
        :param max_seconds: TBD, defaults to None
        :param ignore_eos: Whether to ignore the EOS token and continue generating tokens after the EOS token is generated., defaults to None
        :param skip_special_tokens: Whether to skip special tokens in the output., defaults to None
        :param stop_token_ids: List of tokens that stop the generation when they are generated. The returned output will contain the stop tokens unless the stop tokens are special tokens., defaults to None
        :param max_tokens: The maximum number of tokens that can be generated in translation, defaults to None
        :param temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic., defaults to None
        :param top_k: Integer that controls the number of top tokens to consider. Set to -1 to consider all tokens., defaults to None
        :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both., defaults to None
        :param tools: A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for.


        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            ChatCompletionResponse

        """
        if not model:
            model = self.default_model_llm

        parsed_messages: list[ChatMessage] = self._parse_messages_to_chat_message(
            messages=messages
        )

        request_body = ChatCompletionRequest(
            messages=parsed_messages,
            model=model,
            stream=False,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repetition_penalty=repetition_penalty,
            stop=stop,
            max_seconds=max_seconds,
            ignore_eos=ignore_eos,
            skip_special_tokens=skip_special_tokens,
            stop_token_ids=stop_token_ids,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            tools=tools,
        ).model_dump(exclude_none=True)

        response = self._request("post", "chat/completions", request_body)
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return ChatCompletionResponse(**response)

    def chat_stream(
        self,
        messages: Sequence[ChatMessage | dict[str, str]],
        model: str | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        repetition_penalty: float | None = None,
        stop: list[str] | None = None,
        max_seconds: int | None = None,
        ignore_eos: bool | None = None,
        skip_special_tokens: bool | None = None,
        stop_token_ids: list[list[int]] | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_k: int | None = None,
        top_p: float | None = None,
    ) -> Iterable[ChatCompletionStreamResponse]:
        """Invokes chat endpoint streaming version that returns Iterable ChatCompletionStreamResponse for a given prompt

        :param messages: A list of chat-messages comprising the conversation so far
        :param model: the model to use for chat
        :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim, defaults to None
        :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics, defaults to None
        :param repetition_penalty: Float that penalizes new tokens based on whether they appear in the prompt and the generated text so far. Values > 1 encourage the model to use new tokens, while values < 1 encourage the model to repeat tokens., defaults to None
        :param stop:  Sequences where the API will stop generating further tokens. The returned text will contain the stop sequence., defaults to None
        :param max_seconds: TBD, defaults to None
        :param ignore_eos: Whether to ignore the EOS token and continue generating tokens after the EOS token is generated., defaults to None
        :param skip_special_tokens: Whether to skip special tokens in the output., defaults to None
        :param stop_token_ids: List of tokens that stop the generation when they are generated. The returned output will contain the stop tokens unless the stop tokens are special tokens., defaults to None
        :param max_tokens: The maximum number of tokens that can be generated in translation, defaults to None
        :param temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic., defaults to None
        :param top_k: Integer that controls the number of top tokens to consider. Set to -1 to consider all tokens., defaults to None
        :param top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both., defaults to None

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            ChatCompletionStreamResponse

        """
        if not model:
            model = self.default_model_llm

        parsed_messages = self._parse_messages_to_chat_message(messages=messages)

        request_body = ChatCompletionRequest(
            messages=parsed_messages,
            model=model,
            stream=True,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repetition_penalty=repetition_penalty,
            stop=stop,
            max_seconds=max_seconds,
            ignore_eos=ignore_eos,
            skip_special_tokens=skip_special_tokens,
            stop_token_ids=stop_token_ids,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        ).model_dump(exclude_none=True)

        response = self._stream_request("post", "chat/completions", request_body)

        for json_streamed_response in response:
            yield ChatCompletionStreamResponse(**json_streamed_response)

    def images_generate(
        self,
        prompt: str,
        model: str | None = None,
        negative_prompt: str | None = "blurry",
        seed: int | None = 27,
        seed_increment: int | None = 100,
        n: int | None = 1,
        num_inference_steps: int | None = 20,
        size: str | None = "512x512",
        guidance_scale: float | None = 6.5,
        cache_interval: int | None = None,
        response_format: str | None = "b64_json",
    ) -> ImageResponse:
        """Invokes images generate endpoint non-streaming version and returns an ImageResponse object

        :param prompt: The prompt to guide the image generation
        :param model: The model to be used for generation, defaults to None
        :param negative_prompt: Characteristics to avoid in the image being generated , defaults to "blurry"
        :param seed: The initial value used to generate random numbers. Set a unique seed for reproducible image results., defaults to 27
        :param seed_increment: The amount by which the seed value increases with each iteration. Adjust this to create a series of visually consistent, yet unique images, defaults to 100
        :param n: Number of images to be generated, defaults to 1
        :param num_inference_steps: — The total inference steps taken during image generation. More steps usually lead to a higher quality image at the expense of slower inference., defaults to 20
        :param size: The width x height in pixels of the generated image. defaults to 512x512
        :param guidance_scale: Higher guidance scale encourages to generate images that are closely linked to the text prompt, usually at the expense of lower image quality., defaults to 6.5
        :param cache_interval: _description_, defaults to None
        :param response_format: "url" or "b64_json", defaults to "b64_json"
        :raises ImagineException: :class:`imagine.ImagineException`
        :return: ImageResponse object
        """

        if not model:
            model = self.default_model_tti

        request_body = ImageRequest(
            prompt=prompt,
            model=model,
            stream=False,
            n=n,
            num_inference_steps=num_inference_steps,
            size=size,
            negative_prompt=negative_prompt,
            seed=seed,
            seed_increment=seed_increment,
            guidance_scale=guidance_scale,
            cache_interval=cache_interval,
            response_format=response_format,
        ).model_dump(exclude_none=True)

        response = self._request("post", "images/generations", request_body)
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Invalid response type")
        if response_format == "url":
            for d in response["data"]:
                d["url"] = f"{posixpath.dirname(self._endpoint)}{d['url']}"
        return ImageResponse(**response)

    def images_generate_stream(
        self,
        prompt: str,
        model: str | None = None,
        negative_prompt: str | None = "blurry",
        seed: int | None = 27,
        seed_increment: int | None = 100,
        n: int | None = 1,
        num_inference_steps: int | None = 20,
        size: str | None = "512x512",
        guidance_scale: float | None = 6.5,
        cache_interval: int | None = None,
        response_format: str | None = "b64_json",
    ) -> Iterable[ImageResponse]:
        """Invokes images generate endpoint streaming version and returns an Iterable ImageResponse object

        :param prompt: The prompt to guide the image generation
        :param model: The model to be used for generation, defaults to None
        :param negative_prompt: Characteristics to avoid in the image being generated , defaults to "blurry"
        :param seed: The initial value used to generate random numbers. Set a unique seed for reproducible image results., defaults to 27
        :param seed_increment: The amount by which the seed value increases with each iteration. Adjust this to create a series of visually consistent, yet unique images, defaults to 100
        :param n: Number of images to be generated, defaults to 1
        :param num_inference_steps: — The total inference steps taken during image generation. More steps usually lead to a higher quality image at the expense of slower inference., defaults to 20
        :param size: The width x height in pixels of the generated image. defaults to 512x512
        :param guidance_scale: Higher guidance scale encourages to generate images that are closely linked to the text prompt, usually at the expense of lower image quality., defaults to 6.5
        :param cache_interval: _description_, defaults to None
        :param response_format: "url" or "b64_json", defaults to "b64_json"
        :raises ImagineException: :class:`imagine.ImagineException`
        :return: ImageResponse object
        """

        if not model:
            model = self.default_model_tti

        request_body = ImageRequest(
            prompt=prompt,
            model=model,
            stream=True,
            n=n,
            num_inference_steps=num_inference_steps,
            size=size,
            negative_prompt=negative_prompt,
            seed=seed,
            seed_increment=seed_increment,
            guidance_scale=guidance_scale,
            cache_interval=cache_interval,
            response_format=response_format,
        ).model_dump(exclude_none=True)

        response = self._stream_request("post", "images/generations", request_body)

        for json_streamed_response in response:
            # see how to handle the load_balancer case
            if response_format == "url":
                for d in json_streamed_response["data"]:
                    d["url"] = f"{posixpath.dirname(self._endpoint)}{d['url']}"

            yield ImageResponse(**json_streamed_response)

    def get_reranker_history(
        self, max_items: int = 1
    ) -> list[list[ReRankerResponse | ReRankerRequest]]:
        """
        Returns a list of ReRanker response, request pairs made by the user.

        :param max_items: The number of items to retrieve

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            Returns a list of ReRanker response, request pairs made by the user.
        """
        response = self._request("get", "reranker", {}, params={"max_items": max_items})
        if not response:
            raise ImagineException("No response received")
        if not isinstance(response, list):
            raise ImagineException("Unexpected response body")

        return response

    def get_embedding_history(
        self, max_items: int = 1
    ) -> list[list[EmbeddingResponse | EmbeddingRequest]]:
        """
        Returns a list of Embedding (response, request) pairs made by the user.

        :param max_items: The number of items to retrieve

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            Returns a list of Embedding response, request pairs made by the user.

        """
        response = self._request(
            "get", "embeddings", {}, params={"max_items": max_items}
        )
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, list):
            raise ImagineException("Unexpected response body")
        return response

    def get_chat_history(
        self, max_items: int = 1
    ) -> list[list[ChatCompletionResponse | ChatCompletionRequest]]:
        """
        Returns a list of Chat (response, request) pairs made by the user.

        :param max_items: The number of items to retrieve

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            Returns a list of Chat response, request pairs made by the user.

        """
        response = self._request(
            "get", "chat/completions", {}, params={"max_items": max_items}
        )
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, list):
            raise ImagineException("Unexpected response body")
        return response

    def get_completion_history(
        self, max_items: int = 1
    ) -> list[list[CompletionResponse | CompletionRequest]]:
        """
        Returns a list of Completion (response, request) pairs made by the user.

        :param max_items: The number of items to retrieve

        :raises: ImagineException :class:`imagine.ImagineException`

        :return:
            Returns a list of Completion response, request pairs made by the user.

        """
        response = self._request(
            "get", "completions", {}, params={"max_items": max_items}
        )
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, list):
            raise ImagineException("Unexpected response body")
        return response

    def transcribe(
        self,
        input_file: str | BinaryIO,
        model: str | None = None,
    ) -> TranscribeResponse:
        """
        Transcribe an audio file to text.

        :param input_file: File object or path to the audio file.
        :param model: Name of the model generating the text.
        :return: Response with the transcribed audio.
        """
        if isinstance(input_file, str):
            input_file = open(input_file, "rb")

        if not model:
            model = self.default_model_transcribe

        response = self._request(
            "post",
            "transcribe",
            None,
            data={"model": model},
            files={"file": input_file},
        )
        if not response:
            raise ImagineException("No response received")

        if not isinstance(response, dict):
            raise ImagineException("Unexpected response body")
        return TranscribeResponse(**response)
