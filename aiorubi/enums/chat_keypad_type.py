from enum import Enum


class ChatKeypadType(str, Enum):
    """
    This object represents a type of chat keypad update.

    Source: https://rubika.ir/botapi/models#enums
    """

    NONE = "None"
    NEW = "New"
    REMOVE = "Remove"