from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .keypad import Keypad


class MessageKeypadUpdate(RubikaObject):
    """
    This object is used to update an inline keypad in response to a button click.

    Source: https://rubika.ir/botapi/models#messagekeypadupdate
    """

    message_id: str
    """Unique identifier of the message whose keypad is being updated."""
    inline_keypad: Keypad
    """The new inline keypad to replace the existing one."""

    if TYPE_CHECKING:
        def __init__(
                __pydantic__self__,
                *,
                message_id: str,
                inline_keypad: Keypad,
                **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                message_id=message_id,
                inline_keypad=inline_keypad,
                **__pydantic_kwargs,
            )