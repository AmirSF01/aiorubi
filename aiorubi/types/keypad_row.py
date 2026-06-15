from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .button import Button


class KeypadRow(RubikaObject):
    """
    This object represents a row of buttons in a keypad.

    Source: https://rubika.ir/botapi/models#keypadrow
    """

    buttons: list[Button]
    """List of buttons in a single row."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            buttons: list[Button],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                buttons=buttons,
                **__pydantic_kwargs,
            )