from typing import Any

from aiorubi.methods import RubikaMethod
from aiorubi.methods.base import RubikaType
# from aiorubi.utils.link import docs_url


class AiorubiError(Exception):
    """
    Base exception for all aiorubi errors.
    """


class DetailedAiorubiError(AiorubiError):
    """
    Base exception for all aiorubi errors with detailed message.
    """

    url: str | None = None

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        message = self.message
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class CallbackAnswerException(AiorubiError):
    """
    Exception for callback answer.
    """


class SceneException(AiorubiError):
    """
    Exception for scenes.
    """


class UnsupportedKeywordArgument(DetailedAiorubiError):
    """
    Exception raised when a keyword argument is passed as filter.
    """


class RubikaAPIError(DetailedAiorubiError):
    """
    Base exception for all Rubika API errors.
    """

    label: str = "Rubika server says"

    def __init__(
        self,
        method: RubikaMethod[RubikaType],
        message: str,
    ) -> None:
        super().__init__(message=message)
        self.method = method

    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"


class RubikaNetworkError(RubikaAPIError):
    """
    Base exception for all Rubika network errors.
    """

    label = "HTTP Client says"


class RubikaTooRequests(RubikaAPIError):
    """
    Exception raised when the Rubika API returns a "TOO_REQUESTS" status,
    meaning the bot has sent too many requests in a short time.

    Note: Rubika does not provide a 'retry_after' value, so the client
    must manage timing between requests based on experience.
    """

    def __init__(
        self,
        method: RubikaMethod[RubikaType],
        message: str | None = None,
        retry_after: int | None = None,
    ) -> None:
        description = f"Flood control exceeded on method {type(method).__name__!r}."
        if retry_after:
            description += f" Retry after {retry_after} seconds."
        description += f"\nOriginal description: {message}"

        super().__init__(
            method=method,
            message=description or "Too many requests, slow down."
        )
        self.retry_after = retry_after


class RubikaInvalidInput(RubikaAPIError):
    """
    Exception raised when request is malformed.
    """

    def __init__(
            self,
            method: RubikaMethod[RubikaType],
            message: str | None = None,
    ) -> None:
        super().__init__(
            method=method,
            message=message or "Request contains invalid input."
        )

class RubikaInvalidAccess(RubikaAPIError):
    """
    Exception raised when the bot does not have permission to perform the requested action.
    """

    def __init__(
            self,
            method: RubikaMethod[RubikaType],
            message: str | None = None,
    ) -> None:
        super().__init__(
            method=method,
            message=message or "Access denied. Invalid credentials or insufficient permissions"
        )


class RubikaServerError(RubikaAPIError):
    """
    Exception raised when Rubika server returns 5xx HTTP error or "status": "SERVER_ERROR".
    """

    def __init__(
            self,
            method: RubikaMethod[RubikaType],
            message: str | None = None,
    ) -> None:
        super().__init__(
            method=method,
            message=message or "Server error"
        )


class ClientDecodeError(AiorubiError):
    """
    Exception raised when client can't decode response. (Malformed response, etc.)
    """

    def __init__(self, message: str, original: Exception, data: Any) -> None:
        self.message = message
        self.original = original
        self.data = data

    def __str__(self) -> str:
        original_type = type(self.original)
        return (
            f"{self.message}\n"
            f"Caused from error: "
            f"{original_type.__module__}.{original_type.__name__}: {self.original}\n"
            f"Content: {self.data}"
        )


class DataNotDictLikeError(DetailedAiorubiError):
    """
    Exception raised when data is not dict-like.
    """