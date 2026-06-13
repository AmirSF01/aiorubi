from enum import Enum


class ForwardedFromType(str, Enum):
    """
    This object represents a type of forwarded message source.

    Source: https://rubika.ir/botapi/models#enums
    """

    USER = "User"
    BOT = "Bot"
    CHANNEL = "Channel"