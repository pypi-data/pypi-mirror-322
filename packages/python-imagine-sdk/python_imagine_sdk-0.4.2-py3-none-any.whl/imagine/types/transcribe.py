from __future__ import annotations

from pydantic import BaseModel


class TranscribeRequest(BaseModel):
    #: model to be used for transcribing
    model: str


class TranscribeResponse(BaseModel):
    #: Time taken to generate the response (In seconds)
    generation_time: float

    #: ID of the transcription request
    id: str

    #: Audio transcription
    text: str

    #: The timestamp of when the response was generated
    ts: str | None
