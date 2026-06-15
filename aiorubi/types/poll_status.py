from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class PollStatus(RubikaObject):
    """
    This object contains the current status of a poll.

    Source: https://rubika.ir/botapi/models#pollstatus
    """

    state: str
    """Current state of the poll (e.g., 'Open' or 'Closed')."""
    selection_index: int
    """Index of the option chosen by the user. Returns -1 if no option is selected."""
    percent_vote_options: list[int]
    """List of vote percentages for each option."""
    total_vote: int
    """Total number of votes cast in the poll."""
    show_total_votes: bool
    """True, if the total number of votes should be displayed to the user."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            state: str,
            selection_index: int,
            percent_vote_options: list[int],
            total_vote: int,
            show_total_votes: bool,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                state=state,
                selection_index=selection_index,
                percent_vote_options=percent_vote_options,
                total_vote=total_vote,
                show_total_votes=show_total_votes,
                **__pydantic_kwargs,
            )