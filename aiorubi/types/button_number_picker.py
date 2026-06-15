from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ButtonNumberPicker(RubikaObject):
    """
    This object represents the settings for a number picker button.

    Source: https://rubika.ir/botapi/models#buttonnumberpicker
    """

    min_value: int | str
    """Minimum selectable value."""
    max_value: int | str
    """Maximum selectable value."""
    title: str
    """Title of the button."""
    default_value: int | str | None = None
    """*Optional*. Initial value displayed to the user."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            min_value: int | str,
            max_value: int | str,
            title: str,
            default_value: int | str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                min_value=min_value,
                max_value=max_value,
                title=title,
                default_value=default_value,
                **__pydantic_kwargs,
            )