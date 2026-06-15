from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .location import Location


class ButtonLocation(RubikaObject):
    """
    This object represents the settings for a location input button.

    Source: https://rubika.ir/botapi/models#buttonlocation
    """

    default_pointer_location: Location
    """The initial coordinates for the map pointer."""
    default_map_location: Location
    """The initial coordinates for the center of the map view."""
    type: str
    """Type of map interaction (e.g., Pick or View)."""
    title: str | None = None
    """*Optional*. Title of the location button."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            default_pointer_location: Location,
            default_map_location: Location,
            type: str,
            title: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                default_pointer_location=default_pointer_location,
                default_map_location=default_map_location,
                type=type,
                title=title,
                **__pydantic_kwargs,
            )