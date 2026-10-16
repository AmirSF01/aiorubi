---
name: aiorubi
description: >-
  Working knowledge for building bots with aiorubi — an async Python framework
  for the Rubika Bot API v3 (rubika.ir), structurally ported from aiogram 3.x.
  Use this skill when writing, reviewing, or debugging code that imports aiorubi,
  or when porting aiogram bots to Rubika.
---

# aiorubi agent skill

aiorubi is a fully asynchronous Python framework for the **Rubika Bot API v3**
(rubika.ir), Python 3.10+, built on asyncio + aiohttp + Pydantic v2. It is a
deliberate **structural port of aiogram 3.x**: same module layout, class names,
and ergonomics, so aiogram knowledge transfers ~90% — but the API surface and
several behaviors differ (see the gotchas below; they are the other 10%).

## Mental model

```python
from aiorubi import Bot, Dispatcher, Router, BaseMiddleware, F, flags, enums, methods, types, session
```

That is the entire top-level export surface. Notable:
- `F` is a custom magic-filter (`F.text == "hi"`, `F.file`, `F.aux_data.button_id == "x"`).
- `html` and `md` text-decoration helpers are **commented out** — Rubika renders
  **plain text only**. Do not attempt to send HTML/Markdown.
- Everything below the top level is imported from submodules, e.g.
  `from aiorubi.filters.command import Command`.

## Quick start

```python
import asyncio
from aiorubi import Bot, Dispatcher
from aiorubi.filters.command import Command

dp = Dispatcher()

@dp.new_message(Command("start"))
async def cmd_start(message):
    await message.reply(f"Hello, {message.sender_id}!")

@dp.new_message()
async def echo(message):
    if message.text is not None:          # guard: media messages have text=None
        await message.answer(message.text)

async def main():
    bot = Bot(token="YOUR_TOKEN")
    await bot.me()                        # required before bot.id works
    await dp.start_polling(bot)

asyncio.run(main())
```

There is also a sync entry point: `dp.run_polling(bot)` (starts the loop itself,
uses uvloop when installed).

## Task → reference routing

Read only the reference you need — each is self-contained:

| Task                                          | Read                                            |
| --------------------------------------------- | ----------------------------------------------- |
| Send messages/media/files, download files     | [references/api.md](references/api.md)           |
| Handlers, filters, routers, middleware, flags | [references/dispatcher-and-filters.md](references/dispatcher-and-filters.md) |
| Multi-step dialogs (FSM or Scenes)            | [references/fsm-and-scenes.md](references/fsm-and-scenes.md) |
| Keyboards (keypads) and button clicks         | [references/keypads-and-inline.md](references/keypads-and-inline.md) |
| Error handling, webhook deployment            | [references/errors-and-webhook.md](references/errors-and-webhook.md) |

For long-form tutorials, the Sphinx docs live in `docs/guide/` and
`docs/tutorial/` (RST). When this skill and the RST docs disagree, **verify
against the source code under `aiorubi/`** — code wins.

## Critical gotchas — read before writing any handler

1. **All IDs are `str`.** `chat_id`, `message_id`, `sender_id`, `bot_id`,
   `file_id`, `reply_to_message_id` — never `int`. Compare/compare-and-cast
   accordingly.

2. **One unified `Message.file`.** Unlike aiogram there is no `.photo`, `.video`,
   `.voice` etc. Media arrives as `message.file` with `message.file.file_type`
   (a `FileType` enum: `IMAGE`, `VIDEO`, `VOICE`, `MUSIC`, `GIF`, `FILE`).
   Special content types are separate fields: `.sticker`, `.poll`,
   `.location`, `.contact_message` (not `.contact`).

3. **Guard `message.text is not None`.** Media-only updates carry `text=None`;
   unguarded `message.text.lower()` raises `AttributeError`.

4. **Event names differ from aiogram:**
   - `message` → `new_message`
   - `edited_message` → `updated_message`
   - `callback_query` → `inline_message`
   - member events → `started_bot` / `stopped_bot`
   - There is also a raw `dp.update` observer for whole `Update` objects.

5. **`ButtonId`, not `CallbackData`.** The callback-data factory class is
   `ButtonId` and it is **not exported from `aiorubi.filters`** — import it as
   `from aiorubi.filters.callback_data import ButtonId`. Buttons carry a packed
   string id (`"nav:next:2"`), and clicks arrive as `inline_message` updates.
   See [references/keypads-and-inline.md](references/keypads-and-inline.md).

6. **Handlers fire in registration order.** First matching handler wins —
   no filter-priority ranking. Register broad/escape-hatch handlers (e.g.
   `/cancel` while in an FSM state) **before** state-bound or catch-all handlers.

7. **`bot.id` needs `bot.me()` first.** `bot.id` raises `RuntimeError` until
   `await bot.me()` has cached the bot info.

8. **No HTML/Markdown.** `DefaultBotProperties.parse_mode` exists but Rubika
   v3 does not render formatted text; `metadata` carries entities like bold if
   needed. Keep message text plain.

9. **Webhook budget.** Rubika's webhook timeout is 60s; aiorubi answers at ~55s
   and moves slow handlers to background tasks. Design handlers to finish or
   ack quickly. See [references/errors-and-webhook.md](references/errors-and-webhook.md).

10. **File sending is two-step.** Uploading a new file = `request_send_file()`
    → upload to the returned URL → send by `file_id`. `bot.send_file()` and the
    `reply_image/answer_video/...` helpers do this automatically for
    `InputFile` objects; when `file` is a `str` it is treated as an existing
    `file_id`.

## When porting from aiogram

Beyond the renames above, expect these substitutions:

| aiogram 3.x                              | aiorubi                                    |
| ---------------------------------------- | ------------------------------------------ |
| `dp.message(...)`                        | `dp.new_message(...)`                       |
| `dp.edited_message`, `dp.callback_query` | `dp.updated_message(...)`, `dp.inline_message(...)` |
| `CallbackData`, `CallbackQuery`          | `ButtonId` + `inline_message` observer      |
| `message.photo` / `message.video`        | `message.file` + `FileType`                 |
| `F.data` (callback data string)          | `F.aux_data.button_id`                      |
| HTML/Markdown parse modes                | plain text only                             |
| `chat: int`                              | `chat_id: str`                              |
