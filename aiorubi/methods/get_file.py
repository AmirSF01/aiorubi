from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..types import DownloadUrl
from .base import RubikaMethod

class GetFile(RubikaMethod[DownloadUrl]):
    """
    Use this method to get the download URL of a file.
    Returns a :class:`aiorubi.types.DownloadUrl` object.
    """

    __returning__ = DownloadUrl
    __api_method__ = "getFile"

    file_id: str
    """Identifier of the file to get information about."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            file_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                file_id=file_id,
                **__pydantic_kwargs,
            )