from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    pass
    # from ..methods import LeaveChat, SendMessage


class Chat(RubikaObject):
    """
    This object represents a chat in Rubika.
    It can be a private conversation with a user, a group, or a channel.

    Source: https://rubika.ir/botapi/models#chat
    """

    chat_id: str
    """Unique identifier for this chat."""
    chat_type: str
    """Type of the chat, can be either 'User', 'Bot', 'Group' or 'Channel'"""
    user_id: str | None = None
    """*Optional*. Unique identifier for the user in private chats."""
    first_name: str | None = None
    """*Optional*. First name of the other party in a private chat."""
    last_name: str | None = None
    """*Optional*. Last name of the other party in a private chat."""
    title: str | None = None
    """*Optional*. Title, for groups and channels."""
    username: str | None = None
    """*Optional*. Username of the chat or user if available."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            chat_type: str,
            user_id: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            title: str | None = None,
            username: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            super().__init__(
                chat_id=chat_id,
                chat_type=chat_type,
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                title=title,
                username=username,
                **__pydantic_kwargs,
            )

    @property
    def full_name(self) -> str:
        """
        Get full name of the chat.

        For private chat it is first_name + last_name.
        For other chat types it is title.
        """
        if self.title is not None:
            return self.title
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name or ''}"

