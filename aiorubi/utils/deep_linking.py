from __future__ import annotations

__all__ = [
    "create_deep_link",
    "create_start_link",
    "create_rubika_link",
    "decode_payload",
    "encode_payload",
]

import re
from typing import TYPE_CHECKING

from aiorubi.utils.link import create_rubika_link
from aiorubi.utils.payload import decode_payload, encode_payload

if TYPE_CHECKING:
    from collections.abc import Callable

    from aiorubi import Bot

BAD_PATTERN = re.compile(r"[^a-zA-Z0-9-_]")
DEEPLINK_PAYLOAD_LENGTH = 64


async def create_start_link(
    bot: Bot,
    payload: str,
    encode: bool = False,
    encoder: Callable[[bytes], bytes] | None = None,
) -> str:
    """
    Create 'st' deep link with your payload.

    If you need to encode payload or pass special characters - set encode as True

    :param bot: bot instance
    :param payload: args passed with /start
    :param encode: encode payload with base64url or custom encoder
    :param encoder: custom encoder callable
    :return: link
    """
    username = (await bot.me()).username
    return create_deep_link(
        username=username,
        payload=payload,
        encode=encode,
        encoder=encoder,
    )

def create_deep_link(
    username: str,
    payload: str,
    encode: bool = False,
    encoder: Callable[[bytes], bytes] | None = None,
) -> str:
    """
    Create deep link.

    :param username:
    :param payload: any string-convertible data
    :param encode: encode payload with base64url or custom encoder
    :param encoder: custom encoder callable
    :return: deeplink
    """
    if not isinstance(payload, str):
        payload = str(payload)

    if encode or encoder:
        payload = encode_payload(payload, encoder=encoder)

    if re.search(BAD_PATTERN, payload):
        msg = (
            "Wrong payload! Only A-Z, a-z, 0-9, _ and - are allowed. "
            "Pass `encode=True` or encode payload manually."
        )
        raise ValueError(msg)

    if len(payload) > DEEPLINK_PAYLOAD_LENGTH:
        msg = f"Payload must be up to {DEEPLINK_PAYLOAD_LENGTH} characters long."
        raise ValueError(msg)

    deep_link = create_rubika_link(username, st=payload)

    return deep_link