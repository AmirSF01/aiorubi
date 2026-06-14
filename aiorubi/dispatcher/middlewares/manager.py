import functools
from collections.abc import Callable, Sequence
from typing import Any, overload

from aiorubi.dispatcher.event.bases import (
    MiddlewareEventType,
    MiddlewareType,
    NextMiddlewareType,
)
from aiorubi.dispatcher.event.handler import CallbackType
from aiorubi.types import RubikaObject


class MiddlewareManager(Sequence[MiddlewareType[RubikaObject]]):
    def __init__(self) -> None:
        self._middlewares: list[MiddlewareType[RubikaObject]] = []

    def register(
        self,
        middleware: MiddlewareType[RubikaObject],
    ) -> MiddlewareType[RubikaObject]:
        self._middlewares.append(middleware)
        return middleware

    def unregister(self, middleware: MiddlewareType[RubikaObject]) -> None:
        self._middlewares.remove(middleware)

    def __call__(
        self,
        middleware: MiddlewareType[RubikaObject] | None = None,
    ) -> (
        Callable[[MiddlewareType[RubikaObject]], MiddlewareType[RubikaObject]]
        | MiddlewareType[RubikaObject]
    ):
        if middleware is None:
            return self.register
        return self.register(middleware)

    @overload
    def __getitem__(self, item: int) -> MiddlewareType[RubikaObject]:
        pass

    @overload
    def __getitem__(self, item: slice) -> Sequence[MiddlewareType[RubikaObject]]:
        pass

    def __getitem__(
        self,
        item: int | slice,
    ) -> MiddlewareType[RubikaObject] | Sequence[MiddlewareType[RubikaObject]]:
        return self._middlewares[item]

    def __len__(self) -> int:
        return len(self._middlewares)

    @staticmethod
    def wrap_middlewares(
        middlewares: Sequence[MiddlewareType[MiddlewareEventType]],
        handler: CallbackType,
    ) -> NextMiddlewareType[MiddlewareEventType]:
        @functools.wraps(handler)
        def handler_wrapper(event: RubikaObject, kwargs: dict[str, Any]) -> Any:
            return handler(event, **kwargs)

        middleware = handler_wrapper
        for m in reversed(middlewares):
            middleware = functools.partial(m, middleware)  # type: ignore[assignment]
        return middleware