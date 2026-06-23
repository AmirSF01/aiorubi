from __future__ import annotations

import io
import pathlib
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import metadata
from types import TracebackType
from typing import (
    Any,
    BinaryIO,
    Optional,
    TypeVar,
    Union,
    Literal,
)

import aiofiles

from aiorubi.utils.token import validate_token


from .session.aiohttp import AiohttpSession
from .session.base import BaseSession
from ..methods import (
    RubikaMethod,
    ForwardMessage,
    GetChat,
    GetFile,
    GetMe,
    GetUpdates,
    RequestSendFile,
    SendMessage,
    SendContact,
    SendPoll,
    SendLocation,
    DeleteMessage,
    EditMessageText,
    EditMessageKeypad,
    EditChatKeypad,
    SetCommands,
    UpdateBotEndpoints,
    BanChatMember,
    UnbanChatMember
)
from ..types import (
    BotInfo,
    DownloadUrl,
    GetUpdatesResponse,
    MessageID,
    Chat,
    Keypad,
    MetaData,
    InputFile,
    BotCommand,
    UpdateEndpointsStatus
)
from ..enums import (
    ChatKeypadType,
    UpdateEndpointType,
    PollType
)
from .default import Default, DefaultBotProperties

T = TypeVar("T")


class Bot:
    def __init__(
        self,
        token: str,
        session: BaseSession | None = None,
        default: DefaultBotProperties | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Bot class

        :param token: Rubika Bot token `Obtained from @BotFather <https://rubika.ir/BotFather>`_
        :param session: HTTP Client session (For example AiohttpSession).
            If not specified it will be automatically created.
        :param default: Default bot properties.
            If specified it will be propagated into the API methods at runtime.
        :raise TokenValidationError: When token has invalid format this exception will be raised
        """
        if session is None:
            session = AiohttpSession()
        if default is None:
            default = DefaultBotProperties()

        self.session = session

        self.default = default

        self.__token = token
        self._me: BotInfo | None = None

    async def __aenter__(self) -> Bot:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.session.close()

    @property
    def token(self) -> str:
        return self.__token

    @property
    def id(self) -> str:
        """
        Get bot ID

        :return:
        """
        return self._me.bot_id

    @asynccontextmanager
    async def context(self, auto_close: bool = True) -> AsyncIterator[Bot]:
        """
        Generate bot context

        :param auto_close: close session on exit
        :return:
        """
        try:
            yield self
        finally:
            if auto_close:
                await self.session.close()

    async def me(self) -> BotInfo:
        """
        Cached alias for getMe method

        :return:
        """
        if self._me is None:  # pragma: no cover
            self._me = await self.get_me()
        return self._me

    async def __call__(self, method: RubikaMethod[T], request_timeout: int | None = None) -> T:
        """
        Call API method

        :param method:
        :return:
        """
        return await self.session(self, method, timeout=request_timeout)

    def __hash__(self) -> int:
        """
        Get hash for the token

        :return:
        """
        return hash(self.__token)

    def __eq__(self, other: Any) -> bool:
        """
        Compare current bot with another bot instance

        :param other:
        :return:
        """
        if not isinstance(other, Bot):
            return False
        return hash(self) == hash(other)

    async def upload_file(
        self,
        url: str,
        file: InputFile,
        timeout: int = 30,
    ) -> dict[str, Any]:
        """
        Internal method to upload files to Rubika's storage.
        """
        return await self.session.upload_file(
            url=url,
            file=file,
            bot=self,
            timeout=timeout
        )

    async def get_me(
        self,
        request_timeout: int | None = None,
    ) -> BotInfo:
        call = GetMe()
        return await self(call, request_timeout=request_timeout)

    async def get_chat(
        self,
        chat_id: str,
        request_timeout: int | None = None,
    ) -> Chat:
        call = GetChat(chat_id=chat_id)
        return await self(call, request_timeout=request_timeout)

    async def get_file(
        self,
        file_id: str,
        request_timeout: int | None = None,
    ) -> DownloadUrl:
        """
        Get url of a file to download.
        """
        call = GetFile(
            file_id=file_id
        )
        return await self(call, request_timeout=request_timeout)

    async def get_updates(
        self,
        offset_id: str | None = None,
        limit: int | None = None,
        request_timeout: int | None = None,
    ) -> GetUpdatesResponse:
        call = GetUpdates(
            offset_id=offset_id,
            limit=limit,
        )
        return await self(call, request_timeout=request_timeout)

    async def set_commands(
        self,
        bot_commands: list[BotCommand],
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to change the list of the bot's commands.
        Returns :code:`True` on success.

        Source: https://botapi.rubika.ir/v3/setCommands

        :param bot_commands: A list of bot commands to be set as the list of the bot's commands.
        :param request_timeout: Request timeout
        :return: Returns :code:`True` on success.
        """

        call = SetCommands(
            bot_commands=bot_commands,
        )
        return await self(call, request_timeout=request_timeout)

    async def update_bot_endpoints(
        self,
        url: str,
        type: UpdateEndpointType,
        request_timeout: int | None = None,
    ) -> UpdateEndpointsStatus:
        """
        Use this method to update the bot's endpoint URLs for different event types.
        Returns :code:`True` on success.

        Source: https://rubika.ir/botapi/methods#url-endpoint

        :param url: The new endpoint URL
        :param type: The type of endpoint (e.g., UpdateEndpointType.RECEIVE_UPDATE)
        :param request_timeout: Request timeout
        :return: Returns :code:`True` on success.
        """

        call = UpdateBotEndpoints(
            url=url,
            type=type,
        )
        return await self(call, request_timeout=request_timeout)

    async def edit_chat_keypad(
        self,
        chat_id: str,
        chat_keypad: Keypad,
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to edit the chat's keypad.
        Returns :code:`True` on success.

        Source: https://rubika.ir/botapi/methods#keypad_2

        :param chat_id: Unique identifier for the target chat
        :param chat_keypad: The new keypad
        :param request_timeout: Request timeout
        :return: Returns :code:`True` on success.
        """

        call = EditChatKeypad(
            chat_id=chat_id,
            chat_keypad_type=ChatKeypadType.NEW,
            chat_keypad=chat_keypad,
        )
        return await self(call, request_timeout=request_timeout)

    async def remove_chat_keypad(
        self,
        chat_id: str,
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to remove the chat's keypad.
        Returns :code:`True` on success.

        Source: https://rubika.ir/botapi/methods#keypad_1

        :param chat_id: Unique identifier for the target chat
        :param request_timeout: Request timeout
        :return: Returns :code:`True` on success.
        """

        call = EditChatKeypad(
            chat_id=chat_id,
            chat_keypad_type=ChatKeypadType.REMOVE,
        )
        return await self(call, request_timeout=request_timeout)

    async def request_send_file(
        self,
        type: str,
        request_timeout: int | None = None,
    ):
        call = RequestSendFile(
            type=type
        )
        return await self(call, request_timeout=request_timeout)

    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_to_message_id: str | None = None,
        metadata: MetaData | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> MessageID:
        call = SendMessage(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            metadata=metadata,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
        )
        return await self(call, request_timeout=request_timeout)

    async def send_contact(
        self,
        chat_id: str,
        first_name: str,
        phone_number: str,
        last_name: str | None = None,
        reply_to_message_id: str | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> MessageID:
        call = SendContact(
            chat_id=chat_id,
            first_name=first_name,
            phone_number=phone_number,
            last_name=last_name,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
        )
        return await self(call, request_timeout=request_timeout)

    async def send_poll(
        self,
        chat_id: str,
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
        request_timeout: int | None = None,
    ) -> MessageID:
        call = SendPoll(
            chat_id=chat_id,
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
        )
        return await self(call, request_timeout=request_timeout)

    async def send_location(
        self,
        chat_id: str,
        latitude: str | float,
        longitude: str | float,
        reply_to_message_id: str | None = None,
        disable_notification: bool | None = None,
        inline_keypad: Keypad | None = None,
        chat_keypad: Keypad | None = None,
        chat_keypad_type: ChatKeypadType | None = None,
        request_timeout: int | None = None,
    ) -> MessageID:
        """
        Send a location.
        """
        call = SendLocation(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            reply_to_message_id=reply_to_message_id,
            disable_notification=disable_notification,
            inline_keypad=inline_keypad,
            chat_keypad=chat_keypad,
            chat_keypad_type=chat_keypad_type,
        )
        return await self(call, request_timeout=request_timeout)

    async def forward_message(
        self,
        from_chat_id: str,
        to_chat_id: str,
        message_id: str,
        disable_notification: bool = False,
        request_timeout: int | None = None,
    ) -> MessageID:
        """
        Forward messages of any kind.

        :param from_chat_id: Unique identifier for the chat where the original message was sent.
        :param to_chat_id: Unique identifier for the target chat.
        :param message_id: Message identifier in the chat specified in from_chat_id.
        :param disable_notification: Sends the message silently.
        :param request_timeout: Timeout for the request.
        :return: :class:`MessageID` object.
        """
        call = ForwardMessage(
            from_chat_id=from_chat_id,
            to_chat_id=to_chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
        )
        return await self(call, request_timeout=request_timeout)

    async def edit_message_text(
        self,
        chat_id: str,
        message_id: str,
        text: str,
        metadata: MetaData | None = None,
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to edit text messages.
        Returns :code:`True` on success.

        Source: https://rubika.ir/botapi/methods#_9

        :param text: New text of the message
        :param chat_id: Unique identifier for the target chat
        :param message_id: Identifier of the message to edit
        :param request_timeout: Request timeout
        :return: Returns :code:`True` on success.
        """

        call = EditMessageText(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            metadata=metadata,
        )
        return await self(call, request_timeout=request_timeout)

    async def edit_message_keypad(
        self,
        chat_id: str,
        message_id: str,
        inline_keypad: Keypad,
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to edit only the keypad of messages.
        Returns :code:`True` on success.

        Source: https://botapi.rubika.ir/v3/editMessageKeypad

        :param chat_id: Unique identifier for the target chat
        :param message_id: Identifier of the message to edit
        :param inline_keypad: The new keypad to replace the current inline keypad of the message.
        :param request_timeout: Request timeout
        :return: Returns :code:`True` on success.
        """

        call = EditMessageKeypad(
            chat_id=chat_id,
            message_id=message_id,
            inline_keypad=inline_keypad,
        )
        return await self(call, request_timeout=request_timeout)

    async def delete_message(
        self,
        chat_id: str,
        message_id: str,
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to delete a message, including service messages.
        Returns :code:`True` on success.

        Source: https://rubika.ir/botapi/methods#_10

        :param chat_id: Unique identifier for the target chat
        :param message_id: Identifier of the message to delete
        :param request_timeout: Request timeout
        :return: Returns :code:`True` on success.
        """

        call = DeleteMessage(
            chat_id=chat_id,
            message_id=message_id,
        )
        return await self(call, request_timeout=request_timeout)

    async def ban_chat_member(
        self,
        chat_id: str,
        user_id: str,
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to ban a user in a group or a channel.
        Returns :code:`True` on success.

        Source: https://rubika.ir/botapi/methods#_15
        """

        call = BanChatMember(
            chat_id=chat_id,
            user_id=user_id,
        )
        return await self(call, request_timeout=request_timeout)

    async def unban_chat_member(
        self,
        chat_id: str,
        user_id: str,
        request_timeout: int | None = None,
    ) -> bool:
        """
        Use this method to unban a user in a group or a channel.
        Returns :code:`True` on success.

        Source: https://rubika.ir/botapi/methods#_16
        """

        call = UnbanChatMember(
            chat_id=chat_id,
            user_id=user_id,
        )
        return await self(call, request_timeout=request_timeout)
