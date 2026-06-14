from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from aiorubi.dispatcher.middlewares.base import BaseMiddleware
from aiorubi.types import (
    RubikaObject,
    Update,
)

EVENT_CONTEXT_KEY = "event_context"

EVENT_FROM_USER_KEY = "event_from_user"
EVENT_CHAT_KEY = "event_chat"


@dataclass(frozen=True)
class EventContext:
    chat_id: str | None = None
    user_id: str | None = None


class UserContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[RubikaObject, dict[str, Any]], Awaitable[Any]],
        event: RubikaObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Update):
            msg = "UserContextMiddleware got an unexpected event type!"
            raise RuntimeError(msg)
        event_context = data[EVENT_CONTEXT_KEY] = self.resolve_event_context(event=event)

        # Backward compatibility
        if event_context.user_id is not None:
            data[EVENT_FROM_USER_KEY] = event_context.user_id
        if event_context.chat_id is not None:
            data[EVENT_CHAT_KEY] = event_context.chat_id

        return await handler(event, data)

    @classmethod
    def resolve_event_context(cls, event: Update) -> EventContext:
        """
        Resolve chat and user instance from Update object
        """
        if event.new_message:
            return EventContext(
                chat_id=event.chat_id,
                user_id=event.new_message.sender_id,
            )
        if event.updated_message:
            return EventContext(
                chat_id=event.chat_id,
                user_id=event.updated_message.sender_id,
            )
        if event.removed_message:
            return EventContext(
                chat_id=event.chat_id,
            )
        return EventContext()