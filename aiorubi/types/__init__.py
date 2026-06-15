from typing import Literal, Optional, Union

from .base import RubikaObject
from .chat import Chat
from .file import File
from .location import Location
from .sticker import Sticker
from .contact_message import ContactMessage
from .poll_status import PollStatus
from .poll import Poll
from .forwarded_from import ForwardedFrom
from .bot_info import BotInfo
from .bot_command import BotCommand
from .aux_data import AuxData
from .button_selection_item import ButtonSelectionItem
from .button_selection import ButtonSelection
from .button_calendar import ButtonCalendar
from .button_number_picker import ButtonNumberPicker
from .button_string_picker import ButtonStringPicker
from .button_textbox import ButtonTextbox
from .button_location import ButtonLocation
from .button import Button
from .custom import DateTime
from .error_event import ErrorEvent
from .forwarded_no_link import ForwardedNoLink
from .download_url import DownloadUrl
from .upload_url import UploadUrl
from .get_updates_response import GetUpdatesResponse
from .keypad_row import KeypadRow
from .keypad import Keypad
from .message_keypad_update import MessageKeypadUpdate
from .message_text_update import MessageTextUpdate
from .message import Message
from .removed_message import RemovedMessage
from .metadata import MetaData, MetaDataPart
from .inline_message import InlineMessage
from .update import Update
from .response_parameters import ResponseParameters
from .input_file import InputFile
from .update_endpoint_status import UpdateEndpointsStatus

from .message_id import MessageID

__all__ = [
    "RubikaObject",
    "Chat",
    "File",
    "Location",
    "Sticker",
    "ContactMessage",
    "PollStatus",
    "Poll",
    "ForwardedFrom",
    "BotInfo",
    "BotCommand",
    "AuxData",
    "ButtonSelectionItem",
    "ButtonSelection",
    "ButtonCalendar",
    "ButtonNumberPicker",
    "ButtonStringPicker",
    "ButtonTextbox",
    "ButtonLocation",
    "Button",
    "ErrorEvent",
    "DateTime",
    "DownloadUrl",
    "UploadUrl",
    "ForwardedNoLink",
    "GetUpdatesResponse",
    "KeypadRow",
    "Keypad",
    "MessageKeypadUpdate",
    "MessageTextUpdate",
    "Message",
    "RemovedMessage",
    "MetaData",
    "MetaDataPart",
    "InlineMessage",
    "Update",
    "ResponseParameters",
    "InputFile",
    "MessageID",
    "UpdateEndpointsStatus"
]


from ..client.default import Default as _Default

# Load typing forward refs for every RubikaObject
for _entity_name in __all__:
    _entity = globals()[_entity_name]
    if not hasattr(_entity, "model_rebuild"):
        continue
    _entity.model_rebuild(
        _types_namespace={
            "List": list,
            "Optional": Optional,
            "Union": Union,
            "Literal": Literal,
            "Default": _Default,
            **{k: v for k, v in globals().items() if k in __all__},
        }
    )

del _entity
del _entity_name
