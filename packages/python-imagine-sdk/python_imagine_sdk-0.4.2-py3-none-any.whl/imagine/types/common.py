from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class UsageInfo(BaseModel):
    #: Number of tokens in the prompt
    prompt_tokens: int | None = None

    #: Total number of tokens used in the request (prompt + completion).
    total_tokens: int | None = None

    #: Number of tokens in the generated completion
    completion_tokens: int | None = None


class DeltaMessage(BaseModel):
    #: The role of the message `user`, `assistant`, `system`
    role: str | None = None

    #: The content of the message
    content: str | None = None


class FinishReason(str, Enum):
    stop = "stop"
    length = "length"
    error = "error"
    tool_calls = "tool_calls"


class LLMSamplingParams(BaseModel):
    #: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim, defaults to None
    frequency_penalty: float | None = None

    #: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics, defaults to None
    presence_penalty: float | None = None

    #: Float that penalizes new tokens based on whether they appear in the prompt and the generated text so far. Values > 1 encourage the model to use new tokens, while values < 1 encourage the model to repeat tokens., defaults to None
    repetition_penalty: float | None = None

    #: Sequences where the API will stop generating further tokens. The returned text will contain the stop sequence., defaults to None
    stop: list[str] | None = None

    #: TBD, defaults to None
    max_seconds: int | None = None

    #: Whether to ignore the EOS token and continue generating tokens after the EOS token is generated., defaults to None
    ignore_eos: bool | None = None

    #: Whether to skip special tokens in the output., defaults to None
    skip_special_tokens: bool | None = None

    #: List of tokens that stop the generation when they are generated. The returned output will contain the stop tokens unless the stop tokens are special tokens., defaults to None
    stop_token_ids: list[list[int]] | None = None

    #: The maximum number of tokens that can be generated, defaults to None
    max_tokens: int | None = None

    #: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic., defaults to None
    temperature: float | None = None

    #: Integer that controls the number of top tokens to consider. Set to -1 to consider all tokens., defaults to None
    top_k: int | None = None

    #: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both., defaults to None
    top_p: float | None = None


class ModelType(str, Enum):
    EMBEDDING = "embedding"
    LLM = "llm"
    TEXT_TO_IMAGE = "text_to_image"
    TRANSLATE = "translate"
    TRANSCRIBE = "transcribe"
