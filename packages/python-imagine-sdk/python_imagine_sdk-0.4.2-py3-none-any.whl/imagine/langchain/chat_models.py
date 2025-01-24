from __future__ import annotations

import json

from operator import itemgetter
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Iterator,
    List,
    Literal,
    Optional,
    Sequence,
    Type,
    Union,
    cast,
)

from pydantic import BaseModel

from imagine.langchain.mixins import BaseLangChainMixin
from imagine.types.chat_completions import ChatMessage as ImagineChatMessage


try:
    from langchain_core.callbacks import (
        AsyncCallbackManagerForLLMRun,
        CallbackManagerForLLMRun,
    )
    from langchain_core.language_models import LanguageModelInput
    from langchain_core.language_models.chat_models import (
        BaseChatModel,
        agenerate_from_stream,
        generate_from_stream,
    )
    from langchain_core.messages import (
        AIMessage,
        AIMessageChunk,
        BaseMessage,
        BaseMessageChunk,
        ChatMessage,
        ChatMessageChunk,
        HumanMessage,
        HumanMessageChunk,
        SystemMessage,
        SystemMessageChunk,
        ToolCall,
        ToolMessage,
    )
    from langchain_core.output_parsers.base import OutputParserLike
    from langchain_core.output_parsers.openai_tools import (
        JsonOutputKeyToolsParser,
        PydanticToolsParser,
        make_invalid_tool_call,
    )

    # parse_tool_call,
    from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
    from langchain_core.runnables import Runnable, RunnableMap, RunnablePassthrough
    from langchain_core.tools import BaseTool
    from langchain_core.utils.function_calling import convert_to_openai_tool
    from langchain_core.utils.pydantic import is_basemodel_subclass

except ImportError:
    raise ImportError(
        "LangChain dependencies are missing. Please install with 'pip install python-imagine-sdk[langchain]' to add them."
    )

from imagine.types.chat_completions import (
    ChatCompletionResponse,
    ChatCompletionStreamResponse,
)


def _convert_imagine_message_to_lc_message(
    _message: ImagineChatMessage,
) -> BaseMessage:
    role = _message.role
    content = _message.content

    if role == "user":
        return HumanMessage(content=content)
    elif role == "assistant":
        additional_kwargs: dict = {}
        tool_calls = []
        invalid_tool_calls = []
        if response_tool_calls := _message.tool_calls:
            # additional_kwargs["tool_calls"] = response_tool_calls
            for response_tool_call in response_tool_calls:
                try:
                    # tool_calls.append(parse_tool_call(raw_tool_call, return_id=True))
                    tool_calls.append(
                        ToolCall(
                            name=response_tool_call.function.name,
                            args=json.loads(response_tool_call.function.arguments),
                            id=response_tool_call.id,
                            type="tool_call",
                        )
                    )

                except Exception as e:
                    invalid_tool_calls.append(
                        make_invalid_tool_call(response_tool_call, str(e))
                    )

        return AIMessage(
            content=content,
            additional_kwargs=additional_kwargs,
            tool_calls=tool_calls,
            invalid_tool_calls=invalid_tool_calls,
        )

    elif role == "system":
        return SystemMessage(content=content)

    elif role == "tool":
        additional_kwargs = {}
        additional_kwargs["name"] = _message.name
        return ToolMessage(
            content=content,
            tool_call_id=_message.tool_call_id,
            additional_kwargs=additional_kwargs,
        )
    else:
        return ChatMessage(content=content, role=role)


def _convert_chunk_to_message_chunk(
    chunk: ChatCompletionStreamResponse, default_class: Type[BaseMessageChunk]
) -> BaseMessageChunk:
    _delta = chunk.choices[0].delta
    role = _delta.role
    content = _delta.content or ""
    if role == "user" or default_class == HumanMessageChunk:
        return HumanMessageChunk(content=content)
    elif role == "assistant" or default_class == AIMessageChunk:
        if token_usage := chunk.usage:
            usage_metadata = {
                "input_tokens": token_usage.prompt_tokens,
                "output_tokens": token_usage.completion_tokens,
                "total_tokens": token_usage.total_tokens,
            }
        else:
            usage_metadata = None
        return AIMessageChunk(
            content=content,
            usage_metadata=usage_metadata,  # type: ignore[arg-type]
        )
    elif role == "system" or default_class == SystemMessageChunk:
        return SystemMessageChunk(content=content)
    elif role or default_class == ChatMessageChunk:
        return ChatMessageChunk(content=content, role=role)  # type: ignore
    else:
        return default_class(content=content)  # type: ignore[call-arg]


