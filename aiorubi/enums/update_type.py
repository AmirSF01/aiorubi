from enum import Enum


class UpdateType(str, Enum):
    """
    This object represents a type of update.

    Source: https://rubika.ir/botapi/models#enums
    """

    NEW_MESSAGE = "NewMessage"
    UPDATED_MESSAGE = "UpdatedMessage"
    REMOVED_MESSAGE = "RemovedMessage"

    INLINE_MESSAGE = "InlineMessage"
    """Added for abstraction (not in official API)."""

    STARTED_BOT = "StartedBot"
    STOPPED_BOT = "StoppedBot"