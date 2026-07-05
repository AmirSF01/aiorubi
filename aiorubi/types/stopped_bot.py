from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from ..methods import GetChat


class StoppedBot(RubikaObject):
    """
    This object represents the event where a user stopped (blocked) the bot.
    """

    chat_id: str
    """Unique identifier of the chat that stopped the bot."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                **__pydantic_kwargs,
            )
