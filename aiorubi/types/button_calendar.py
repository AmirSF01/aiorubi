from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ButtonCalendar(RubikaObject):
    """
    This object represents the settings for a calendar button.

    Source: https://rubika.ir/botapi/models#buttoncalendar
    """

    type: str
    """Type of the calendar (e.g., Persian or Gregorian)."""
    min_year: str
    """Minimum selectable year in the calendar."""
    max_year: str
    """Maximum selectable year in the calendar."""
    title: str
    """Title of the calendar button."""
    default_value: str | None = None
    """*Optional*. Initial date displayed to the user."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            type: str,
            min_year: str,
            max_year: str,
            title: str,
            default_value: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                min_year=min_year,
                max_year=max_year,
                title=title,
                default_value=default_value,
                **__pydantic_kwargs,
            )