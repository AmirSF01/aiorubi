from __future__ import annotations

from pydantic import model_validator
from typing import TYPE_CHECKING, Any, cast

from ..utils.mypy_hacks import lru_cache
from ..enums import UpdateType
from .base import RubikaObject
from .removed_message import RemovedMessage
from .started_bot import StartedBot
from .stopped_bot import StoppedBot
from .custom import DateTime

if TYPE_CHECKING:
    from .message import Message
    from .inline_message import InlineMessage


class Update(RubikaObject):
    """
    This object represents an incoming update.

    Source: https://rubika.ir/botapi/models#update
    """

    type: UpdateType
    """The type of update (e.g., NewMessage, EditMessage, RemoveMessage)."""
    chat_id: str
    """Unique identifier for the chat where the update occurred."""
    new_message: Message | None = None
    """*Optional*. New incoming message of any kind."""
    updated_message: Message | None = None
    """*Optional*. New version of a message that is known to the bot and was edited."""
    removed_message: RemovedMessage | None = None
    """*Optional*. Identifier of the message that was removed. Parsed from removed_message_id."""
    inline_message: InlineMessage | None = None
    """*Optional*. Inline message event (button click / inline interaction)."""
    started_bot: StartedBot | None = None
    """*Optional*. Present when the user has started/unblocked the bot."""
    stopped_bot: StoppedBot | None = None
    """*Optional*. Present when the user has stopped/blocked the bot."""
    update_time: DateTime | None = None
    """Unix timestamp of when the update was received."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            type: UpdateType,
            chat_id: str,
            new_message: Message | None = None,
            updated_message: Message | None = None,
            removed_message: RemovedMessage | None = None,
            inline_message: InlineMessage | None = None,
            update_time: int | str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                chat_id=chat_id,
                new_message=new_message,
                updated_message=updated_message,
                removed_message=removed_message,
                inline_message=inline_message,
                update_time=update_time,
                **__pydantic_kwargs,
            )

    @model_validator(mode="before")
    @classmethod
    def normalize_raw_data(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = data.copy()
        chat_id = data.get("chat_id")
        raw_type = data.get("type")

        for key in ("new_message", "updated_message"):
            nested = data.get(key)
            if isinstance(nested, dict):
                nested = nested.copy()
                nested["chat_id"] = chat_id
                data[key] = nested

        if data.get("removed_message_id") is not None:
            data["removed_message"] = {
                "message_id": data["removed_message_id"],
                "chat_id": chat_id,
            }

        if raw_type == UpdateType.STARTED_BOT:
            data["started_bot"] = {"chat_id": chat_id}
        elif raw_type == UpdateType.STOPPED_BOT:
            data["stopped_bot"] = {"chat_id": chat_id}

        return data

    def __hash__(self) -> int:
        return hash((
            type(self),
            self.type,
            self.chat_id,
            self.message_id,
            self.update_time,
        ))

    @property
    def message_id(self) -> str | None:
        if self.new_message:
            return self.new_message.message_id
        if self.updated_message:
            return self.updated_message.message_id
        if self.removed_message:
            return self.removed_message.message_id
        if self.inline_message:
            return self.inline_message.message_id
        return None

    @property
    @lru_cache()
    def event_type(self) -> str:
        type_map = {
            UpdateType.NEW_MESSAGE: "new_message",
            UpdateType.UPDATED_MESSAGE: "updated_message",
            UpdateType.REMOVED_MESSAGE: "removed_message",
            UpdateType.INLINE_MESSAGE: "inline_message",
            UpdateType.STARTED_BOT: "started_bot",
            UpdateType.STOPPED_BOT: "stopped_bot",
        }
        try:
            return type_map[self.type]
        except KeyError:
            raise UpdateTypeLookupError(
                f"Unknown update type: {self.type!r}"
            ) from None

    @property
    def event(self) -> RubikaObject:
        return cast(RubikaObject, getattr(self, self.event_type))


class UpdateTypeLookupError(LookupError):
    """Update does not contain any known event type."""