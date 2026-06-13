from enum import Enum


class ButtonSelectionGet(str, Enum):
    """
    This object represents a get type for button selection.

    Source: https://rubika.ir/botapi/models#enums
    """
    LOCAL = "Local"
    API = "Api"