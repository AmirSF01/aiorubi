from enum import Enum


class ChatType(str, Enum):
    """
    This object represents a chat type.

    Source: https://rubika.ir/botapi/models#enums
    """

    USER = "User"
    BOT = "Bot"
    GROUP = "Group"
    CHANNEL = "Channel"