from __future__ import annotations
from typing import TYPE_CHECKING, Any

from .base import RubikaMethod
from ..types import Chat

class GetChat(RubikaMethod[Chat]):
    """
    This method returns full information about a specific chat.
    Includes ID, name, type, and settings.
    """
    __returning__ = Chat
    __api_method__ = "getChat"
    __returning_field__ = "chat"

    chat_id: str
    """Unique identifier for the target chat."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                **__pydantic_kwargs,
            )