from enum import Enum


class UpdateEndpointType(str, Enum):
    """
    This object represents a type of update endpoint.

    Source: https://rubika.ir/botapi/models#enums
    """

    RECEIVE_UPDATE = "ReceiveUpdate"
    RECEIVE_INLINE_MESSAGE = "ReceiveInlineMessage"
    RECEIVE_QUERY = "ReceiveQuery"
    GET_SELECTION_ITEM = "GetSelectionItem"
    SEARCH_SELECTION_ITEMS = "SearchSelectionItems"