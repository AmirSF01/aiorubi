from __future__ import annotations
from typing import Any, TYPE_CHECKING
from .base import RubikaObject

class DownloadUrl(RubikaObject):
    download_url: str

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            download_url: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(download_url=download_url, **__pydantic_kwargs)