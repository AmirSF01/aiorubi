from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaMethod
from ..types import Keypad


class EditMessageKeypad(RubikaMethod[bool]):
    """
    Use this method to edit only the reply markup of messages.
    Returns :code:`True` on success.

    Source: https://rubika.ir/botapi/methods#inline-keypad
    """

    __returning__ = bool
    __api_method__ = "editMessageKeypad"

    chat_id: str
    """Unique identifier for the target chat"""
    message_id: str
    """Identifier of the message to edit"""
    inline_keypad: Keypad
    """The new keypad to replace the current inline keypad of the message."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            message_id: str,
            inline_keypad: Keypad,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                message_id=message_id,
                inline_keypad=inline_keypad,
                **__pydantic_kwargs,
            )