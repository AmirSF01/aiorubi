from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .file import File


class Sticker(RubikaObject):
    """
    This object represents a sticker.

    Source: https://rubika.ir/botapi/models#sticker
    """

    sticker_id: str
    """Unique identifier for this sticker."""
    file: File
    """Information about the sticker file."""
    emoji_character: str | None = None
    """*Optional*. Emoji associated with the sticker."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            sticker_id: str,
            file: File,
            emoji_character: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                sticker_id=sticker_id,
                file=file,
                emoji_character=emoji_character,
                **__pydantic_kwargs,
            )