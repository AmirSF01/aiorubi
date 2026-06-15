from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .file import File


class BotInfo(RubikaObject):
    """
    This object represents a Rubika bot's public information.

    Source: https://rubika.ir/botapi/models#bot
    """

    bot_id: str
    """Unique identifier for this bot."""
    bot_title: str
    """Display title of the bot."""
    avatar: File | None = None
    """*Optional*. Bot's profile picture."""
    description: str | None = None
    """*Optional*. Bot's description."""
    username: str | None = None
    """*Optional*. Bot's username."""
    start_message: str | None = None
    """*Optional*. The message shown to users when they start the bot."""
    share_url: str | None = None
    """*Optional*. Shareable link for the bot."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            bot_id: str,
            bot_title: str,
            avatar: File | None = None,
            description: str | None = None,
            username: str | None = None,
            start_message: str | None = None,
            share_url: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                bot_id=bot_id,
                bot_title=bot_title,
                avatar=avatar,
                description=description,
                username=username,
                start_message=start_message,
                share_url=share_url,
                **__pydantic_kwargs,
            )