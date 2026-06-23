from abc import ABC

from aiorubi.handlers import BaseHandler
from aiorubi.types import Poll


class PollHandler(BaseHandler[Poll], ABC):
    """
    Base class for poll handlers
    """

    @property
    def question(self) -> str:
        return self.event.question

    @property
    def options(self) -> list[str]:
        return self.event.options