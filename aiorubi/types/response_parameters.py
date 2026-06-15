from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject


class ResponseParameters(RubikaObject):
    """
    Describes why a request was unsuccessful.

    In Rubika, this model captures the error details provided in the
    'dev_message' and 'status' fields.
    """

    dev_message: str | None = None
    """*Optional*. Detailed error message from Rubika API."""
    retry_after: int | None = None
    """*Optional*. In case of exceeding flood control, the number of seconds left to wait before the request can be repeated"""
    migrate_to_chat_id: int | None = None
    """*Optional*. The group has been migrated to a supergroup with the specified identifier."""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
                __pydantic__self__,
                *,
                dev_message: str | None = None,
                retry_after: int | None = None,
                migrate_to_chat_id: int | None = None,
                **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                dev_message=dev_message,
                retry_after=retry_after,
                migrate_to_chat_id=migrate_to_chat_id,
                **__pydantic_kwargs,
            )