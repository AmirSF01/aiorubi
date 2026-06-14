from __future__ import annotations

from ..types import BotInfo
from .base import RubikaMethod


class GetMe(RubikaMethod[BotInfo]):
    """
    A simple method for testing your bot's auth token.
    Returns basic information about the bot in form of a Bot object.

    Source: https://rubika.ir/botapi/methods#getMe
    """

    __returning__ = BotInfo
    __api_method__ = "getMe"
    __returning_field__ = "bot"