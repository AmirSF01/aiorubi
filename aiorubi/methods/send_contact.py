from __future__ import annotations
from typing import TYPE_CHECKING, Any
from .base import RubikaMethod
from ..types import MessageID, Keypad
from ..enums import ChatKeypadType

class SendContact(RubikaMethod[MessageID]):
    __returning__ = MessageID
    __api_method__ = "sendContact"

    chat_id: str
    first_name: str
    phone_number: str
    last_name: str | None = None
    reply_to_message_id: str | None = None
    disable_notification: bool | None = None
    inline_keypad: Keypad | None = None
    chat_keypad: Keypad | None = None
    chat_keypad_type: ChatKeypadType | None = None

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            first_name: str,
            phone_number: str,
            last_name: str | None = None,
            reply_to_message_id: str | None = None,
            disable_notification: bool | None = None,
            inline_keypad: Keypad | None = None,
            chat_keypad: Keypad | None = None,
            chat_keypad_type: ChatKeypadType | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                first_name=first_name,
                phone_number=phone_number,
                last_name=last_name,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
                inline_keypad=inline_keypad,
                chat_keypad=chat_keypad,
                chat_keypad_type=chat_keypad_type,
                **__pydantic_kwargs,
            )