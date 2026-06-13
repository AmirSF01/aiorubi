from enum import Enum


class ButtonSelectionSearch(str, Enum):
    """
    This object represents a search type for button selection.

    Source: https://rubika.ir/botapi/models#enums
    """
    NONE = "None"
    LOCAL = "Local"
    API = "Api"