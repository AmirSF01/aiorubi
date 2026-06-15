from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .keypad_row import KeypadRow


class Keypad(RubikaObject):
    """
    This object represents a keypad (inline or chat) with rows of buttons.

    Source: https://rubika.ir/botapi/models#keypad
    """

    rows: list[KeypadRow]
    """List of keypad rows, each containing buttons."""
    resize_keyboard: bool | None = False
    """*Optional*. Requests clients to rescale the keypad vertically for optimal fit."""
    one_time_keyboard: bool | None = False
    """*Optional*. Requests clients to hide the keypad as soon as it's been used."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            rows: list[KeypadRow],
            resize_keyboard: bool | None = False,
            one_time_keyboard: bool | None = False,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                rows=rows,
                resize_keyboard=resize_keyboard,
                one_time_keyboard=one_time_keyboard,
                **__pydantic_kwargs,
            )