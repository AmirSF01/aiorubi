from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..types import MessageID
from .base import RubikaMethod


class ForwardMessage(RubikaMethod[MessageID]):
    """
    Use this method to forward messages of any kind.
    On success, the sent :class:`aiorubi.types.MessageID` is returned.
    """

    __returning__ = MessageID
    __api_method__ = "forwardMessage"

    from_chat_id: str
    """Unique identifier for the chat where the original message was sent"""
    to_chat_id: str
    """Unique identifier for the target chat"""
    message_id: str
    """Message identifier in the chat specified in from_chat_id"""
    disable_notification: bool | None = None
    """Sends the message silently. Users will receive a notification with no sound."""

    if TYPE_CHECKING:
        def __init__(
                __pydantic__self__,
                *,
                from_chat_id: str,
                to_chat_id: str,
                message_id: str,
                disable_notification: bool | None = None,
                **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                from_chat_id=from_chat_id,
                to_chat_id=to_chat_id,
                message_id=message_id,
                disable_notification=disable_notification,
                **__pydantic_kwargs,
            )