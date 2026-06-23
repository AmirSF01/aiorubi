from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import model_validator

from aiorubi.client.context_controller import BotContextController
from ..types import InputFile
from ..types.base import UNSET_TYPE

if TYPE_CHECKING:
    from ..client.bot import Bot

RubikaType = TypeVar("RubikaType", bound=Any)


class Request(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    method: str
    data: dict[str, Any | None]
    files: dict[str, InputFile] | None = None


class Response(BaseModel, Generic[RubikaType]):
    status: str | None = None
    """Response status (e.g., 'OK' or 'INVALID_ACCESS')."""

    data: RubikaType | None = None
    """Main data payload from Rubika."""

    dev_message: str | None = None
    """Error description for developers."""

    @property
    def ok(self) -> bool:
        return self.status == "OK"

    @property
    def error_code(self) -> str | int | None:
        return None if self.ok else self.status

    @property
    def description(self) -> str | None:
        return self.dev_message

    @property
    def result(self) -> RubikaType | None:
        return self.data

    @classmethod
    def unwrap(cls, data: dict[str, Any], field: str) -> dict[str, Any]:
        if isinstance(data.get("data"), dict):
            data["data"] = data["data"].get(field, data["data"])
        return data


class RubikaMethod(BotContextController, BaseModel, Generic[RubikaType], ABC):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @model_validator(mode="before")
    @classmethod
    def remove_unset(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(values, dict):
            return values
        return {k: v for k, v in values.items() if not isinstance(v, UNSET_TYPE)}

    if TYPE_CHECKING:
        __returning__: ClassVar[Any]
        __api_method__: ClassVar[str]
        __returning_field__: ClassVar[str | None]
    else:
        @property
        @abstractmethod
        def __returning__(self) -> type:
            pass

        @property
        @abstractmethod
        def __api_method__(self) -> str:
            pass

        @property
        def __returning_field__(self) -> str | None:
            return None

    def build_request(self) -> Request:
        """
        Builds the request object by separating InputFiles from other data.
        """
        data = self.model_dump(exclude_none=True, by_alias=True)
        files: dict[str, InputFile] = {}

        for key, value in list(data.items()):
            if isinstance(value, InputFile):
                files[key] = data.pop(key)

        return Request(method=self.__api_method__, data=data, files=files or None)

    async def emit(self, bot: Bot) -> RubikaType:
        return await bot(self)

    def __await__(self) -> Generator[Any, None, RubikaType]:
        bot = self._bot
        if not bot:
            raise RuntimeError(
                "This method is not mounted to any bot instance. Please call it explicitly "
                "with bot instance `await bot(method)`\n"
                "or mount method to a bot instance `method.as_(bot)` "
                "and then call it `await method`"
            )
        return self.emit(bot).__await__()