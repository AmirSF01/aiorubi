from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaMethod


class UnbanChatMember(RubikaMethod[bool]):
    """
    Use this method to unban a user in a group or a channel.
    Returns :code:`True` on success.

    Source: https://rubika.ir/botapi/methods#_16
    """

    __returning__ = bool
    __api_method__ = "unbanChatMember"

    chat_id: str
    """Unique identifier for the target chat"""
    user_id: str
    """Unique identifier of the target user"""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            user_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                user_id=user_id,
                **__pydantic_kwargs,
            )