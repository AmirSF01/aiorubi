from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class AuxData(RubikaObject):
    """
    This object represents auxiliary data associated with messages and button clicks.

    Source: https://rubika.ir/botapi/models#auxdata
    """

    start_id: str | None = None
    """Optional. The start parameter from a deep link (e.g., st=...)."""
    button_id: str | None = None
    """Optional. The identifier of the button that was clicked."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            start_id: str | None = None,
            button_id: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                start_id=start_id,
                button_id=button_id,
                **__pydantic_kwargs,
            )