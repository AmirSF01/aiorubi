from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

from aiorubi.methods.base import RubikaType

if TYPE_CHECKING:
    from aiorubi.client.bot import Bot
    from aiorubi.methods import Response, RubikaMethod


class NextRequestMiddlewareType(Protocol[RubikaType]):  # pragma: no cover
    async def __call__(
        self,
        bot: Bot,
        method: RubikaMethod[RubikaType],
    ) -> Response[RubikaType]:
        pass


class RequestMiddlewareType(Protocol):  # pragma: no cover
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[RubikaType],
        bot: Bot,
        method: RubikaMethod[RubikaType],
    ) -> Response[RubikaType]:
        pass


class BaseRequestMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[RubikaType],
        bot: Bot,
        method: RubikaMethod[RubikaType],
    ) -> Response[RubikaType]:
        """
        Execute middleware

        :param make_request: Wrapped make_request in middlewares chain
        :param bot: bot for request making
        :param method: Request method (Subclass of :class:`aiorubi.methods.base.RubikaMethod`)

        :return: :class:`aiorubi.methods.Response`
        """