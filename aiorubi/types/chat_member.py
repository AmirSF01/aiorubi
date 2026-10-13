from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ChatMember(RubikaObject):
    """
    This object represents information about a member of a chat.

    Source: https://rubika.ir/botapi/models#chatmember
    """

    user_id: str
    """Unique identifier for this user."""
    status: str
    """The member's status in the chat, e.g. `Admin`."""
    access_list: list[str] | None = None
    """*Optional*. List of access permissions granted to the member."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            user_id: str,
            status: str,
            access_list: list[str] | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                user_id=user_id,
                status=status,
                access_list=access_list,
                **__pydantic_kwargs,
            )