from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ButtonSelectionItem(RubikaObject):
    """
    This object represents an item in a selection list.

    Source: https://rubika.ir/botapi/models#buttonselectionitem
    """

    text: str
    """Text of the button."""
    type: str
    """Type of the button selection display."""
    image_url: str | None = None
    """*Optional*. URL of the image associated with the option."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            text: str,
            type: str,
            image_url: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                text=text,
                type=type,
                image_url=image_url,
                **__pydantic_kwargs,
            )