from enum import Enum


class PollType(str, Enum):
    """
    This object represents a type of poll.
    """

    REGULAR = "Regular"
    QUIZ = "Quiz"
