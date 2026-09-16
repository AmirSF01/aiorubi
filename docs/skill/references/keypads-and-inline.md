# aiorubi reference: Keypads, buttons, and inline messages

Verified against `aiorubi/types/keypad*.py`, `aiorubi/filters/callback_data.py`
(v1.2.x). Rubika has no inline mode — its two "keyboard" mechanisms both use the
`Keypad` model.

## Building a keypad

```python
from aiorubi.types import Keypad, KeypadRow, Button

keypad = Keypad(
    rows=[
        KeypadRow(buttons=[
            Button(id="btn_list", type="Simple", button_text="List items"),
            Button(id="btn_help", type="Simple", button_text="Help"),
        ]),
        KeypadRow(buttons=[
            Button(id="btn_del", type="Simple", button_text="Remove keypad"),
        ]),
    ],
    resize_keyboard=True,        # optional
    one_time_keyboard=True,      # optional
)
```

- `Button(id: str, type: str, button_text: str, ...)` — `type` is the
  `ButtonType` enum *value* (`"Simple"`, `"Selection"`, `"Calendar"`,
  `"NumberPicker"`, `"StringPicker"`, `"Location"`, `"Textbox"`, `"Link"`,
  `"AskMyPhoneNumber"`, ...). Pass `type=ButtonType.SIMPLE.value` (it's a
  `str`-Enum) or the plain string.
- Special button types take an extra payload field: `button_selection`,
  `button_calendar`, `button_number_picker`, `button_string_picker`,
  `button_location`, `button_textbox` (models in `aiorubi.types`).

## Attaching a keypad

Two kwargs on every send method (and `reply_*`/`answer_*` helpers):

- **`inline_keypad=`** — buttons attached under the message itself.
- **`chat_keypad=`** (+ `chat_keypad_type=ChatKeypadType.NEW`) — replaces the
  chat's persistent reply keyboard. Remove later with
  `bot.remove_chat_keypad(chat_id)` (the dedicated method), or by sending
  another message with `chat_keypad_type=ChatKeypadType.REMOVE`.

```python
from aiorubi.enums import ChatKeypadType

@dp.new_message(Command("menu"))
async def menu(message):
    await message.reply(
        "Choose:",
        inline_keypad=keypad,                      # inline
    )
    # or chat keypad:
    # await message.answer(text="...", chat_keypad=keypad, chat_keypad_type=ChatKeypadType.NEW)
```

## Handling clicks

### Inline keypad → `inline_message` updates

A click on an inline button arrives as an **`inline_message`** update
(`InlineMessage`: `sender_id`, `message_id`, `chat_id`, `text`, `file`,
`location`, `aux_data.button_id`).

### Chat keypad → `new_message` with `aux_data.button_id`

Clicking a chat-keypad button sends a normal message whose `aux_data.button_id`
holds the button id (no text). Filter with `F.aux_data.button_id == "..."`.

### `ButtonId` — the typed callback-data factory

Like aiogram's `CallbackData`, but named `ButtonId` and **not exported from
`aiorubi.filters`**:

```python
from aiorubi import F
from aiorubi.filters.callback_data import ButtonId    # <- real import path

class Nav(ButtonId, prefix="nav"):                    # prefix REQUIRED
    action: str
    page: int = 0

# pack: values joined by ":" after the prefix
Nav(action="next", page=2).pack()                     # -> "nav:next:2"

# send button carrying the packed id
Button(id=Nav(action="next", page=0).pack(), type="Simple", button_text="Next")

# filter: unpacks and injects `button_id: Nav`; use module-level F (the class
# attributes are pydantic fields, not descriptors on the class itself)
@dp.inline_message(Nav.filter(F.action == "next"))
async def next_page(inline_message, button_id: Nav):
    await inline_message.answer(f"page {button_id.page}")
```

Rules: `prefix` is required (`class Nav(ButtonId, prefix="nav")`), separator
defaults to `":"` (`sep=` to change; must not appear in prefix or any value),
fields must be `int | str | float | bool | Decimal | Fraction | UUID | Enum | None`,
and the packed string must be ≤ 64 bytes (`MAX_CALLBACK_LENGTH`), else
`ValueError` at pack time. `.filter(rule)` returns an `InlineMessageFilter`
that works on `inline_message` updates and injects `button_id`.
`MyId.unpack("nav:next:2")` parses manually.

### Editing keypads after send

- `bot.edit_message_keypad(chat_id, message_id, inline_keypad)` — swap an
  inline keypad (returns `bool`).
- `bot.edit_chat_keypad(chat_id, chat_keypad)` — replace the chat keypad; the
  method sets `ChatKeypadType.NEW` internally (no `chat_keypad_type` param).
- `bot.remove_chat_keypad(chat_id)` — remove the chat keypad.

## Deep dive

`docs/guide/filter.rst` (ButtonId section), `docs/tutorial/04_keypads.rst`.
