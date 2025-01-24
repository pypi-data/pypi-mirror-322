from __future__ import annotations

from typing import Any

from httpx import Response


class ImagineException(Exception):
    """Base Exception class, returned when nothing more specific applies"""

    def __init__(self, message: str | None = None):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        msg = self.message or "<empty message>"
        return msg

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={str(self)})"


class ImagineAPIException(ImagineException):
    """Returned when the API responds with an error message"""

    def __init__(
        self,
        message: str | None = None,
        http_status: int | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.headers: dict[str, Any] = headers or {}

    @classmethod
    def from_response(
        cls, response: Response, message: str | None = None
    ) -> "ImagineAPIException":
        return cls(
            message=message or response.text,
            http_status=response.status_code,
            headers=dict(response.headers),
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={str(self)}, "
            f"http_status={self.http_status})"
        )


class ImagineAPIStatusException(ImagineAPIException):
    """Returned when we receive a non-200 response from the API that we should retry"""


class ImagineConnectionException(ImagineException):
    """Returned when the SDK can not reach the API server for any reason"""


class ImagineAPITooManyRequestsException(ImagineAPIException):
    """Returned when we receive a 429 response from the API, indicating that we probably hit a rate limit"""
