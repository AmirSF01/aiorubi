from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject
from ..enums import EventType


class EventData(RubikaObject):
    """
    This object is received as `event_data` when an event happens in a Rubika chat,
    e.g. when the bot is added to a chat, its permissions are changed, or it is removed.
    """

    type: EventType
    """Type of the event: `BotJoined`, `BotPermissionsChanged` or `BotRemoved`."""
    access_list: list[str] | None = None
    """List of permissions currently granted to the bot,
    e.g. `DeleteGlobalAllMessages`, `ViewMembers`, `EditAllMessages`, `SendMessages`.
    Not present for `BotRemoved`."""
    join_type: str | None = None
    """How the bot is a member of the chat, e.g. `Admin` or `Member`.
    Not present for `BotRemoved`."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            type: EventType,
            access_list: list[str] | None = None,
            join_type: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                access_list=access_list,
                join_type=join_type,
                **__pydantic_kwargs,
            )