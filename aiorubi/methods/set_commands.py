from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaMethod
from ..types import BotCommand


class SetCommands(RubikaMethod[bool]):
    """
    Use this method to change the list of the bot's commands.
    Returns :code:`True` on success.

    Source: https://rubika.ir/botapi/methods#commands
    """

    __returning__ = bool
    __api_method__ = "setCommands"

    bot_commands: list[BotCommand]
    """A list of bot commands to be set as the list of the bot's commands."""

    if TYPE_CHECKING:

        def __init__(
            __pydantic__self__,
            *,
            bot_commands: list[BotCommand],
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                bot_commands=bot_commands,
                **__pydantic_kwargs,
            )