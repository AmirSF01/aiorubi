from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .button_selection_item import ButtonSelectionItem


class ButtonSelection(RubikaObject):
    """
    This object represents the settings for a selection button.

    Source: https://rubika.ir/botapi/models#buttonselection
    """

    selection_id: str
    """Unique identifier for the selection list."""
    search_type: str
    """Type of search functionality."""
    get_type: str
    """Type of item retrieval (e.g., Offline/Sync)."""
    items: list[ButtonSelectionItem]
    """List of items to be displayed in the selection."""
    is_multi_selection: bool
    """True, if the user can select multiple options."""
    columns_count: str
    """Number of columns to display items in."""
    title: str | None = None
    """*Optional*. Title of the selection menu."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            selection_id: str,
            search_type: str,
            get_type: str,
            items: list[ButtonSelectionItem],
            is_multi_selection: bool,
            columns_count: str,
            title: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            
            super().__init__(
                selection_id=selection_id,
                search_type=search_type,
                get_type=get_type,
                items=items,
                is_multi_selection=is_multi_selection,
                columns_count=columns_count,
                title=title,
                **__pydantic_kwargs,
            )