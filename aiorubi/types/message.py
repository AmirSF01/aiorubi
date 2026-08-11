from __future__ import annotations

from typing import TYPE_CHECKING, Any, Coroutine

from .base import RubikaObject
from .custom import DateTime
from ..enums import FileType

if TYPE_CHECKING:
    from ..methods import (
        SendMessage,
        SendContact,
        SendPoll,
        SendLocation,
    )

    from .aux_data import AuxData
    from .file import File
    from .forwarded_from import ForwardedFrom
    from .forwarded_no_link import ForwardedNoLink
    from .keypad import Keypad
    from .location import Location
    from .sticker import Sticker
    from .contact_message import ContactMessage
    from .poll import Poll
    from .metadata import MetaData
    from .input_file import InputFile
    from .message_id import MessageID

    from ..enums import (
        ChatKeypadType,
        PollType
    )


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

    def reply(
        self,
        text: str,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any
    ) -> SendMessage:
        from aiorubi.methods import SendMessage

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendMessage(
            chat_id=self.chat_id,
            text=text,
            reply_to_message_id=self.message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)

    def answer(
        self,
        text: str,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any
    ) -> SendMessage:
        from aiorubi.methods import SendMessage

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendMessage(
            chat_id=self.chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)

    def reply_file(
        self,
        file: str | InputFile,
        file_type: FileType = FileType.FILE,
        text: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_file(
            chat_id=self.chat_id,
            file=file,
            file_type=file_type,
            text=text,
            reply_to_message_id=self.message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def answer_file(
        self,
        file: str | InputFile,
        file_type: FileType = FileType.FILE,
        text: str | None = None,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_file(
            chat_id=self.chat_id,
            file=file,
            file_type=file_type,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def reply_gif(
        self,
        gif: str | InputFile,
        text: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_gif(
            chat_id=self.chat_id,
            gif=gif,
            text=text,
            reply_to_message_id=self.message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def answer_gif(
        self,
        gif: str | InputFile,
        text: str | None = None,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_gif(
            chat_id=self.chat_id,
            gif=gif,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def reply_image(
        self,
        image: str | InputFile,
        text: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_image(
            chat_id=self.chat_id,
            image=image,
            text=text,
            reply_to_message_id=self.message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def answer_image(
        self,
        image: str | InputFile,
        text: str | None = None,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_image(
            chat_id=self.chat_id,
            image=image,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def reply_music(
        self,
        music: str | InputFile,
        text: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_music(
            chat_id=self.chat_id,
            music=music,
            text=text,
            reply_to_message_id=self.message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def answer_music(
        self,
        music: str | InputFile,
        text: str | None = None,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_music(
            chat_id=self.chat_id,
            music=music,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def reply_video(
        self,
        video: str | InputFile,
        text: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_video(
            chat_id=self.chat_id,
            video=video,
            text=text,
            reply_to_message_id=self.message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def answer_video(
        self,
        video: str | InputFile,
        text: str | None = None,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_video(
            chat_id=self.chat_id,
            video=video,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def reply_voice(
        self,
        voice: str | InputFile,
        text: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_voice(
            chat_id=self.chat_id,
            voice=voice,
            text=text,
            reply_to_message_id=self.message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def answer_voice(
        self,
        voice: str | InputFile,
        text: str | None = None,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> Coroutine[Any, Any, MessageID]:
        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return self._bot.send_voice(
            chat_id=self.chat_id,
            voice=voice,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            request_timeout=request_timeout,
        )

    def reply_contact(
        self,
        first_name: str,
        phone_number: str,
        last_name: str | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any,
    ) -> SendContact:
        from aiorubi.methods import SendContact

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendContact(
            chat_id=self.chat_id,
            first_name=first_name,
            phone_number=phone_number,
            last_name=last_name,
            reply_to_message_id=self.message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)

    def answer_contact(
        self,
        first_name: str,
        phone_number: str,
        last_name: str | None = None,
        reply_to_message_id: str | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any,
    ) -> SendContact:
        from aiorubi.methods import SendContact

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendContact(
            chat_id=self.chat_id,
            first_name=first_name,
            phone_number=phone_number,
            last_name=last_name,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)

    def reply_poll(
        self,
        question: str,
        options: list[str],
        type: PollType | None = None,
        allows_multiple_answers: bool | None = None,
        is_anonymous: bool | None = None,
        correct_option_index: int | None = None,
        explanation: str | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any,
    ) -> SendPoll:
        from aiorubi.methods import SendPoll

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendPoll(
            chat_id=self.chat_id,
            question=question,
            options=options,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            is_anonymous=is_anonymous,
            correct_option_index=correct_option_index,
            explanation=explanation,
            reply_to_message_id=self.message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)

    def answer_poll(
        self,
        question: str,
        options: list[str],
        type: PollType | None = None,
        allows_multiple_answers: bool | None = None,
        is_anonymous: bool | None = None,
        correct_option_index: int | None = None,
        explanation: str | None = None,
        reply_to_message_id: str | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any,
    ) -> SendPoll:
        from aiorubi.methods import SendPoll

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendPoll(
            chat_id=self.chat_id,
            question=question,
            options=options,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            is_anonymous=is_anonymous,
            correct_option_index=correct_option_index,
            explanation=explanation,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)

    def reply_location(
        self,
        latitude: str | float,
        longitude: str | float,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any,
    ) -> SendLocation:
        from aiorubi.methods import SendLocation

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendLocation(
            chat_id=self.chat_id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=self.message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)

    def answer_location(
        self,
        latitude: str | float,
        longitude: str | float,
        reply_to_message_id: str | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        **kwargs: Any,
    ) -> SendLocation:
        from aiorubi.methods import SendLocation

        assert self.chat_id is not None, (
            "This method can be used only if chat_id is present in the message."
        )

        return SendLocation(
            chat_id=self.chat_id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
            **kwargs
        ).as_(self._bot)
