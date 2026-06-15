from __future__ import annotations
from .base import RubikaObject
from .update import Update


class GetUpdatesResponse(RubikaObject):
    """
    This object represents the response from getUpdates method.
    It contains a list of updates and the ID for the next request.
    """

    updates: list[Update] = []
    """An array of incoming updates."""

    next_offset_id: str | None = None
    """The identifier to be used as 'offset_id' in the next request."""

    def __iter__(self):
        return iter(self.updates)

    def __getitem__(self, item: int | slice) -> Update | list[Update]:
        return self.updates.__getitem__(item)

    def __len__(self) -> int:
        return len(self.updates)