from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ContactMessage(RubikaObject):
    """
    This object represents a shared contact.

    Source: https://rubika.ir/botapi/models#contactmessage
    """

    phone_number: str
    """Contact's phone number."""
    first_name: str
    """Contact's first name."""
    last_name: str | None = None
    """*Optional*. Contact's last name."""

    if TYPE_CHECKING:
        
        def __init__(
            __pydantic__self__,
            *,
            phone_number: str,
            first_name: str,
            last_name: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                **__pydantic_kwargs,
            )