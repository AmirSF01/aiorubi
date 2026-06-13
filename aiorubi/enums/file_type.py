from enum import Enum


class FileType(str, Enum):
    """
    This object represents a type of file.

    Source: https://rubika.ir/botapi/models#enums
    """

    FILE = "File"
    IMAGE = "Image"
    VOICE = "Voice"
    VIDEO = "Video"
    MUSIC = "Music"
    GIF = "Gif"