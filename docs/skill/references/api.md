# aiorubi API reference: Bot, messages, and files

All signatures verified against `aiorubi/client/bot.py` (v1.2.x) and `aiorubi/types/`.

## Bot

```python
from aiorubi import Bot

bot = Bot(token)                    # token from Rubika @BotFather; raises TokenValidationError on bad format
bot = Bot(token, session=None, default=DefaultBotProperties())
```

- Context manager: `async with bot:` closes the aiohttp session on exit.
- `await bot.me()` → `BotInfo`, cached. **Required before `bot.id`** (otherwise `RuntimeError`).
- `await bot(method_object)` — low-level call: any object from `aiorubi.methods`.
- `DefaultBotProperties(parse_mode=None, disable_notification=None, allow_sending_without_reply=None)`
  is passed as `default=`, but note Rubika v3 renders plain text only.

Full endpoint method list (each is `async` on `Bot`):

| Method | Returns | Notes |
| --- | --- | --- |
| `get_me()` | `BotInfo` | not cached; `me()` is the cached wrapper |
| `get_chat(chat_id)` | `Chat` | |
| `get_file(file_id)` | `DownloadUrl` | contains `.download_url` |
| `get_updates(...)` | raw updates | used internally by polling |
| `set_commands(bot_commands)` | `bool` | `bot_commands=[BotCommand(command="start", description="...")]` |
| `update_bot_endpoints(url, type=UpdateEndpointType.RECEIVE_UPDATE)` | `UpdateEndpointsStatus` | webhook registration |
| `send_message(chat_id, text, reply_to_message_id=None, metadata=None, inline_keypad=None, chat_keypad=None, chat_keypad_type=None)` | `MessageID` | |
| `send_file(chat_id, file, file_type=FileType.FILE, text=None, ...)` | `MessageID` | `file` = `file_id` str or `InputFile` |
| `send_image / send_gif / send_music / send_video / send_voice(chat_id, <media>, text=None, ...)` | `MessageID` | typed wrappers over `send_file` |
| `send_contact(chat_id, first_name, phone_number, last_name=None, ...)` | `MessageID` | |
| `send_poll(chat_id, question, options, type=None, ...)` | `MessageID` | |
| `send_location(chat_id, latitude, longitude, ...)` | `MessageID` | |
| `forward_message(from_chat_id, to_chat_id, message_id, disable_notification=False)` | `MessageID` | |
| `edit_message_text(chat_id, message_id, text, ...)` | `bool` | |
| `edit_message_keypad(chat_id, message_id, inline_keypad)` | `bool` | inline keypad edit |
| `edit_chat_keypad(chat_id, chat_keypad)` | `bool` | chat keypad replace; sets `ChatKeypadType.NEW` internally |
| `remove_chat_keypad(chat_id)` | `bool` | removes chat keypad (`ChatKeypadType.REMOVE`) |
| `delete_message(chat_id, message_id)` | `bool` | |
| `ban_chat_member(chat_id, user_id)` / `unban_chat_member(...)` | `bool` | |
| `request_send_file(file_type)` | `UploadUrl` | step 1 of manual upload |
| `upload_file(url, file)` | `File` | step 2; gives `file_id` |
| `download(file_or_file_id, destination=None)` | `BinaryIO \| None` | auto-creates `BytesIO` if destination is None |
| `download_file(url, destination=None)` | `BinaryIO \| None` | direct URL download |

All `chat_id` / `message_id` parameters are **`str`**.

## Message shortcuts

`aiorubi.types.Message` (received in `new_message` / `updated_message` handlers)
has 20 awaitable helpers — for each content kind there is a `reply_*` (sets
`reply_to_message_id` to the incoming message) and an `answer_*` variant
(no reply unless you pass `reply_to_message_id=`):

```
reply / answer                        # text
reply_file / answer_file              # file + file_type kwarg
reply_image / answer_image            # image
reply_gif / answer_gif
reply_music / answer_music
reply_video / answer_video
reply_voice / answer_voice
reply_contact / answer_contact
reply_poll / answer_poll
reply_location / answer_location
```

All accept the common kwargs `text` (for media), `metadata`,
`disable_notification`, `inline_keypad`, `chat_keypad`, `chat_keypad_type`.
They return bound method/coroutine objects — just `await` them.

```python
@dp.new_message(F.file.file_type == FileType.IMAGE)
async def echo_image(message):
    await message.reply_image(image=FSInputFile("cat.jpg"), text="Nice photo!")
    await message.answer("Got your image")
```

`InlineMessage` (button clicks) has **only** `.answer(text, **kwargs)` — no
`reply`, no media helpers. It also carries `sender_id`, `message_id`, `chat_id`,
`text`, `file`, `location`, `aux_data` (with `button_id`).

## Files

### Uploading (sending)

Two ways to pass `file`/`image`/`video`/... arguments:

- **`str`** — an existing Rubika `file_id` (fastest; the API re-sends it).
- **`InputFile`** — new upload; the bot does request-URL → upload → send
  automatically. Concrete classes in `aiorubi.types.input_file` (**import from
  the submodule — only the `InputFile` base is exported from `aiorubi.types`**):
  - `FSInputFile(path, filename=None)` — from disk
  - `BufferedInputFile(data: bytes, filename)` or `BufferedInputFile.from_file(path)`
  - `URLInputFile(url, ...)` — stream from the internet

```python
from aiorubi.types.input_file import FSInputFile, BufferedInputFile

await message.reply_image(FSInputFile("cat.png"), text="caption")     # upload
await message.answer_image("ABCD1234fileid")                           # re-send by file_id
await bot.send_file(chat_id, BufferedInputFile(b"...", "report.pdf"))
```

### Downloading

```python
# from a received message with media
stream_or_none = await bot.download(message.file)            # -> io.BytesIO
await bot.download(message.file, destination="out.jpg")      # -> saved to disk

# or manually
url = (await bot.get_file(message.file.file_id)).download_url
await bot.download_file(url, destination="out.jpg")
```

## Types cheat-sheet

`from aiorubi.types import ...` — key models (Pydantic v2, subclass `RubikaObject`):

- `Update`, `Message`, `InlineMessage`, `RemovedMessage`, `StartedBot`, `StoppedBot`
- `File` (`file_id: str`, `file_name`, `size`), `InputFile` family above
- `Keypad`, `KeypadRow`, `Button` (+ special button payload models)
- `AuxData` (`button_id`, `start_id` — `start_id` holds deep-link `st=` payload)
- `BotInfo`, `BotCommand`, `Chat`, `ErrorEvent`, `MessageID`, `MetaData`

Enums in `aiorubi.enums`: `FileType`, `ChatType`, `ChatKeypadType`,
`ButtonType`, `PollType`, `UpdateType`, `UpdateEndpointType`.

## Deep dive

Sphinx guides: `docs/guide/handlers.rst`, `docs/tutorial/05_files.rst`.
