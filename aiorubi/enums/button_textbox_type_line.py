from enum import Enum


class ButtonTextboxTypeLine(str, Enum):
    """
    This object represents an input line mode for textbox button.

    Source: https://rubika.ir/botapi/models#enums
    """

    SINGLE_LINE = "SingleLine"
    MULTI_LINE = "MultiLine"