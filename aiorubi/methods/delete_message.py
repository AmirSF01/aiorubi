from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaMethod


class DeleteMessage(RubikaMethod[bool]):
    """
    Use this method to delete a message, including service messages.
    Returns :code:`True` on success.

    Source: https://rubika.ir/botapi/methods#_10
    """

    __returning__ = bool
    __api_method__ = "deleteMessage"

    chat_id: str
    """Unique identifier for the target chat"""
    message_id: str
    """Identifier of the message to delete"""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            message_id: str,
            **__pydantic_kwargs: Any
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                message_id=message_id,
                **__pydantic_kwargs
            )