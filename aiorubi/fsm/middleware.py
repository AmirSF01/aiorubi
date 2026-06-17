from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiorubi import Bot
from aiorubi.dispatcher.middlewares.base import BaseMiddleware
from aiorubi.dispatcher.middlewares.user_context import EVENT_CONTEXT_KEY, EventContext
from aiorubi.fsm.context import FSMContext
from aiorubi.fsm.storage.base import (
    DEFAULT_DESTINY,
    BaseEventIsolation,
    BaseStorage,
    StorageKey,
)
from aiorubi.fsm.strategy import FSMStrategy, apply_strategy
from aiorubi.types import RubikaObject


class FSMContextMiddleware(BaseMiddleware):
    def __init__(
        self,
        storage: BaseStorage,
        events_isolation: BaseEventIsolation,
        strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
    ) -> None:
        self.storage = storage
        self.strategy = strategy
        self.events_isolation = events_isolation

    async def __call__(
        self,
        handler: Callable[[RubikaObject, dict[str, Any]], Awaitable[Any]],
        event: RubikaObject,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = cast(Bot, data["bot"])
        context = self.resolve_event_context(bot, data)
        data["fsm_storage"] = self.storage
        if context:
            # Bugfix: https://github.com/aiogram/aiogram/issues/1317
            # State should be loaded after lock is acquired
            async with self.events_isolation.lock(key=context.key):
                data.update({"state": context, "raw_state": await context.get_state()})
                return await handler(event, data)
        return await handler(event, data)

    def resolve_event_context(
        self,
        bot: Bot,
        data: dict[str, Any],
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext | None:
        event_context: EventContext = cast(EventContext, data.get(EVENT_CONTEXT_KEY))
        return self.resolve_context(
            bot=bot,
            chat_id=event_context.chat_id,
            user_id=event_context.user_id,
            destiny=destiny,
        )

    def resolve_context(
        self,
        bot: Bot,
        chat_id: str | None,
        user_id: str | None,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext | None:
        if chat_id is not None and user_id is not None:
            chat_id, user_id = apply_strategy(
                chat_id=chat_id,
                user_id=user_id,
                strategy=self.strategy,
            )
            return self.get_context(
                bot=bot,
                chat_id=chat_id,
                user_id=user_id,
                destiny=destiny,
            )
        return None

    def get_context(
        self,
        bot: Bot,
        chat_id: str,
        user_id: str,
        destiny: str = DEFAULT_DESTINY,
    ) -> FSMContext:
        return FSMContext(
            storage=self.storage,
            key=StorageKey(
                user_id=user_id,
                chat_id=chat_id,
                bot_id=bot.id,
                destiny=destiny,
            ),
        )

    async def close(self) -> None:
        await self.storage.close()
        await self.events_isolation.close()