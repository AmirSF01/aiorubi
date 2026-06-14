from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, NoReturn, TypeVar
from unittest.mock import sentinel

from aiorubi.dispatcher.middlewares.base import BaseMiddleware
from aiorubi.types import RubikaObject

MiddlewareEventType = TypeVar("MiddlewareEventType", bound=RubikaObject)
NextMiddlewareType = Callable[[MiddlewareEventType, dict[str, Any]], Awaitable[Any]]
MiddlewareType = (
    BaseMiddleware
    | Callable[
        [NextMiddlewareType[MiddlewareEventType], MiddlewareEventType, dict[str, Any]],
        Awaitable[Any],
    ]
)


UNHANDLED = sentinel.UNHANDLED
REJECTED = sentinel.REJECTED


class SkipHandler(Exception):
    pass


class CancelHandler(Exception):
    pass


def skip(message: str | None = None) -> NoReturn:
    """
    Raise an SkipHandler
    """
    raise SkipHandler(message or "Event skipped")