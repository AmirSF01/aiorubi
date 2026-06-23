from collections.abc import Sequence
from inspect import isclass
from typing import Any, cast

from aiorubi.filters.base import Filter
from aiorubi.fsm.state import State, StatesGroup
from aiorubi.types import RubikaObject

StateType = str | State | StatesGroup | type[StatesGroup] | None


class StateFilter(Filter):
    """
    State filter
    """

    __slots__ = ("states",)

    def __init__(self, *states: StateType) -> None:
        if not states:
            msg = "At least one state is required"
            raise ValueError(msg)

        self.states = states

    def __str__(self) -> str:
        return self._signature_to_string(
            *self.states,
        )

    async def __call__(
        self,
        obj: RubikaObject,
        raw_state: str | None = None,
    ) -> bool | dict[str, Any]:
        allowed_states = cast(Sequence[StateType], self.states)
        for allowed_state in allowed_states:
            if isinstance(allowed_state, str) or allowed_state is None:
                if allowed_state in {"*", raw_state}:
                    return True
            elif isinstance(allowed_state, (State, StatesGroup)):
                if allowed_state(event=obj, raw_state=raw_state):
                    return True
            elif (
                isclass(allowed_state)
                and issubclass(allowed_state, StatesGroup)
                and allowed_state()(event=obj, raw_state=raw_state)
            ):
                return True
        return False
