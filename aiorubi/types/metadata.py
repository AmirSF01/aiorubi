from __future__ import annotations

from typing import Any, List, TYPE_CHECKING

from pydantic import Field, RootModel, model_serializer, model_validator

from .base import MutableRubikaObject
from ..enums import MetadataType


class MetaDataPart(MutableRubikaObject):
    """
    Represents a single formatting entity within a message text.

    This model includes fields discovered through community research and
    reverse engineering, as some are not officially documented in
    the Rubika Bot API docs.
    """

    type: MetadataType
    """Type of the entity (e.g., 'Bold', 'Italic', 'Link', 'MentionText')"""
    from_index: int
    """Offset in UTF-16 code units to the start of the entity"""
    length: int
    """Length of the entity in UTF-16 code units"""

    link_url: str | None = None
    """*Optional*. URL for 'Link' type entities. (Not found in official docs)"""
    mention_text_user_id: str | None = None
    """*Optional*. Target User ID for 'MentionText' entities. (Not found in official docs)"""

    if TYPE_CHECKING:
        def __init__(
                __pydantic__self__,
                *,
                type: str,
                from_index: int,
                length: int,
                link_url: str | None = None,
                mention_text_user_id: str | None = None,
                **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                type=type,
                from_index=from_index,
                length=length,
                link_url=link_url,
                mention_text_user_id=mention_text_user_id,
                **__pydantic_kwargs,
            )


class MetaData(RootModel):
    """
    A smart container for MetaDataPart objects.

    This model acts as a List in Python but automatically wraps/unwraps
    the 'meta_data_parts' layer required by Rubika's API.

    Note: The 'metadata' wrapper structure is undocumented in some parts
    of the official Rubika API reference.
    """

    root: List[MetaDataPart] = Field(default_factory=list)

    @property
    def meta_data_parts(self) -> List[MetaDataPart]:
        return self.root

    @model_validator(mode="before")
    @classmethod
    def unwrap_metadata(cls, data: Any) -> Any:
        """
        Unwraps the 'meta_data_parts' key if the incoming data is a dict.
        This ensures the model can be initialized from raw API responses.
        """
        if isinstance(data, dict) and "meta_data_parts" in data:
            return data["meta_data_parts"]
        return data

    @model_serializer
    def wrap_metadata(self) -> dict[str, Any]:
        """
        Wraps the list into the 'meta_data_parts' key during serialization.
        This prepares the data for the Rubika API request format.
        """
        return {
            "meta_data_parts": [
                item.model_dump(exclude_none=True) for item in self.root
            ]
        }

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def __repr__(self) -> str:
        return f"{self.root!r}"