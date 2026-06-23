from __future__ import annotations

import abc
import datetime
import json
import secrets
from collections.abc import AsyncGenerator, Callable
from enum import Enum
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Final, cast

from pydantic import ValidationError
from typing_extensions import Self

from aiorubi.client.default import Default
from aiorubi.client.rubika import PRODUCTION, RubikaAPIServer
from aiorubi.exceptions import (
    ClientDecodeError,
    RubikaAPIError,
    RubikaTooRequests,
    RubikaInvalidInput,
    RubikaServerError,
    RubikaInvalidAccess,
)
from aiorubi.methods import Response, RubikaMethod
from aiorubi.methods.base import RubikaType
from aiorubi.types import InputFile, RubikaObject

from .middlewares.manager import RequestMiddlewareManager

if TYPE_CHECKING:
    from types import TracebackType

    from aiorubi.client.bot import Bot

_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]

DEFAULT_TIMEOUT: Final[float] = 60.0


class BaseSession(abc.ABC):
    """
    This is base class for all HTTP sessions in aiorubi.

    If you want to create your own session, you must inherit from this class.
    """

    def __init__(
        self,
        api: RubikaAPIServer = PRODUCTION,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """

        :param api: Rubika Bot API URL patterns
        :param json_loads: JSON loader
        :param json_dumps: JSON dumper
        :param timeout: Session scope request timeout
        """
        self.api = api
        self.json_loads = json_loads
        self.json_dumps = json_dumps
        self.timeout = timeout

        self.middleware = RequestMiddlewareManager()

    def check_response(
        self,
        bot: Bot,
        method: RubikaMethod[RubikaType],
        status_code: int,
        content: str,
    ) -> Response[RubikaType]:
        """
        Check response status
        """

        try:
            phrase = HTTPStatus(status_code).phrase
        except ValueError:
            phrase = "Unknown"

        if HTTPStatus.INTERNAL_SERVER_ERROR <= status_code <= 599:
            raise RubikaServerError(
                method=method,
                message=f"{status_code} ({phrase})"
            )

        if not HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED:
            raise RubikaAPIError(
                method=method,
                message=f"HTTP error {status_code} ({phrase})",
            )

        try:
            json_data = self.json_loads(content)
        except Exception as e:  # noqa: BLE001
            # Handled error type can't be classified as specific error
            # in due to decoder can be customized and raise any exception

            msg = "Failed to decode object"
            raise ClientDecodeError(msg, e, content) from e

        if (field := method.__returning_field__) is not None:
            json_data = Response.unwrap(data=json_data, field=field)

        if method.__returning__ is bool and isinstance(json_data.get("data"), dict):
            json_data["data"] = True

        try:
            response_type = Response[method.__returning__]  # type: ignore
            response = response_type.model_validate(json_data, context={"bot": bot})
        except ValidationError as e:
            msg = "Failed to deserialize object"
            raise ClientDecodeError(msg, e, json_data) from e

        if response.ok:
            return response

        description = response.description

        if status := response.status:
            if status == "TOO_REQUESTS":
                raise RubikaTooRequests(
                    method=method,
                    message=description
                )
            if status == "INVALID_INPUT":
                raise RubikaInvalidInput(
                    method=method,
                    message=description
                )
            if status == "INVALID_ACCESS":
                raise RubikaInvalidAccess(
                    method=method,
                    message=description
                )
            if status == "SERVER_ERROR":
                raise RubikaServerError(
                    method=method,
                    message=description
                )

        raise RubikaAPIError(
            method=method,
            message=content,
        )

    @abc.abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """
        Close client session
        """

    @abc.abstractmethod
    async def make_request(
        self,
        bot: Bot,
        method: RubikaMethod[RubikaType],
        timeout: int | None = None,
    ) -> RubikaType:  # pragma: no cover
        """
        Make request to Rubika Bot API

        :param bot: Bot instance
        :param method: Method instance
        :param timeout: Request timeout
        :return:
        :raise RubikaAPIError:
        """

    @abc.abstractmethod
    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:  # pragma: no cover
        """
        Stream reader
        """
        yield b""

    def prepare_value(
        self,
        value: Any,
        bot: Bot,
        _dumps_json: bool = False
    ) -> Any:
        """
        Prepare value before send
        """
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, Default):
            default_value = bot.default[value.name]
            return self.prepare_value(default_value, bot=bot, _dumps_json=_dumps_json)

        if isinstance(value, dict):
            value = {
                k: prepared_item
                for k, item in value.items()
                if (prepared_item := self.prepare_value(item, bot=bot, _dumps_json=False)) is not None
            }
            return self.json_dumps(value) if _dumps_json else value

        if isinstance(value, list):
            value = [
                prepared_item
                for item in value
                if (prepared_item := self.prepare_value(item, bot=bot, _dumps_json=False)) is not None
            ]
            return self.json_dumps(value) if _dumps_json else value

        if isinstance(value, (datetime.datetime, datetime.timedelta)):
            if isinstance(value, datetime.timedelta):
                value = datetime.datetime.now() + value
            return str(round(value.timestamp()))

        if isinstance(value, Enum):
            return self.prepare_value(value.value, bot=bot, _dumps_json=_dumps_json)

        if isinstance(value, RubikaObject):
            return self.prepare_value(value.model_dump(exclude_none=True), bot=bot, _dumps_json=_dumps_json)

        if _dumps_json:
            return self.json_dumps(value)
        return value

    async def __call__(
        self,
        bot: Bot,
        method: RubikaMethod[RubikaType],
        timeout: int | None = None,
    ) -> RubikaType:
        middleware = self.middleware.wrap_middlewares(self.make_request, timeout=timeout)
        return cast(RubikaType, await middleware(bot, method))

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()