from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UsageRecord(BaseModel):
    #: userid for particular usage record
    userid: str

    #: model corresponding to usage record
    model: str

    #: date_bin corresponding to usage record
    date_bin: datetime

    #: total input tokens corresponding to the usage record
    total_input_tokens: int

    #: total output tokens corresponding to the usage record
    total_output_tokens: int

    #: total tokens corresponding to the usage record
    total_tokens: int

    #: total generation time corresponding to the usage record
    total_generation_time: float


class UsageRecordAggregated(BaseModel):
    #: userid for particular usage aggregation
    userid: str

    #: model corresponding to usage aggregation
    model: str

    #: total input tokens corresponding to the usage aggregation
    total_input_tokens: int

    #: total output tokens corresponding to the usage aggregation
    total_output_tokens: int

    #: total tokens corresponding to the usage aggregation
    total_tokens: int

    #: total generation time corresponding to the usage aggregation
    total_generation_time: float


class UsageResponse(BaseModel):
    #: list of usage record
    usage: list[UsageRecord]

    #: list of overall usage per record type
    overall: list[UsageRecordAggregated]
