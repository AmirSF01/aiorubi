from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import RubikaObject

class UploadUrl(RubikaObject):
    upload_url: str

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            upload_url: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(upload_url=upload_url, **__pydantic_kwargs)