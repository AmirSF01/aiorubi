from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class Location(RubikaObject):
    """
    This object represents a geographic location.

    Source: https://rubika.ir/botapi/models#location
    """

    longitude: str | float
    """Longitude as defined by sender."""
    latitude: str | float
    """Latitude as defined by sender."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            longitude: str,
            latitude: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                longitude=longitude,
                latitude=latitude,
                **__pydantic_kwargs,
            )