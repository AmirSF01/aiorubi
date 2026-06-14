from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaMethod
from ..types import Keypad
from ..enums import ChatKeypadType


class EditChatKeypad(RubikaMethod[bool]):
    """
    Use this method to edit or remove the chat's keypad.
    Returns :code:`True` on success.

    Source: https://rubika.ir/botapi/methods#keypad_1
    Source: https://rubika.ir/botapi/methods#keypad_2
    """

    __returning__ = bool
    __api_method__ = "editChatKeypad"

    chat_id: str
    """Unique identifier for the target chat"""
    chat_keypad_type: ChatKeypadType
    """The type of operation"""
    chat_keypad: Keypad | None = None
    """The new keypad (Required if chat_keypad_type is 'New')"""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            chat_keypad_type: ChatKeypadType,
            chat_keypad: Keypad | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                chat_keypad_type=chat_keypad_type,
                chat_keypad=chat_keypad,
                **__pydantic_kwargs,
            )