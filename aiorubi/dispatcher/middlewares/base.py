from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from aiorubi.types import RubikaObject

T = TypeVar("T")


class BaseMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__(
        self,
        handler: Callable[[RubikaObject, dict[str, Any]], Awaitable[Any]],
        event: RubikaObject,
        data: dict[str, Any],
    ) -> Any:  # pragma: no cover
        """
        Execute middleware

        :param handler: Wrapped handler in middlewares chain
        :param event: Incoming event (Subclass of :class:`aiorubi.types.base.RubikaObject`)
        :param data: Contextual data. Will be mapped to handler arguments
        :return: :class:`Any`
        """