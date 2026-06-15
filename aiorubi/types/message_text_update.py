from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class MessageTextUpdate(RubikaObject):
    """
    This object represents a text update for a message.
    It is returned when the text of a message changes as a result of interaction
    with an Inline Keypad.

    Source: https://rubika.ir/botapi/models#messagetextupdate
    """

    message_id: str
    """Unique identifier of the message that was updated."""
    text: str
    """The new text of the message after the update."""

    if TYPE_CHECKING:
        
        def __init__(
            __pydantic__self__,
            *,
            message_id: str,
            text: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            super().__init__(
                message_id=message_id,
                text=text,
                **__pydantic_kwargs,
            )