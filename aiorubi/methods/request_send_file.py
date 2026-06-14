from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..types import UploadUrl
from ..enums import FileType
from .base import RubikaMethod


class RequestSendFile(RubikaMethod[UploadUrl]):
    """
    Use this method to get an upload URL.
    Returns a :class:`aiorubi.types.UploadUrl` object.
    """

    __returning__ = UploadUrl
    __api_method__ = "requestSendFile"

    type: FileType

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            type: FileType,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                type=type,
                **__pydantic_kwargs,
            )