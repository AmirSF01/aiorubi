from enum import Enum


class ButtonSelectionType(str, Enum):
    """
    This object represents a type of button selection display.

    Source: https://rubika.ir/botapi/models#enums
    """

    TEXT_ONLY = "TextOnly"
    TEXT_IMG_THU = "TextImgThu"
    TEXT_IMG_BIG = "TextImgBig"