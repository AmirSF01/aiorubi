from enum import Enum, auto


class FSMStrategy(Enum):
    """
    FSM strategy for storage key generation.
    """

    USER_IN_CHAT = auto()
    """State will be stored for each user in chat."""
    CHAT = auto()
    """State will be stored for each chat globally without separating by users."""
    GLOBAL_USER = auto()
    """State will be stored globally for each user globally."""


def apply_strategy(
    strategy: FSMStrategy,
    chat_id: str,
    user_id: str,
) -> tuple[str, str]:
    if strategy == FSMStrategy.CHAT:
        return chat_id, chat_id
    if strategy == FSMStrategy.GLOBAL_USER:
        return user_id, user_id

    return chat_id, user_id
