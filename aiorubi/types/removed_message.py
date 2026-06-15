from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class RemovedMessage(RubikaObject):
    """
    This object is received when a message is deleted in a Rubika chat.

    Source: https://rubika.ir/botapi/models#update
    """

    message_id: str
    """Unique identifier of the removed message."""
    chat_id: str | None = None
    """Unique identifier of the chat where the message was removed.
    Injected automatically from the parent Update object."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            message_id: str,
            chat_id: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                message_id=message_id,
                chat_id=chat_id,
                **__pydantic_kwargs,
            )