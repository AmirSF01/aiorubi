from __future__ import annotations
from typing import Any, TYPE_CHECKING
from pydantic import Field, AliasChoices
from .base import RubikaObject

class MessageID(RubikaObject):
    message_id: str = Field(validation_alias=AliasChoices('message_id', 'new_message_id'))

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            message_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(message_id=message_id, **__pydantic_kwargs)