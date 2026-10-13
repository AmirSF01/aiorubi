from __future__ import annotations
from typing import TYPE_CHECKING, Any

from .base import RubikaMethod
from ..types import ChatMember

class GetChatMember(RubikaMethod[ChatMember]):
    """
    This method returns information about a specific member of a chat.
    Includes user ID, status, and access permissions.

    Source: https://rubika.ir/botapi/methods#getchatmember
    """
    __returning__ = ChatMember
    __api_method__ = "getChatMember"
    __returning_field__ = "chat_member"

    chat_id: str
    """Unique identifier for the target chat."""
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