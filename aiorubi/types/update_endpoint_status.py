from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject

from ..enums import UpdateEndpointStatusType

class UpdateEndpointsStatus(RubikaObject):
    status: UpdateEndpointStatusType
    """The status of the update process"""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            status: UpdateEndpointStatusType,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                status=status,
                **__pydantic_kwargs,
            )

    @property
    def is_done(self) -> bool:
        return self.status == UpdateEndpointStatusType.DONE
