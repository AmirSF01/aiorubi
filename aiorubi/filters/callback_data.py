from __future__ import annotations

import types
import typing
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import TYPE_CHECKING, Any, ClassVar, Literal, TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic_core import PydanticUndefined
from typing_extensions import Self

from aiorubi.filters.base import Filter
from aiorubi.types import InlineMessage

if TYPE_CHECKING:
    from magic_filter import MagicFilter
    from pydantic.fields import FieldInfo

T = TypeVar("T", bound="ButtonId")

MAX_CALLBACK_LENGTH: int = 64


_UNION_TYPES = {typing.Union, types.UnionType}


class ButtonIdException(Exception):
    pass


class ButtonId(BaseModel):
    """
    Base class for button id wrapper

    This class should be used as super-class of user-defined callbacks.

    The class-keyword :code:`prefix` is required to define prefix
    and also the argument :code:`sep` can be passed to define separator (default is :code:`:`).
    """

    if TYPE_CHECKING:
        __separator__: ClassVar[str]
        """Data separator (default is :code:`:`)"""
        __prefix__: ClassVar[str]
        """Callback prefix"""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        if "prefix" not in kwargs:
            msg = (
                f"prefix required, usage example: "
                f"`class {cls.__name__}(ButtonId, prefix='my_button'): ...`"
            )
            raise ValueError(msg)
        cls.__separator__ = kwargs.pop("sep", ":")
        cls.__prefix__ = kwargs.pop("prefix")
        if cls.__separator__ in cls.__prefix__:
            msg = (
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )
            raise ValueError(msg)
        super().__init_subclass__(**kwargs)

    def _encode_value(self, key: str, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, UUID):
            return value.hex
        if isinstance(value, bool):
            return str(int(value))
        if isinstance(value, (int, str, float, Decimal, Fraction)):
            return str(value)
        msg = (
            f"Attribute {key}={value!r} of type {type(value).__name__!r}"
            f" can not be packed to button id"
        )
        raise ValueError(msg)

    def pack(self) -> str:
        """
        Generate button id string

        :return: valid button id for Rubika Bot API
        """
        result = [self.__prefix__]
        for key, value in self.model_dump(mode="python").items():
            encoded = self._encode_value(key, value)
            if self.__separator__ in encoded:
                msg = (
                    f"Separator symbol {self.__separator__!r} can not be used "
                    f"in value {key}={encoded!r}"
                )
                raise ValueError(msg)
            result.append(encoded)
        button_id = self.__separator__.join(result)
        if len(button_id.encode()) > MAX_CALLBACK_LENGTH:
            msg = (
                f"Resulted button id is too long! "
                f"len({button_id!r}.encode()) > {MAX_CALLBACK_LENGTH}"
            )
            raise ValueError(msg)
        return button_id

    @classmethod
    def unpack(cls, value: str) -> Self:
        """
        Parse button id string

        :param value: value from Rubika
        :return: instance of ButtonId
        """
        prefix, *parts = value.split(cls.__separator__)
        names = cls.model_fields.keys()
        if len(parts) != len(names):
            msg = (
                f"Button id {cls.__name__!r} takes {len(names)} arguments "
                f"but {len(parts)} were given"
            )
            raise TypeError(msg)
        if prefix != cls.__prefix__:
            msg = f"Bad prefix ({prefix!r} != {cls.__prefix__!r})"
            raise ValueError(msg)
        payload = {}
        for k, v in zip(names, parts, strict=True):  # type: str, str
            if (
                (field := cls.model_fields.get(k))
                and v == ""
                and _check_field_is_nullable(field)
                and field.default != ""
            ):
                v = field.default if field.default is not PydanticUndefined else None
            payload[k] = v
        return cls(**payload)

    @classmethod
    def filter(cls, rule: MagicFilter | None = None) -> InlineMessageFilter:
        """
        Generates a filter for inline message with rule

        :param rule: magic rule
        :return: instance of filter
        """
        return InlineMessageFilter(button_id=cls, rule=rule)


class InlineMessageFilter(Filter):
    """
    This filter helps to handle inline message.

    Should not be used directly, you should create the instance of this filter
    via button id instance
    """

    __slots__ = (
        "button_id",
        "rule",
    )

    def __init__(
        self,
        *,
        button_id: type[ButtonId],
        rule: MagicFilter | None = None,
    ):
        """
        :param button_id: Expected type of button id
        :param rule: Magic rule
        """
        self.button_id = button_id
        self.rule = rule

    def __str__(self) -> str:
        return self._signature_to_string(
            button_id=self.button_id,
            rule=self.rule,
        )

    async def __call__(self, inline_message: InlineMessage) -> Literal[False] | dict[str, Any]:
        if not isinstance(inline_message, InlineMessage):
            return False
        button_id = inline_message.aux_data.button_id if inline_message.aux_data else None
        if not button_id:
            return False
        try:
            button_id = self.button_id.unpack(button_id)
        except (TypeError, ValueError):
            return False

        if self.rule is None or self.rule.resolve(button_id):
            return {"button_id": button_id}
        return False


def _check_field_is_nullable(field: FieldInfo) -> bool:
    """
    Check if the given field is nullable.

    :param field: The FieldInfo object representing the field to check.
    :return: True if the field is nullable, False otherwise.

    """
    if not field.is_required():
        return True

    return typing.get_origin(field.annotation) in _UNION_TYPES and type(None) in typing.get_args(
        field.annotation,
    )
