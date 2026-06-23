import logging
from typing import TYPE_CHECKING, Any

from aiorubi import loggers
from aiorubi.methods import RubikaMethod
from aiorubi.methods.base import Response, RubikaType

from .base import BaseRequestMiddleware, NextRequestMiddlewareType

if TYPE_CHECKING:
    from aiorubi.client.bot import Bot

logger = logging.getLogger(__name__)


class RequestLogging(BaseRequestMiddleware):
    def __init__(self, ignore_methods: list[type[RubikaMethod[Any]]] | None = None):
        """
        Middleware for logging outgoing requests

        :param ignore_methods: methods to ignore in logging middleware
        """
        self.ignore_methods = ignore_methods or []

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[RubikaType],
        bot: Bot,
        method: RubikaMethod[RubikaType],
    ) -> Response[RubikaType]:
        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                "Make request with method=%r by bot id=%d",
                type(method).__name__,
                bot.id,
            )
        return await make_request(bot, method)