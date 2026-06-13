from enum import Enum


class PollStatus(str, Enum):
    """
    This object represents a status of a poll.

    Source: https://rubika.ir/botapi/models#enums
    """

    OPEN = "Open"
    CLOSED = "Closed"