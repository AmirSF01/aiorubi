from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .button_selection import ButtonSelection
    from .button_calendar import ButtonCalendar
    from .button_number_picker import ButtonNumberPicker
    from .button_string_picker import ButtonStringPicker
    from .button_location import ButtonLocation
    from .button_textbox import ButtonTextbox


class Button(RubikaObject):
    """
    This object represents an interactive button in a message or keypad.

    Source: https://rubika.ir/botapi/models#button
    """

    id: str
    """Unique identifier for the button."""
    type: str
    """Type of the button (defines its behavior)."""
    button_text: str
    """Text displayed on the button."""
    button_selection: ButtonSelection | None = None
    """*Optional*. Data for a selection list button."""
    button_calendar: ButtonCalendar | None = None
    """*Optional*. Data for a calendar button."""
    button_number_picker: ButtonNumberPicker | None = None
    """*Optional*. Data for a number picker button."""
    button_string_picker: ButtonStringPicker | None = None
    """*Optional*. Data for a string picker button."""
    button_location: ButtonLocation | None = None
    """*Optional*. Data for a location selection button."""
    button_textbox: ButtonTextbox | None = None
    """*Optional*. Data for a text input button."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            id: str,
            type: str,
            button_text: str,
            button_selection: ButtonSelection | None = None,
            button_calendar: ButtonCalendar | None = None,
            button_number_picker: ButtonNumberPicker | None = None,
            button_string_picker: ButtonStringPicker | None = None,
            button_location: ButtonLocation | None = None,
            button_textbox: ButtonTextbox | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                id=id,
                type=type,
                button_text=button_text,
                button_selection=button_selection,
                button_calendar=button_calendar,
                button_number_picker=button_number_picker,
                button_string_picker=button_string_picker,
                button_location=button_location,
                button_textbox=button_textbox,
                **__pydantic_kwargs,
            )