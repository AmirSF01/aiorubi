from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import RubikaObject
from .custom import DateTime

if TYPE_CHECKING:
    from ..methods import (
        SendMessage
    )
    from .aux_data import AuxData
    from .file import File
    from .forwarded_from import ForwardedFrom
    from .forwarded_no_link import ForwardedNoLink
    from .location import Location
    from .sticker import Sticker
    from .contact_message import ContactMessage
    from .poll import Poll
    from .metadata import MetaData


class Message(RubikaObject):
    """
    This object represents a message in Rubika.

    Source: https://rubika.ir/botapi/models#message
    """

    message_id: str
    """Unique message identifier."""
    time: DateTime
    """Date the message was sent in Unix time."""
    chat_id: str | None = None
    """Unique identifier for the chat where the update occurred."""
    sender_type: str | None = None
    """Type of the message sender (e.g., User, Bot)."""
    sender_id: str | None = None
    """Unique identifier of the sender."""
    text: str | None = None
    """*Optional*. For text messages, the actual UTF-8 text of the message."""
    is_edited: bool | None = False
    """*Optional*. True, if the message was edited."""
    aux_data: AuxData | None = None
    """*Optional*. Auxiliary data associated with the message."""
    file: File | None = None
    """*Optional*. Message is a file, information about the file."""
    reply_to_message_id: str | None = None
    """*Optional*. For replies, identifier of the original message."""
    forwarded_from: ForwardedFrom | None = None
    """*Optional*. For forwarded messages, information about the original sender."""
    forwarded_no_link: ForwardedNoLink | str | None = None
    """*Optional*. Text to display instead of a user link for private forwarders."""
    location: Location | None = None
    """*Optional*. Message is a shared location, information about the location."""
    sticker: Sticker | None = None
    """*Optional*. Message is a sticker, information about the sticker."""
    contact_message: ContactMessage | None = None
    """*Optional*. Message is a shared contact, information about the contact."""
    poll: Poll | None = None
    """*Optional*. Message is a native poll, information about the poll."""
    metadata: MetaData | None = None
    """*Optional*. Special entities like bold, italic, links, etc. that appear in the text."""

    if TYPE_CHECKING:
        def __init__(
            __pydantic__self__,
            *,
            message_id: str,
            time: int,
            chat_id: str | None,
            sender_type: str,
            sender_id: str,
            text: str | None = None,
            is_edited: bool | None = False,
            aux_data: AuxData | None = None,
            file: File | None = None,
            reply_to_message_id: str | None = None,
            forwarded_from: ForwardedFrom | None = None,
            forwarded_no_link: str | None = None,
            location: Location | None = None,
            sticker: Sticker | None = None,
            contact_message: ContactMessage | None = None,
            poll: Poll | None = None,
            metadata: MetaData | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            super().__init__(
                message_id=message_id,
                time=time,
                chat_id=chat_id,
                sender_type=sender_type,
                sender_id=sender_id,
                text=text,
                is_edited=is_edited,
                aux_data=aux_data,
                file=file,
                reply_to_message_id=reply_to_message_id,
                forwarded_from=forwarded_from,
                forwarded_no_link=forwarded_no_link,
                location=location,
                sticker=sticker,
                contact_message=contact_message,
                poll=poll,
                metadata=metadata,
                **__pydantic_kwargs,
            )

    def answer(
        self,
        text: str,
        **kwargs: Any
    ) -> SendMessage:
        from aiorubi.methods import SendMessage

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendMessage(
            chat_id=self.chat_id,
            text=text,
            **kwargs
        ).as_(self._bot)

