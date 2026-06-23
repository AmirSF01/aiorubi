from abc import ABC

from aiorubi.handlers import BaseHandler
from aiorubi.types import InlineMessage


class InlineMessageHandler(BaseHandler[InlineMessage], ABC):
    """
    Base class for inline message (button click) handlers.

    Example:
        .. code-block:: python

            from aiorubi.handlers import InlineMessageHandler

            ...

            @router.inline_message()
            class MyHandler(InlineMessageHandler):
                async def handle(self) -> Any: ...
    """

    @property
    def sender_id(self) -> str:
        """
        Is alias for `event.sender_id`
        """
        return self.event.sender_id

    @property
    def chat_id(self) -> str:
        """
        Is alias for `event.chat_id`
        """
        return self.event.chat_id

    @property
    def button_id(self) -> str | None:
        """
        Is alias for `event.aux_data.button_id`
        """
        if self.event.aux_data:
            return self.event.aux_data.button_id
        return None