def _lc_tool_call_to_imagine_tool_call(tool_call: ToolCall) -> dict:
    return {
        "type": "function",
        "id": tool_call["id"],
        "function": {
            "name": tool_call["name"],
            "arguments": json.dumps(tool_call["args"]),
        },
    }


def _convert_lc_message_to_dict_message(
    message: BaseMessage,
) -> dict:
    if isinstance(message, ChatMessage):
        message_dict = {"role": message.role, "content": message.content}

    elif isinstance(message, HumanMessage):
        message_dict = {"role": "user", "content": message.content}

    elif isinstance(message, AIMessage):
        message_dict: dict[str, Any] = {"role": "assistant", "content": message.content}
        if message.tool_calls:
            message_dict["tool_calls"] = [
                _lc_tool_call_to_imagine_tool_call(tc) for tc in message.tool_calls
            ]
        elif "tool_calls" in message.additional_kwargs:
            message_dict["tool_calls"] = message.additional_kwargs["tool_calls"]

    elif isinstance(message, SystemMessage):
        message_dict = {"role": "system", "content": message.content}

    elif isinstance(message, ToolMessage):
        message_dict = {
            "role": "tool",
            "content": message.content,
            "tool_call_id": message.tool_call_id,
        }
    else:
        raise ValueError(f"Got unknown type {message}")

    return message_dict


