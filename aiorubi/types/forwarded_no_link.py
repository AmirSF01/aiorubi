from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ForwardedNoLink(RubikaObject):
    """
    This object represents information about a forwarded message.
    """

    from_title: str
    """Title of the forward source."""

    if TYPE_CHECKING:
        def __init__(
                __pydantic__self__,
                *,
                type_from: str,
                message_id: str,
                from_chat_id: str,
                from_sender_id: str | None = None,
                **__pydantic_kwargs: Any,
        ) -> None:
            # Is needed only for type checking and IDE support without any additional plugins
            super().__init__(
                type_from=type_from,
                message_id=message_id,
                from_chat_id=from_chat_id,
                from_sender_id=from_sender_id,
                **__pydantic_kwargs,
            )