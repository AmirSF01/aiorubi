from __future__ import annotations

from pydantic import Field, field_validator, model_validator
from typing import TYPE_CHECKING, Any, cast

from ..utils.mypy_hacks import lru_cache
from .base import RubikaObject
from .custom import DateTime

if TYPE_CHECKING:
    from .message import Message
    from .removed_message import RemovedMessage
    from .inline_message import InlineMessage


class Update(RubikaObject):
    """
    This object represents an incoming update.

    Source: https://rubika.ir/botapi/models#update
    """

    type: str
    """The type of update (e.g., NewMessage, EditMessage, RemoveMessage)."""
    chat_id: str
    """Unique identifier for the chat where the update occurred."""
    new_message: Message | None = None
    """*Optional*. New incoming message of any kind."""
    updated_message: Message | None = None
    """*Optional*. New version of a message that is known to the bot and was edited."""
    removed_message: RemovedMessage | None = Field(None, alias="removed_message_id")
    inline_message: InlineMessage | None = None
    """Inline message event (button click / inline interaction)."""
    """*Optional*. Identifier of the message that was removed. Parsed from removed_message_id."""
    update_time: DateTime | None = None
    """Unix timestamp of when the update was received."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            type: str,
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

    @field_validator("removed_message", mode="before")
    @classmethod
    def parse_removed_message(cls, v: str | None) -> RemovedMessage | None:
        if v is None:
            return None
        return RemovedMessage(message_id=v)

    @model_validator(mode="after")
    def resolve_events(self) -> "Update":
        if self.new_message:
            object.__setattr__(self.new_message, 'chat_id', self.chat_id)
        if self.updated_message:
            object.__setattr__(self.updated_message, 'chat_id', self.chat_id)
        if self.removed_message:
            object.__setattr__(self.removed_message, 'chat_id', self.chat_id)
        # NOTE: inline_message already contains chat_id from API. no injection needed
        return self

    def __hash__(self) -> int:
        """
        Generate a unique hash for this update.

        - NewMessage: chat_id + message_id are sufficient (each message has a unique ID)
        - UpdatedMessage: chat_id + message_id + update_time are needed (same message can be edited multiple times)
        - RemovedMessage: chat_id + message_id are sufficient (each message is removed only once)
        - Fallback: chat_id + type + update_time for unknown update types
        """
        if self.new_message:
            return hash((type(self), self.type, self.chat_id, self.new_message.message_id))
        if self.updated_message:
            return hash((type(self), self.type, self.chat_id, self.updated_message.message_id, self.update_time))
        if self.removed_message:
            return hash((type(self), self.type, self.chat_id, self.removed_message.message_id))
        if self.inline_message:
            return hash((type(self), self.type, self.chat_id, self.inline_message.message_id))
        return hash((type(self), self.type, self.chat_id, self.update_time))

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
        _type_map = {
            "NewMessage": "new_message",
            "UpdatedMessage": "updated_message",
            "RemovedMessage": "removed_message",
            "InlineMessage": "inline_message",
        }
        event = _type_map.get(self.type)
        if event is None:
            raise UpdateTypeLookupError(f"Unknown update type: {self.type!r}")
        return event

    @property
    def event(self) -> RubikaObject:
        return cast(RubikaObject, getattr(self, self.event_type))


class UpdateTypeLookupError(LookupError):
    """Update does not contain any known event type."""