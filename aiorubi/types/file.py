from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class File(RubikaObject):
    """
    This object represents a file in Rubika.

    Source: https://rubika.ir/botapi/models#file
    """

    file_id: str
    """Unique identifier for this file."""
    file_name: str | None = None
    """*Optional*. File name."""
    size: str | int | None = None
    """*Optional*. File size in bytes."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            file_id: str,
            file_name: str | None = None,
            size: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            super().__init__(
                file_id=file_id,
                file_name=file_name,
                size=size,
                **__pydantic_kwargs,
            )