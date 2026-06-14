from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .base import RubikaMethod
from ..types import MessageID, Keypad, MetaData
from ..enums import ChatKeypadType


class SendFile(RubikaMethod[MessageID]):
    """
    Use this method to send a file from the bot to a chat.
    Returns the sent :class:`MessageID` on success.

    Source: https://rubika.ir/botapi/methods#send-file
    """

    __returning__ = MessageID
    __api_method__ = "sendFile"

    chat_id: str
    """Unique identifier for the target chat"""
    file_id: str
    """Identifier of the file to send"""
    text: str | None = None
    """*Optional*. Caption of the file"""
    reply_to_message_id: str | None = None
    """*Optional*. ID of the message to reply to"""
    metadata: MetaData | None = None
    """*Optional*. Formatting metadata for the text (e.g. Bold, Italic, Mono)."""
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
            file_id: str,
            text: str | None = None,
            reply_to_message_id: str | None = None,
            metadata: MetaData | None = None,
            disable_notification: bool | None = None,
            inline_keypad: Keypad | None = None,
            chat_keypad: Keypad | None = None,
            chat_keypad_type: ChatKeypadType | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                file_id=file_id,
                text=text,
                reply_to_message_id=reply_to_message_id,
                metadata=metadata,
                disable_notification=disable_notification,
                inline_keypad=inline_keypad,
                chat_keypad=chat_keypad,
                chat_keypad_type=chat_keypad_type,
                **__pydantic_kwargs,
            )