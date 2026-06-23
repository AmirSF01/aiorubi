from abc import ABC
from typing import cast

from aiorubi.filters import CommandObject
from aiorubi.handlers.base import BaseHandler, BaseHandlerMixin
from aiorubi.types import Message


class MessageHandler(BaseHandler[Message], ABC):
    """
    Base class for message handlers
    """

    @property
    def sender_id(self) -> str | None:
        return self.event.sender_id

    @property
    def chat_id(self) -> str | None:
        return self.event.chat_id


class MessageHandlerCommandMixin(BaseHandlerMixin[Message]):
    @property
    def command(self) -> CommandObject | None:
        if "command" in self.data:
            return cast(CommandObject, self.data["command"])
        return None