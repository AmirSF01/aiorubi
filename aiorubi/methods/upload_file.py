from __future__ import annotations

from ..types import File
from .base import RubikaMethod

class UploadFile(RubikaMethod[File]):
    """
    Fake method to reuse check_response() for upload endpoint.

    Upload responses have the same {status, data} format as Bot API methods.
    This class lets us validate upload responses using the existing logic
    without duplicating code.

    Not a real API method. Used internally only.
    """
    __returning__ = File
    __api_method__ = None

