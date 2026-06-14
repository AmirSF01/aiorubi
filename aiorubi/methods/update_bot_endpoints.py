from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaMethod

from ..types import UpdateEndpointsStatus
from ..enums import UpdateEndpointType


class UpdateBotEndpoints(RubikaMethod[UpdateEndpointsStatus]):
    """
    Use this method to update the bot's endpoint URLs.
    Returns :code:`True` on success.

    Source: https://rubika.ir/botapi/methods#url-endpoint
    """

    __returning__ = UpdateEndpointsStatus
    __api_method__ = "updateBotEndpoints"

    url: str
    """The new endpoint URL"""
    type: UpdateEndpointType
    """The type of endpoint"""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            url: str,
            type: UpdateEndpointType,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                url=url,
                type=type,
                **__pydantic_kwargs,
            )