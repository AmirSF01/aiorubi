from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..types import GetUpdatesResponse
from .base import RubikaMethod


class GetUpdates(RubikaMethod[GetUpdatesResponse]):
    """
    Use this method to receive incoming updates using polling.
    Returns a :class:`aiorubi.types.GetUpdatesResponse` object.

     **Notes**

     **1.** Use `next_offset_id` from the previous response as `offset_id` to prevent duplicates.

     **2.** Uses standard polling (not long polling); returns an immediate response.

    Source: https://rubika.ir/botapi/methods#_7
    """

    __returning__ = GetUpdatesResponse
    __api_method__ = "getUpdates"

    offset_id: str | None = None
    """Identifier of the update from which to start receiving. To get the next batch, use 'next_offset_id' from the previous response. If not specified, updates are returned starting from the oldest available update."""
    limit: int | None = None
    """Limits the number of updates to be retrieved."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            offset_id: str | None = None,
            limit: int | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                offset_id=offset_id,
                limit=limit,
                **__pydantic_kwargs,
            )