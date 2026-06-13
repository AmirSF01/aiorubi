from enum import Enum


class ButtonCalendarType(str, Enum):
    """
    This object represents a type of button calendar.

    Source: https://rubika.ir/botapi/models#enums
    """

    DATE_PERSIAN = "DatePersian"
    DATE_GREGORIAN = "DateGregorian"