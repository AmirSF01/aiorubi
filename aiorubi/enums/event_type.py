from enum import Enum


class EventType(str, Enum):
    """
    Type of the event delivered in an `EventData` update (`event_data.type`).
    """

    BOT_JOINED = "BotJoined"
    """The bot was added to a chat."""
    BOT_PERMISSIONS_CHANGED = "BotPermissionsChanged"
    """The permissions of the bot in a chat were changed."""
    BOT_REMOVED = "BotRemoved"
    """The bot was removed from a chat."""