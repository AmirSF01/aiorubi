from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ButtonStringPicker(RubikaObject):
    """
    This object represents the settings for a string picker button.

    Source: https://rubika.ir/botapi/models#buttonstringpicker
    """

    items: list[str]
    """List of strings representing the selectable options."""
    default_value: str | None = None
    """*Optional*. The initial string value displayed to the user."""
    title: str | None = None
    """*Optional*. Title of the string picker button."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            items: list[str],
            default_value: str | None = None,
            title: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                items=items,
                default_value=default_value,
                title=title,
                **__pydantic_kwargs,
            )