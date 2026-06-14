from __future__ import annotations
from typing import TYPE_CHECKING, Any, Literal

from .base import RubikaMethod
from ..types import MessageID, Keypad
from ..enums import ChatKeypadType, PollType

class SendPoll(RubikaMethod[MessageID]):
    __returning__ = MessageID
    __api_method__ = "sendPoll"

    chat_id: str
    """Unique identifier for the target chat"""
    question: str
    """Poll question"""
    options: list[str]
    """List of answer options"""
    type: PollType | None = None
    """*Optional*. Type of the poll"""
    allows_multiple_answers: bool | None = None
    """*Optional*. If True, users can select multiple answers"""
    is_anonymous: bool | None = None
    """*Optional*. If True, the poll is anonymous"""
    correct_option_index: int | None = None
    """*Optional*. Index of the correct answer option, required for Quiz type"""
    explanation: str | None = None
    """*Optional*. Explanation shown when a user chooses the wrong answer in a Quiz"""
    reply_to_message_id: str | None = None
    """*Optional*. ID of the message to reply to"""
    disable_notification: bool | None = None
    """*Optional*. If True, sends the message silently"""
    inline_keypad: Keypad | None = None
    """*Optional*. Inline keypad attached to the message"""
    chat_keypad: Keypad | None = None
    """*Optional*. Keypad attached to the chat"""
    chat_keypad_type: ChatKeypadType | None = None
    """*Optional*. Action to perform on the chat keypad"""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            chat_id: str,
            question: str,
            options: list[str],
            type: PollType | None = None,
            allows_multiple_answers: bool | None = None,
            is_anonymous: bool | None = None,
            correct_option_index: int | None = None,
            explanation: str | None = None,
            reply_to_message_id: str | None = None,
            disable_notification: bool | None = None,
            inline_keypad: Keypad | None = None,
            chat_keypad: Keypad | None = None,
            chat_keypad_type: ChatKeypadType | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                chat_id=chat_id,
                question=question,
                options=options,
                type=type,
                allows_multiple_answers=allows_multiple_answers,
                is_anonymous=is_anonymous,
                correct_option_index=correct_option_index,
                explanation=explanation,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
                inline_keypad=inline_keypad,
                chat_keypad=chat_keypad,
                chat_keypad_type=chat_keypad_type,
                **__pydantic_kwargs,
            )