from __future__ import annotations

import html
import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, cast

from aiorubi.enums import MetadataType

if TYPE_CHECKING:
    from collections.abc import Generator
    from re import Pattern

    from aiorubi.types import MetaDataPart

__all__ = (
    "HtmlDecoration",
    "MarkdownDecoration",
    "TextDecoration",
    "add_surrogates",
    "html_decoration",
    "markdown_decoration",
    "remove_surrogates",
)


def add_surrogates(text: str) -> bytes:
    """Convert text to UTF-16 LE encoded bytes for proper offset calculation"""
    return text.encode("utf-16-le")


def remove_surrogates(text: bytes) -> str:
    """Convert UTF-16 LE encoded bytes back to string"""
    return text.decode("utf-16-le")


class TextDecoration(ABC):
    def apply_entity(self, entity: MetaDataPart, text: str) -> str:
        """
        Apply single entity to text

        :param entity: MetaDataPart object
        :param text: Text content to format
        :return: Formatted text
        """
        if entity.type == MetadataType.BOLD:
            return self.bold(value=text)
        if entity.type == MetadataType.ITALIC:
            return self.italic(value=text)
        if entity.type == MetadataType.MONO:
            return self.code(value=text)
        if entity.type == MetadataType.UNDERLINE:
            return self.underline(value=text)
        if entity.type == MetadataType.STRIKE:
            return self.strikethrough(value=text)
        if entity.type == MetadataType.SPOILER:
            return self.spoiler(value=text)
        if entity.type == MetadataType.LINK:
            return self.link(value=text, link=cast(str, entity.link_url))
        if entity.type == MetadataType.MENTION_TEXT:
            return self.mention(
                value=text,
                user_id=cast(str, entity.mention_text_user_id)
            )
        if entity.type == MetadataType.PRE:
            return self.pre(value=text)
        if entity.type == MetadataType.QUOTE:
            return self.blockquote(value=text)

        # Fallback: quote the text if entity type is unknown
        return self.quote(text)

    def unparse(self, text: str, metadata: list[MetaDataPart] | None = None) -> str:
        """
        Unparse message entities from Rubika metadata

        :param text: raw text
        :param metadata: List of MetaDataPart objects
        :return: Formatted text
        """
        return "".join(
            self._unparse_entities(
                add_surrogates(text),
                sorted(metadata, key=lambda item: item.from_index) if metadata else [],
            ),
        )

    def _unparse_entities(
        self,
        text: bytes,
        entities: list[MetaDataPart],
        offset: int | None = None,
        length: int | None = None,
    ) -> Generator[str, None, None]:
        if offset is None:
            offset = 0
        length = length or len(text)

        for index, entity in enumerate(entities):
            if entity.from_index * 2 < offset:
                continue
            if entity.from_index * 2 > offset:
                yield self.quote(remove_surrogates(text[offset: entity.from_index * 2]))

            start = entity.from_index * 2
            offset = entity.from_index * 2 + entity.length * 2

            # Find nested entities
            sub_entities = list(
                filter(
                    lambda e: e.from_index * 2 < (offset or 0),
                    entities[index + 1:]
                ),
            )

            yield self.apply_entity(
                entity,
                "".join(
                    self._unparse_entities(
                        text,
                        sub_entities,
                        offset=start,
                        length=offset
                    )
                ),
            )

        if offset < length:
            yield self.quote(remove_surrogates(text[offset:length]))

    @abstractmethod
    def link(self, value: str, link: str) -> str:
        pass

    @abstractmethod
    def mention(self, value: str, user_id: str) -> str:
        pass

    @abstractmethod
    def bold(self, value: str) -> str:
        pass

    @abstractmethod
    def italic(self, value: str) -> str:
        pass

    @abstractmethod
    def code(self, value: str) -> str:
        pass

    @abstractmethod
    def pre(self, value: str) -> str:
        pass

    @abstractmethod
    def underline(self, value: str) -> str:
        pass

    @abstractmethod
    def strikethrough(self, value: str) -> str:
        pass

    @abstractmethod
    def spoiler(self, value: str) -> str:
        pass

    @abstractmethod
    def quote(self, value: str) -> str:
        pass

    @abstractmethod
    def blockquote(self, value: str) -> str:
        pass


class HtmlDecoration(TextDecoration):
    BOLD_TAG = "b"
    ITALIC_TAG = "i"
    UNDERLINE_TAG = "u"
    STRIKETHROUGH_TAG = "s"
    CODE_TAG = "code"
    PRE_TAG = "pre"
    LINK_TAG = "a"
    SPOILER_TAG = "span"
    SPOILER_CLASS = "spoiler"
    BLOCKQUOTE_TAG = "blockquote"

    def _tag(
        self,
        tag: str,
        content: str,
        *,
        attrs: dict[str, str] | None = None,
    ) -> str:
        attrs_str = ""
        if attrs:
            attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs.items())

        return f"<{tag}{attrs_str}>{content}</{tag}>"

    def link(self, value: str, link: str) -> str:
        return self._tag(self.LINK_TAG, value, attrs={"href": link})

    def mention(self, value: str, user_id: str) -> str:
        # Rubika mention format - adjust if needed
        return self._tag(self.LINK_TAG, value, attrs={"href": f"rubika://user/{user_id}"})

    def bold(self, value: str) -> str:
        return self._tag(self.BOLD_TAG, value)

    def italic(self, value: str) -> str:
        return self._tag(self.ITALIC_TAG, value)

    def code(self, value: str) -> str:
        return self._tag(self.CODE_TAG, value)

    def pre(self, value: str) -> str:
        return self._tag(self.PRE_TAG, value)

    def underline(self, value: str) -> str:
        return self._tag(self.UNDERLINE_TAG, value)

    def strikethrough(self, value: str) -> str:
        return self._tag(self.STRIKETHROUGH_TAG, value)

    def spoiler(self, value: str) -> str:
        return self._tag(self.SPOILER_TAG, value, attrs={"class": self.SPOILER_CLASS})

    def quote(self, value: str) -> str:
        return html.escape(value, quote=False)

    def blockquote(self, value: str) -> str:
        return self._tag(self.BLOCKQUOTE_TAG, value)


class MarkdownDecoration(TextDecoration):
    MARKDOWN_QUOTE_PATTERN: Pattern[str] = re.compile(r"([_*\[\]()~`>#+\-=|{}.!\\])")

    def link(self, value: str, link: str) -> str:
        return f"[{value}]({link})"

    def mention(self, value: str, user_id: str) -> str:
        return f"[{value}](rubika://user/{user_id})"

    def bold(self, value: str) -> str:
        return f"**{value}**"

    def italic(self, value: str) -> str:
        return f"_{value}_"

    def code(self, value: str) -> str:
        return f"`{value}`"

    def pre(self, value: str) -> str:
        return f"```\n{value}\n```"

    def underline(self, value: str) -> str:
        return f"__{value}__"

    def strikethrough(self, value: str) -> str:
        return f"~~{value}~~"

    def spoiler(self, value: str) -> str:
        return f"||{value}||"

    def quote(self, value: str) -> str:
        return re.sub(pattern=self.MARKDOWN_QUOTE_PATTERN, repl=r"\\\1", string=value)

    def blockquote(self, value: str) -> str:
        return "\n".join(f"> {line}" for line in value.splitlines())


html_decoration = HtmlDecoration()
markdown_decoration = MarkdownDecoration()