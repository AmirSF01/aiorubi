from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ButtonTextbox(RubikaObject):
    """
    This object represents the settings for a textbox input button.

    Source: https://rubika.ir/botapi/models#buttontextbox
    """

    type_line: str
    """Determines if the text input is single-line or multi-line."""
    type_keypad: str
    """Type of keypad displayed for text input (e.g., String or Numeric)."""
    place_holder: str | None = None
    """*Optional*. Placeholder text displayed in the input field."""
    title: str | None = None
    """*Optional*. Title of the textbox button."""
    default_value: str | None = None
    """*Optional*. Initial value displayed in the textbox."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            type_line: str,
            type_keypad: str,
            place_holder: str | None = None,
            title: str | None = None,
            default_value: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type_line=type_line,
                type_keypad=type_keypad,
                place_holder=place_holder,
                title=title,
                default_value=default_value,
                **__pydantic_kwargs,
            )