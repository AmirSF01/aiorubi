from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaMethod
from ..types import MetaData

class EditMessageText(RubikaMethod[bool]):
    """
    This method is used to edit the text of a message sent by the bot.
    On success, the edited Message is returned, otherwise True is returned.

    Source: https://rubika.ir/botapi/methods#_9
    """

    __returning__ = bool
    __api_method__ = "editMessageText"

    chat_id: str
    """Unique identifier for the target chat"""
    message_id: str
    """Identifier of the message to edit"""
    text: str
    """New text of the message"""
    metadata: MetaData | None = None
    """Formatting metadata for the new text (e.g. Bold, Italic, Mono)."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            message_id: str,
            text: str,
            metadata: MetaData | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                metadata=metadata,
                **__pydantic_kwargs,
            )