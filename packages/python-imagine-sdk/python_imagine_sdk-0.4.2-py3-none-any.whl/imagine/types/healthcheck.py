from pydantic import BaseModel


class PingResponse(BaseModel):
    #: Ping Message
    message: str

    #: Status
    status: str


class HealthResponse(BaseModel):
    #: Status of Postgres
    postgres: str

    #: Status of Redis
    redis: str

    #: Status of Models
    models: str
