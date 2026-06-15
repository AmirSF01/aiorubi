from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ForwardedFrom(RubikaObject):
    """
    This object represents information about a forwarded message.

    Source: https://rubika.ir/botapi/models#forwardedfrom
    """

    type_from: str
    """Type of the forward source (User, Channel or Bot)."""
    message_id: str
    """Identifier of the original message that was forwarded."""
    from_chat_id: str | None = None
    """Identifier of the source chat from which the message was forwarded."""
    from_sender_id: str | None = None
    """*Optional*. Identifier of the original sender of the message."""

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