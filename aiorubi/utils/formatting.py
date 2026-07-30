from __future__ import annotations

import textwrap
from collections.abc import Generator, Iterable, Iterator
from typing import Any, ClassVar

from typing_extensions import Self

from aiorubi.enums import MetadataType
from aiorubi.types import MetaDataPart
from aiorubi.utils.text_decorations import (
    add_surrogates,
    html_decoration,
    markdown_decoration,
    remove_surrogates,
)

NodeType = Any


def sizeof(value: str) -> int:
    return len(value.encode("utf-16-le")) // 2


class Text(Iterable[NodeType]):
    """
    Simple text element
    """

    type: ClassVar[str | None] = None

    __slots__ = ("_body", "_params")

    def __init__(
        self,
        *body: NodeType,
        **params: Any,
    ) -> None:
        self._body: tuple[NodeType, ...] = body
        self._params: dict[str, Any] = params

    @classmethod
    def from_metadata(cls, text: str, metadata: list[MetaDataPart]) -> Text:
        """
        Create Text instance from text and metadata list

        :param text: raw text
        :param metadata: List of MetaDataPart objects
        :return: Text instance
        """
        return cls(
            *_unparse_metadata(
                text=add_surrogates(text),
                metadata=sorted(metadata, key=lambda item: item.from_index) if metadata else [],
            ),
        )

    def render(
        self,
        *,
        _offset: int = 0,
        _sort: bool = True,
        _collect_metadata: bool = True,
    ) -> tuple[str, list[MetaDataPart]]:
        """
        Render elements tree as text with metadata list

        :return: tuple of text and metadata parts
        """

        text = ""
        metadata = []
        offset = _offset

        for node in self._body:
            if not isinstance(node, Text):
                node = str(node)
                text += node
                offset += sizeof(node)
            else:
                node_text, node_metadata = node.render(
                    _offset=offset,
                    _sort=False,
                    _collect_metadata=_collect_metadata,
                )
                text += node_text
                offset += sizeof(node_text)
                if _collect_metadata:
                    metadata.extend(node_metadata)

        if _collect_metadata and self.type:
            metadata.append(self._render_metadata_part(offset=_offset, length=offset - _offset))

        if _collect_metadata and _sort:
            metadata.sort(key=lambda part: part.from_index)

        return text, metadata

    def _render_metadata_part(self, *, offset: int, length: int) -> MetaDataPart:
        """
        Render current node as MetaDataPart

        :param offset: start position
        :param length: length of text
        :return: MetaDataPart instance
        """
        assert self.type is not None, "Node without type can't be rendered as metadata part"
        return MetaDataPart(
            type=self.type,
            from_index=offset,
            length=length,
            **self._params
        )

    def as_kwargs(
        self,
        *,
        text_key: str = "text",
        metadata_key: str = "metadata",
    ) -> dict[str, Any]:
        """
        Render element tree as keyword arguments for usage in an API call, for example:

        .. code-block:: python

            text_content = Text(...)
            await message.answer(**text_content.as_kwargs())

        :param text_key: key name for text
        :param metadata_key: key name for metadata
        :return: dict with text and metadata
        """
        text_value, metadata_value = self.render()
        result: dict[str, Any] = {
            text_key: text_value,
            metadata_key: metadata_value,
        }
        return result

    def as_html(self) -> str:
        """
        Render elements tree as HTML markup
        """
        text, metadata = self.render()
        return html_decoration.unparse(text, metadata)

    def as_markdown(self) -> str:
        """
        Render elements tree as MarkdownV2 markup
        """
        text, metadata = self.render()
        return markdown_decoration.unparse(text, metadata)

    def replace(self: Self, *args: Any, **kwargs: Any) -> Self:
        return type(self)(*args, **{**self._params, **kwargs})

    def as_pretty_string(self, indent: bool = False) -> str:
        sep = ",\n" if indent else ", "
        body = sep.join(
            item.as_pretty_string(indent=indent) if isinstance(item, Text) else repr(item)
            for item in self._body
        )
        params = sep.join(f"{k}={v!r}" for k, v in self._params.items() if v is not None)

        args = []
        if body:
            args.append(body)
        if params:
            args.append(params)

        args_str = sep.join(args)
        if indent:
            args_str = textwrap.indent("\n" + args_str + "\n", "    ")
        return f"{type(self).__name__}({args_str})"

    def __add__(self, other: NodeType) -> Text:
        if isinstance(other, Text) and other.type == self.type and self._params == other._params:
            return type(self)(*self, *other, **self._params)
        if type(self) is Text and isinstance(other, str):
            return type(self)(*self, other, **self._params)
        return Text(self, other)

    def __iter__(self) -> Iterator[NodeType]:
        yield from self._body

    def __len__(self) -> int:
        text, _ = self.render(_collect_metadata=False)
        return sizeof(text)

    def __getitem__(self, item: slice) -> Text:
        if not isinstance(item, slice):
            msg = "Can only be sliced"
            raise TypeError(msg)
        if (item.start is None or item.start == 0) and item.stop is None:
            return self.replace(*self._body)
        start = 0 if item.start is None else item.start
        stop = len(self) if item.stop is None else item.stop
        if start == stop:
            return self.replace()

        nodes = []
        position = 0

        for node in self._body:
            node_size = len(node)
            current_position = position
            position += node_size
            if position < start:
                continue
            if current_position > stop:
                break
            a = max((0, start - current_position))
            b = min((node_size, stop - current_position))
            new_node = node[a:b]
            if not new_node:
                continue
            nodes.append(new_node)

        return self.replace(*nodes)


