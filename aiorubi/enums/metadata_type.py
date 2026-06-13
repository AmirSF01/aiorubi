from enum import Enum


class MetadataType(str, Enum):
    """
    This object represents a type of metadata.

    Source: https://rubika.ir/botapi/models#metadataTypeEnum
    """

    BOLD = "Bold"
    ITALIC = "Italic"
    MONO = "Mono"
    UNDERLINE = "Underline"
    STRIKE = "Strike"
    SPOILER = "Spoiler"
    LINK = "Link"
    MENTION_TEXT = "MentionText"
    PRE = "Pre"
    QUOTE = "Quote"