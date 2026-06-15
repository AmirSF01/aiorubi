from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from ..methods import (
        SendMessage
    )
    from .file import File
    from .location import Location
    from .aux_data import AuxData


class InlineMessage(RubikaObject):
    """
    This object represents a message when a user interacts with its inline keypad.

    Source: https://rubika.ir/botapi/models#inlinemessage
    """

    sender_id: str
    """Unique identifier of the user who clicked the button."""
    message_id: str
    """Unique identifier of the message containing the inline keypad."""
    chat_id: str
    """Unique identifier of the chat where the message is located."""
    text: str | None = None
    """*Optional*. Text of the message, if available."""
    file: File | None = None
    """*Optional*. File attached to the message, if available."""
    location: Location | None = None
    """*Optional*. Location attached to the message, if available."""
    aux_data: AuxData | None = None
    """*Optional*. Auxiliary data (like button_id) associated with the click."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            sender_id: str,
            message_id: str,
            chat_id: str,
            text: str | None = None,
            file: File | None = None,
            location: Location | None = None,
            aux_data: AuxData | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                sender_id=sender_id,
                message_id=message_id,
                chat_id=chat_id,
                text=text,
                file=file,
                location=location,
                aux_data=aux_data,
                **__pydantic_kwargs,
            )

    def answer(
        self,
        text: str,
        **kwargs: Any
    ) -> SendMessage:
        from aiorubi.methods import SendMessage

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendMessage(
            chat_id=self.chat_id,
            text=text,
            **kwargs
        ).as_(self._bot)

