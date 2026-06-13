from enum import Enum


class MessageSenderType(str, Enum):
    """
    This object represents a type of message sender.

    Source: https://rubika.ir/botapi/models#enums
    """

    USER = "User"
    BOT = "Bot"