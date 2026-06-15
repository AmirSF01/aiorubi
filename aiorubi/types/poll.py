from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

if TYPE_CHECKING:
    from .poll_status import PollStatus


class Poll(RubikaObject):
    """
    This object contains information about a poll.

    Source: https://rubika.ir/botapi/models#poll
    """

    question: str
    """The question of the poll."""
    options: list[str]
    """List of poll options."""
    poll_status: PollStatus
    """Current status of the poll."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            question: str,
            options: list[str],
            poll_status: PollStatus,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                question=question,
                options=options,
                poll_status=poll_status,
                **__pydantic_kwargs,
            )