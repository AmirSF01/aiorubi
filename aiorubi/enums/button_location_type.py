from enum import Enum


class ButtonLocationType(str, Enum):
    """
    This object represents a type of button location.

    Source: https://rubika.ir/botapi/models#enums
    """

    PICKER = "Picker"
    VIEW = "View"