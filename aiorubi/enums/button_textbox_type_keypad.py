from enum import Enum


class ButtonTextboxTypeKeypad(str, Enum):
    """
    This object represents a type of keypad for textbox button.

    Source: https://rubika.ir/botapi/models#enums
    """

    STRING = "String"
    NUMBER = "Number"