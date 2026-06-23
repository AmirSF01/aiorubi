from __future__ import annotations
from typing import TYPE_CHECKING, Any

from .base import RubikaMethod
from ..types import MessageID, Keypad
from ..enums import ChatKeypadType

class SendLocation(RubikaMethod[MessageID]):
    __returning__ = MessageID
    __api_method__ = "sendLocation"

    chat_id: str
    """Unique identifier for the target chat"""
    latitude: str | float
    """Latitude of the location"""
    longitude: str | float
    """Longitude of the location"""
    reply_to_message_id: str | None = None
    """*Optional*. ID of the message to reply to"""
    disable_notification: bool | None = None
    """*Optional*. If True, sends the message silently"""
    inline_keypad: Keypad | None = None
    """*Optional*. Inline keypad attached to the message"""
    chat_keypad: Keypad | None = None
    """*Optional*. Keypad attached to the chat"""
    chat_keypad_type: ChatKeypadType | None = None
    """*Optional*. Action to perform on the chat keypad"""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            latitude: str | float,
            longitude: str | float,
            reply_to_message_id: str | None = None,
            disable_notification: bool | None = None,
            inline_keypad: Keypad | None = None,
            chat_keypad: Keypad | None = None,
            chat_keypad_type: ChatKeypadType | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                latitude=latitude,
                longitude=longitude,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
                inline_keypad=inline_keypad,
                chat_keypad=chat_keypad,
                chat_keypad_type=chat_keypad_type,
                **__pydantic_kwargs,
            )