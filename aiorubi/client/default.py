from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiorubi.utils.dataclass import dataclass_kwargs



# @dataclass ??
class Default:
    # Is not a dataclass because of JSON serialization.

    __slots__ = ("_name",)

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"Default({self._name!r})"

    def __repr__(self) -> str:
        return f"<{self}>"


@dataclass(**dataclass_kwargs(slots=True, kw_only=True))
class DefaultBotProperties:
    """
    Default bot properties.
    """

    parse_mode: str | None = None
    """Default parse mode for messages."""
    disable_notification: bool | None = None
    """Sends the message silently. Users will receive a notification with no sound."""
    allow_sending_without_reply: bool | None = None
    """Allows to send messages without reply."""

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item, None)