class Bold(Text):
    """
    Bold element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.BOLD`
    """

    type = MetadataType.BOLD


class Italic(Text):
    """
    Italic element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.ITALIC`
    """

    type = MetadataType.ITALIC


class Mono(Text):
    """
    Monospace (Code) element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.MONO`
    """

    type = MetadataType.MONO


class Underline(Text):
    """
    Underline element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.UNDERLINE`
    """

    type = MetadataType.UNDERLINE


class Strike(Text):
    """
    Strikethrough element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.STRIKE`
    """

    type = MetadataType.STRIKE


class Spoiler(Text):
    """
    Spoiler element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.SPOILER`
    """

    type = MetadataType.SPOILER


class Link(Text):
    """
    Link element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.LINK`
    """

    type = MetadataType.LINK

    def __init__(self, *body: NodeType, url: str, **params: Any) -> None:
        super().__init__(*body, link_url=url, **params)


class MentionText(Text):
    """
    Mention text element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.MENTION_TEXT`
    """

    type = MetadataType.MENTION_TEXT

    def __init__(self, *body: NodeType, user_id: str, **params: Any) -> None:
        super().__init__(*body, mention_text_user_id=user_id, **params)


class Pre(Text):
    """
    Pre (code block) element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.PRE`
    """

    type = MetadataType.PRE


class Quote(Text):
    """
    Quote element.

    Will be wrapped into :obj:`aiorubi.types.MetaDataPart`
    with type :obj:`aiorubi.enums.MetadataType.QUOTE`
    """

    type = MetadataType.QUOTE


NODE_TYPES: dict[str | None, type[Text]] = {
    Text.type: Text,
    Bold.type: Bold,
    Italic.type: Italic,
    Mono.type: Mono,
    Underline.type: Underline,
    Strike.type: Strike,
    Spoiler.type: Spoiler,
    Link.type: Link,
    MentionText.type: MentionText,
    Pre.type: Pre,
    Quote.type: Quote,
}


def _apply_metadata_part(metadata_part: MetaDataPart, *nodes: NodeType) -> NodeType:
    """
    Apply single metadata part to text nodes

    :param metadata_part: MetaDataPart to apply
    :param nodes: text nodes
    :return: formatted node
    """
    node_type = NODE_TYPES.get(metadata_part.type, Text)
    return node_type(
        *nodes,
        **metadata_part.model_dump(
            exclude={"type", "from_index", "length"},
            exclude_none=True,
        ),
    )