class ImagineChat(BaseChatModel, BaseLangChainMixin):
    """A chat model that use Imagine Inference API"""

    # max_concurrent_requests: int = 64 # later
    model: str = "Llama-3.1-8B"

    temperature: float = 0.0
    max_tokens: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    streaming: bool = False

    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    repetition_penalty: Optional[float] = None
    stop: Optional[List[str]] = None
    max_seconds: Optional[int] = None
    ignore_eos: Optional[bool] = None
    skip_special_tokens: Optional[bool] = None
    stop_token_ids: Optional[List[List[int]]] = None

    @property
    def _default_params(self) -> dict[str, Any]:
        """Get the default parameters for calling the API."""

        body = dict(
            model=self.model,
            stream=self.streaming,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            repetition_penalty=self.repetition_penalty,
            stop=self.stop,
            max_seconds=self.max_seconds,
            ignore_eos=self.ignore_eos,
            skip_special_tokens=self.skip_special_tokens,
            stop_token_ids=self.stop_token_ids,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
        )

        body = {k: v for k, v in body.items() if v is not None}
        return body

    @property
    def _client_params(self) -> dict[str, Any]:
        """Get the parameters used for the client."""
        return self._default_params

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Get the identifying parameters."""
        return self._default_params

    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "imagine-chat"

    @property
    def lc_secrets(self) -> dict[str, str]:
        return {"IMAGINE_API_KEY": "IMAGINE_API_KEY"}

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this model can be serialized by Langchain."""
        return True

    @classmethod
    def get_lc_namespace(cls) -> list[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "chat_models", "imagine"]

    def _combine_llm_outputs(self, llm_outputs: list[dict | None]) -> dict:
        overall_token_usage: dict = {}
        for output in llm_outputs:
            if output is None:
                # Happens in streaming
                continue

            if token_usage := output.get("token_usage", None):
                for k, v in token_usage.items():
                    if k in overall_token_usage:
                        overall_token_usage[k] += v
                    else:
                        overall_token_usage[k] = v
        combined = {"token_usage": overall_token_usage, "model_name": self.model}
        return combined

    def _create_chat_result(self, response: ChatCompletionResponse) -> ChatResult:
        generations = []
        for res in response.choices:
            finish_reason = str(res.finish_reason)
            message = _convert_imagine_message_to_lc_message(res.message)
            if response.usage and isinstance(message, AIMessage):
                message.usage_metadata = {
                    "input_tokens": response.usage.prompt_tokens or 0,
                    "output_tokens": response.usage.completion_tokens or 0,
                    "total_tokens": response.usage.total_tokens or 0,
                }
            gen = ChatGeneration(
                message=message,
                generation_info={"finish_reason": finish_reason},
            )
            generations.append(gen)

        llm_output = {"token_usage": response.usage.model_dump(), "model": self.model}
        return ChatResult(generations=generations, llm_output=llm_output)

    def _create_message_dicts(
        self, messages: list[BaseMessage]
    ) -> tuple[list[dict], dict[str, Any]]:
        params = self._client_params
        message_dicts = [_convert_lc_message_to_dict_message(m) for m in messages]
        return message_dicts, params

    def _stream(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        message_dicts, params = self._create_message_dicts(messages)
        params = {**params, **kwargs}
        params.pop("stream", "")

        default_chunk_class: Type[BaseMessageChunk] = AIMessageChunk

        for chunk in self.client.chat_stream(messages=message_dicts, **params):
            if len(chunk.choices) == 0:
                continue
            new_chunk = _convert_chunk_to_message_chunk(chunk, default_chunk_class)
            # make future chunks same type as first chunk
            default_chunk_class = new_chunk.__class__
            gen_chunk = ChatGenerationChunk(message=new_chunk)
            if run_manager:
                run_manager.on_llm_new_token(
                    token=cast(str, new_chunk.content), chunk=gen_chunk
                )
            yield gen_chunk

    async def _astream(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        message_dicts, params = self._create_message_dicts(messages)
        params = {**params, **kwargs}
        params.pop("stream", "")

        default_chunk_class: Type[BaseMessageChunk] = AIMessageChunk
        async for chunk in self.async_client.chat_stream(
            messages=message_dicts, **params
        ):
            if len(chunk.choices) == 0:
                continue
            new_chunk = _convert_chunk_to_message_chunk(chunk, default_chunk_class)
            # make future chunks same type as first chunk
            default_chunk_class = new_chunk.__class__
            gen_chunk = ChatGenerationChunk(message=new_chunk)
            if run_manager:
                await run_manager.on_llm_new_token(
                    token=cast(str, new_chunk.content), chunk=gen_chunk
                )
            yield gen_chunk

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        message_dicts, params = self._create_message_dicts(messages)
        params = {**params, **kwargs}
        params.pop("stream", "")

        if self.streaming:
            stream_iter = self.client.chat_stream(
                messages=message_dicts,
                **params,  # type: ignore
            )
            return generate_from_stream(stream_iter)  # type: ignore

        response = self.client.chat(messages=message_dicts, **params)
        return self._create_chat_result(response)

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        stream: bool | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        message_dicts, params = self._create_message_dicts(messages)
        params = {**params, **kwargs}
        params.pop("stream", "")

        should_stream = stream if stream is not None else self.streaming
        if should_stream:
            stream_iter = self._astream(
                messages=messages, stop=stop, run_manager=run_manager, **params
            )
            return await agenerate_from_stream(stream_iter)

        response = await self.async_client.chat(messages=message_dicts, **params)

        return self._create_chat_result(response)

    def bind_tools(
        self,
        tools: Sequence[Union[dict[str, Any], Type[BaseModel], Callable, BaseTool]],
        *,
        tool_choice: Optional[
            Union[dict, str, Literal["auto", "any", "none"], bool]
        ] = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        if tool_choice == "any" or tool_choice == "none":
            raise ValueError("Imagine only supports tool_choice as 'auto'")

        formatted_tools = [convert_to_openai_tool(tool) for tool in tools]

        return super().bind(tools=formatted_tools, **kwargs)

    def _is_pydantic_class(obj: Any) -> bool:
        return isinstance(obj, type) and is_basemodel_subclass(obj)

    # TODO: we don't support "json_mode" with structured output
    # implement it in tool calling
    def with_structured_output(
        self,
        schema: Optional[Union[dict, Type[BaseModel]]] = None,
        *,
        method: Literal["function_calling"] = "function_calling",
        include_raw: bool = False,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, Union[dict, BaseModel]]:
        is_pydantic_schema = isinstance(schema, type) and is_basemodel_subclass(schema)

        if method == "function_calling":
            if schema is None:
                raise ValueError(
                    "schema must be specified when method is 'function_calling'. "
                    "Received None."
                )

            tool_name = convert_to_openai_tool(schema)["function"]["name"]
            llm = self.bind_tools([schema], tool_choice=tool_name)

            if is_pydantic_schema:
                output_parser: OutputParserLike = PydanticToolsParser(
                    tools=[schema],
                    first_tool_only=True,
                )
            else:
                output_parser = JsonOutputKeyToolsParser(
                    key_name=tool_name, first_tool_only=True
                )
        else:
            raise ValueError(
                f"Unrecognized method argument. Expected one of 'function_calling' Received: '{method}'"
            )

        if include_raw:
            parser_assign = RunnablePassthrough.assign(
                parsed=itemgetter("raw") | output_parser, parsing_error=lambda _: None
            )
            parser_none = RunnablePassthrough.assign(parsed=lambda _: None)
            parser_with_fallback = parser_assign.with_fallbacks(
                [parser_none], exception_key="parsing_error"
            )
            return RunnableMap(raw=llm) | parser_with_fallback
        else:
            return llm | output_parser