def _unparse_metadata(
    text: bytes,
    metadata: list[MetaDataPart],
    offset: int | None = None,
    length: int | None = None,
) -> Generator[NodeType, None, None]:
    """
    Unparse metadata parts from text

    :param text: encoded text in UTF-16 LE
    :param metadata: list of MetaDataPart
    :param offset: starting offset
    :param length: length to process
    :return: generator of nodes
    """
    if offset is None:
        offset = 0
    length = length or len(text)

    for index, part in enumerate(metadata):
        if part.from_index * 2 < offset:
            continue
        if part.from_index * 2 > offset:
            yield remove_surrogates(text[offset : part.from_index * 2])
        start = part.from_index * 2
        offset = part.from_index * 2 + part.length * 2

        sub_metadata = list(
            filter(lambda p: p.from_index * 2 < (offset or 0), metadata[index + 1 :])
        )
        yield _apply_metadata_part(
            part,
            *_unparse_metadata(text, sub_metadata, offset=start, length=offset),
        )

    if offset < length:
        yield remove_surrogates(text[offset:length])


def as_line(*items: NodeType, end: str = "\n", sep: str = "") -> Text:
    """
    Wrap multiple nodes into line with :code:`\\\\n` at the end of line.

    :param items: Text or Any
    :param end: ending of the line, by default is :code:`\\\\n`
    :param sep: separator between items, by default is empty string
    :return: Text
    """
    if sep:
        nodes = []
        for item in items[:-1]:
            nodes.extend([item, sep])
        nodes.extend([items[-1], end])
    else:
        nodes = [*items, end]
    return Text(*nodes)


def as_list(*items: NodeType, sep: str = "\n") -> Text:
    """
    Wrap each element to separated lines

    :param items:
    :param sep:
    :return:
    """
    nodes = []
    for item in items[:-1]:
        nodes.extend([item, sep])
    nodes.append(items[-1])
    return Text(*nodes)


def as_marked_list(*items: NodeType, marker: str = "- ") -> Text:
    """
    Wrap elements as marked list

    :param items:
    :param marker: line marker, by default is '- '
    :return: Text
    """
    return as_list(*(Text(marker, item) for item in items))


def as_numbered_list(*items: NodeType, start: int = 1, fmt: str = "{}. ") -> Text:
    """
    Wrap elements as numbered list

    :param items:
    :param start: initial number, by default 1
    :param fmt: number format, by default '{}. '
    :return: Text
    """
    return as_list(*(Text(fmt.format(index), item) for index, item in enumerate(items, start)))


def as_section(title: NodeType, *body: NodeType) -> Text:
    """
    Wrap elements as simple section, section has title and body

    :param title:
    :param body:
    :return: Text
    """
    return Text(title, "\n", *body)


def as_marked_section(
    title: NodeType,
    *body: NodeType,
    marker: str = "- ",
) -> Text:
    """
    Wrap elements as section with marked list

    :param title:
    :param body:
    :param marker:
    :return:
    """
    return as_section(title, as_marked_list(*body, marker=marker))


def as_numbered_section(
    title: NodeType,
    *body: NodeType,
    start: int = 1,
    fmt: str = "{}. ",
) -> Text:
    """
    Wrap elements as section with numbered list

    :param title:
    :param body:
    :param start:
    :param fmt:
    :return:
    """
    return as_section(title, as_numbered_list(*body, start=start, fmt=fmt))


def as_key_value(key: NodeType, value: NodeType) -> Text:
    """
    Wrap elements pair as key-value line. (:code:`<b>{key}:</b> {value}`)

    :param key:
    :param value:
    :return: Text
    """
    return Text(Bold(key, ":"), " ", value)