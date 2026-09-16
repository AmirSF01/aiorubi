# aiorubi — بستهٔ مرجع داخلی برای نوشتن مستندات

> **هدف:** این فایل یک reference داخلی برای نویسندگان و reviewerهای مستندات aiorubi است. هر چیزی که در مستندات رسمی گفته می‌شود باید با این فایل cross-check شود. هر جایی که بین این فایل و کد واقعی پکیج اختلاف وجود داشت، **کد ارجح است**.

**منبع:** کلون رسمی از <https://github.com/AmirSF01/aiorubi> (commit `cd822a7`، نسخه 1.2.1، Aug 11 2026).
**PyPI:** <https://pypi.org/project/aiorubi/>
**مستندات رسمی (فعلی، ناقص):** <https://aiorubi.readthedocs.io>
**چنل روبیکا:** <https://rubika.ir/aiorubi>

---

## 1. هویت پکیج

| ویژگی | مقدار |
|---|---|
| نام | `aiorubi` |
| شعار رسمی | *aiorubi is a modern and fully asynchronous library for the Rubika Bot API.* |
| نویسنده | Amir S. Farahani |
| مجوز | MIT |
| Python | 3.10 تا <3.15 |
| نسخه | 1.2.1 |
| API روبیکا | v3 (`__api_version__ = "3"`) |
| اکستراها | `docs`, `fast` (uvloop + aiodns), `i18n` (Babel), `mongo` (motor + pymongo), `proxy` (aiohttp-socks), `redis` (redis[hiredis]) |
| Runtime deps | aiohttp, aiofiles, pydantic≥2.4,<2.14, magic-filter, certifi, typing-extensions |

### Public API (از `aiorubi/__init__.py`)

```python
from aiorubi import (
    Bot,
    Dispatcher,
    Router,
    BaseMiddleware,
    F,            # MagicFilter instance
    flags,        # FlagGenerator instance
    enums,
    methods,
    types,
    session,
)
from aiorubi.__meta__ import __version__, __api_version__
```

**نکتهٔ مهم برای مستندات:** `html` و `md` text decoration در `__init__.py` کامنت شده‌اند (در حال حاضر غیرفعالند). این را باید ذکر کرد چون ممکن است کاربر فکر کند پشتیبانی می‌شود.

---

## 2. معماری کلی (نسبت به aiogram)

`aiorubi` یک پورت ساختاری از **aiogram 3.x** به **Rubika Bot API v3** است. نگاشت تقریبی:

```
aiogram/aiogram/   ←→   aiorubi/aiorubi/
├── client/         ←→   client/
│   ├── bot.py      ←→   bot.py
│   └── session/    ←→   session/
├── dispatcher/     ←→   dispatcher/
│   ├── dispatcher.py
│   ├── router.py
│   ├── event/
│   ├── middlewares/
│   └── flags.py
├── fsm/            ←→   fsm/
│   ├── state.py
│   ├── context.py
│   ├── scene.py
│   ├── middleware.py
│   ├── strategy.py
│   └── storage/    (memory/redis/mongo/pymongo)
├── filters/        ←→   filters/
├── handlers/       ←→   handlers/
├── types/          ←→   types/        (اما محتوا متفاوت)
├── enums/          ←→   enums/        (محتوای متفاوت)
├── methods/        ←→   methods/      (محتوای متفاوت)
├── utils/          ←→   utils/        (magic_filter سفارشی، backoff، …)
├── webhook/        ←→   webhook/
└── exceptions.py   ←→   exceptions.py
```

### تفاوت‌های ساختاری عمده (برای Migration Guide)

1. **نوع شناسه‌ها:** در aiorubi همه شناسه‌ها `str` هستند، نه `int`. این به‌خاطر ماهیت Rubika API است.
   - `chat_id: str`
   - `message_id: str`
   - `user_id: str`
   - `bot_id: str`

2. **مدل پیام:** aiorabi یک `Message` یکپارچه دارد که همه انواع محتوا را در زیرخود نگه می‌دارد:
   ```python
   class Message(RubikaObject):
       message_id: str
       time: DateTime
       chat_id: str | None
       sender_type: str | None   # 'User' / 'Bot'
       sender_id: str | None
       text: str | None
       is_edited: bool
       aux_data: AuxData | None
       file: File | None          # تصویر، ویدیو، صدا، استیکر، فایل
       reply_to_message_id: str | None
       forwarded_from: ForwardedFrom | None
       forwarded_no_link: ... | None
       location: Location | None
       sticker: Sticker | None
       contact_message: ContactMessage | None
       poll: Poll | None
       metadata: MetaData | None
   ```
   نه `.photo` نه `.video` نه `.voice` به عنوان attribute مستقیم وجود ندارند؛ همه زیر `.file` (یا `.sticker` برای استیکر) جمع می‌شوند.

3. **رویدادها (Observers):**
   ```
   aiogram                                   aiorubi
   ─────────────────────────────────────────────────────
   message / edited_message / ...            new_message / updated_message / removed_message
   callback_query                            inline_message
   my_chat_member / chat_member              started_bot / stopped_bot
   ```
   در aiorabi، Rubika فقط یک نوع آپدیت خام به نام `Update` تحویل می‌دهد و Dispatcher آن را بر اساس `update.type` به observer مناسب می‌فرستد.

4. **شورت‌کات‌های Message:**
   ```python
   msg.reply(text) / msg.answer(text)
   msg.reply_file(...) / msg.answer_file(...)
   msg.reply_gif / answer_gif
   msg.reply_image / answer_image
   msg.reply_music / answer_music
   msg.reply_video / answer_video
   msg.reply_voice / answer_voice
   ```
   این‌ها به coroutine تبدیل می‌شوند (با `await` فراخوانی شوند).

5. **پشتیبانی از HTML/Markdown:** فعلاً غیرفعال است (کامنت شده). فقط پیام متنی ساده پشتیبانی می‌شود.

6. **Keypad به‌جای دو نوع مختلف:** فقط یک ساختار `Keypad` وجود دارد. در زمان ارسال می‌گویید `inline_keypad=...` یا `chat_keypad=...` (کیبورد پایین چت).

7. **موقعیت مکانی:** `send_location(latitude, longitude)` در aiorubi هر دو به صورت `str | float` پذیرفته می‌شوند.

8. **دکمه‌ها:** دکمه‌ها چند نوع‌اند (همه با هم در یک Keypad قابل ترکیب):
   - `Button` — ساده (متنی، لینک)
   - `ButtonSelection` — انتخابگر
   - `ButtonSelectionItem` — آیتم انتخابگر
   - `ButtonCalendar` — تقویم
   - `ButtonNumberPicker` — انتخاب عدد
   - `ButtonStringPicker` — انتخاب رشته
   - `ButtonTextbox` — ورودی متنی
   - `ButtonLocation` — درخواست مکان

9. **Commandها:** فقط `set_commands` (محدود، فقط یک لیست ساده). scope پیچیدهٔ aiogram وجود ندارد.

---

## 3. Bot — کلاینت سطح بالا

فایل: `aiorubi/client/bot.py` (~890 خط).

### سازنده

```python
Bot(
    token: str,
    session: BaseSession | None = None,
    default: DefaultBotProperties | None = None,
    **kwargs,
)
```

- اگر `session` ندادید → `AiohttpSession()` ساخته می‌شود.
- اگر `default` ندادید → `DefaultBotProperties()` ساخته می‌شود.
- **استثنا:** `TokenValidationError` (در `utils/token.py`) — توکن باید شروع به حرف بزرگ و الگوی درست داشته باشد.

### خصوصیات مهم

- `bot.token` → str (خصوصی)
- `bot.id` → str (اگر `bot._me` لود نشده باشد، `RuntimeError` می‌دهد؛ برای لود کردن باید `await bot.me()` یا `await bot.get_me()` صدا بزنید)
- `bot.session` → `BaseSession` (پیش‌فرض `AiohttpSession`)
- `bot.default` → `DefaultBotProperties`

### متدهای Bot (به ترتیب موضوع)

#### فراخوانی متد
- `await bot(method: RubikaMethod[T])` → `T` — فراخوانی سطح پایین.

#### اطلاعات بات
- `await bot.get_me() → BotInfo` — getMe.
- `await bot.me() → BotInfo` (کش‌شده).

#### دانلود فایل
- `await bot.download_file(url, destination=None, timeout=30, chunk_size=65536, seek=True) → BinaryIO | None`
- `await bot.download(file: str | Downloadable, destination=None, timeout=30, chunk_size=65536, seek=True) → BinaryIO | None`
  - اگر `file` رشته باشد، به عنوان `file_id` تفسیر می‌شود؛ در غیر این صورت باید `Downloadable` باشد.
  - اگر `destination` ندهید → `io.BytesIO()` ساخته می‌شود.

#### آپلود فایل
- `await bot.upload_file(url, file: InputFile, request_timeout=None) → File`
  - این متد low-level است؛ معمولاً نباید مستقیم صدا زده شود.

#### چت
- `await bot.get_chat(chat_id) → Chat`
- `await bot.get_file(file_id) → DownloadUrl`
- `await bot.get_updates(offset_id=None, limit=None) → GetUpdatesResponse`

#### دستورات
- `await bot.set_commands(bot_commands: list[BotCommand]) → bool`

#### Webhook
- `await bot.update_bot_endpoints(url, type: UpdateEndpointType) → UpdateEndpointsStatus`

#### ارسال پیام
- `await bot.send_message(chat_id, text, *, reply_to_message_id=None, metadata=None, disable_notification=None, inline_keypad=None, chat_keypad=None, chat_keypad_type=None, request_timeout=None) → MessageID`
- `await bot.send_contact(chat_id, first_name, phone_number, *, last_name=None, ...) → MessageID`
- `await bot.send_poll(chat_id, question, options: list[str], *, type=None, allows_multiple_answers=None, is_anonymous=None, correct_option_index=None, explanation=None, ...) → MessageID`
- `await bot.send_location(chat_id, latitude, longitude, *, ...) → MessageID`

#### ارسال فایل (و شورت‌کات‌ها)
- `await bot.send_file(chat_id, file: str | InputFile, *, file_type: FileType = FileType.FILE, text=None, ...) → MessageID`
  - اگر `file` رشته باشد، به عنوان `file_id` تفسیر می‌شود (مرحلهٔ آپلود رد می‌شود).
  - در غیر این صورت، `InputFile` ابتدا با `request_send_file(file_type)` و سپس `upload_file` آپلود می‌شود.
- شورت‌کات‌ها (همگی فقط `file_type` را برای‌شان تنظیم می‌کنند و `send_file` را صدا می‌زنند):
  - `send_gif(file_type=FileType.GIF)`
  - `send_image(file_type=FileType.IMAGE)`
  - `send_music(file_type=FileType.MUSIC)`
  - `send_video(file_type=FileType.VIDEO)`
  - `send_voice(file_type=FileType.VOICE)`

#### ویرایش و حذف
- `await bot.edit_message_text(chat_id, message_id, text, *, metadata=None) → bool`
- `await bot.edit_message_keypad(chat_id, message_id, inline_keypad: Keypad) → bool`
- `await bot.edit_chat_keypad(chat_id, chat_keypad: Keypad) → bool`
- `await bot.remove_chat_keypad(chat_id) → bool`
- `await bot.delete_message(chat_id, message_id) → bool`

#### فوروارد
- `await bot.forward_message(from_chat_id, to_chat_id, message_id, *, disable_notification=False) → MessageID`

#### مدیریت عضو
- `await bot.ban_chat_member(chat_id, user_id) → bool`
- `await bot.unban_chat_member(chat_id, user_id) → bool`

#### context manager
- `async with bot:` → بستن خودکار session.
- `bot.context(auto_close=True)` — اگر False بگذارید، session بعداً بسته نمی‌شود.

### قوانین عمومی Bot

- Bot قابل hash شدن است (بر اساس token). دو Bot با token یکسان، برابر در نظر گرفته می‌شوند.
- فراخوانی مستقیم `bot(call, request_timeout=...)` الگوی سطح پایین برای اجرای متد است؛ شورت‌کات‌های Bot در بیرون فقط یک `RubikaMethod` می‌سازند و `__call__` را صدا می‌زنند.
- اکثر متدهای ارسال یکسان ساختار یکسانی دارند: ساختن RubikaMethod → فراخوانی از طریق `bot(call)` → برگرداندن نتیجه.

---

## 4. Dispatcher و Router

### Dispatcher (فایل: `dispatcher/dispatcher.py`)

```python
Dispatcher(
    *,
    storage: BaseStorage | None = None,
    fsm_strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
    events_isolation: BaseEventIsolation | None = None,
    disable_fsm: bool = False,
    name: str | None = None,
    **kwargs,
)
```

#### رفتار درونی
- در سازنده، observer به نام `update` (RubikaEventObserver) ساخته می‌شود که handler پیش‌فرض آن `_listen_update` است.
- این handler، نوع آپدیت (`UpdateType`) را می‌خواند و آپدیت را به observer تخصصی می‌فرستد (مثلاً `new_message`, `inline_message`, ...).
- `ErrorsMiddleware` به‌عنوان outer middleware اول روی `update` نصب می‌شود.
- `UserContextMiddleware` بعد از آن نصب می‌شود (برای cache کردن اطلاعات user/chat).
- اگر `disable_fsm=False` (پیش‌فرض)، `FSMContextMiddleware` بعد از آن نصب می‌شود.
- `dispatcher.fsm.close` به‌عنوان shutdown callback ثبت می‌شود.

#### متدهای مهم Dispatcher

- `await dispatcher.feed_update(bot, update, **kwargs) → Any` — نقطهٔ ورودی برای آپدیت‌ها.
- `await dispatcher.feed_raw_update(bot, update_dict, **kwargs) → Any` — خودش دیکشنری را به `Update` تبدیل می‌کند.
- `await dispatcher.feed_webhook_update(bot, update, _timeout=55, **kwargs) → RubikaMethod | None` — برای webhook؛ اگر handler بیش از 55 ثانیه طول بکشد، در پس‌زمینه ادامه می‌دهد و مقدار برگشتی به صورت silent call ارسال می‌شود.
- `await dispatcher.poll(bot, *, limit=100, polling_interval=0.5, handle_as_tasks=True, backoff_config=None, tasks_concurrency_limit=None, ...)` — شروع polling.
- `await dispatcher.silent_call_request(bot, result: RubikaMethod) → None` — برای شبیه‌سازی پاسخ webhook.
- `dispatcher.startup` و `dispatcher.shutdown` → `EventObserver` برای هوک‌های startup/shutdown.
- `dispatcher.workflow_data: dict` — داده‌های سراسری قابل دسترسی از طریق `dispatcher["key"]` یا `dispatcher.get("key", default)`.
- `dispatcher.fsm: FSMContextMiddleware`
- `dispatcher.storage: BaseStorage` (alias از `fsm.storage`)

#### نکات
- `Dispatcher` ریشه است؛ نمی‌توان آن را به یک Router/Dispatcher دیگر include کرد.
- `parent_router` در Dispatcher همیشه `None` و ست کردنش خطا می‌دهد.

### Router (فایل: `dispatcher/router.py`)

```python
Router(name: str | None = None)
```

- Observers پیش‌فرض: `new_message`, `updated_message`, `removed_message`, `inline_message`, `started_bot`, `stopped_bot`, `error`/`errors`.
- `startup` و `shutdown` → EventObserver (مثل aiogram).
- `sub_routers: list[Router]`
- `parent_router: Router | None` (read-only عمومی؛ باید از طریق `include_router` تنظیم شود).

#### متدهای Router
- `include_router(router) → Router`
- `include_routers(*routers)`
- `resolve_used_update_types(skip_events=None) → list[str]` — استفاده برای اینکه polling/webhook فقط observerهای دارای handler را فعال کند.
- `await router.emit_startup(*args, **kwargs)` و `emit_shutdown` — برای recursive startup/shutdown.
- `await router.propagate_event(update_type, event, **kwargs)` — داخلی، برای propagate کردن رویداد در زنجیرهٔ routerها.

#### Chain helpers
- `router.chain_head` → generator از root تا خود router.
- `router.chain_tail` → generator از خود router تا آخرین sub-router.

---

## 5. FSM

### State و StatesGroup (`fsm/state.py`)

```python
class State:
    def __init__(self, state: str | None = None, group_name: str | None = None) -> None: ...

class StatesGroup(metaclass=StatesGroupMeta):
    """ گروهی از State ها. """
```

نمونه:
```python
from aiorubi.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()      # state = "Form:name"
    age = State()       # state = "Form:age"
```

- `state.state` → `"Form:name"` (نام گروه + نام state)
- `state == "*"` → wildcard (هر state)
- `default_state = State()` — برای «هیچ state»
- `any_state = State(state="*")` — برای هر state

### FSMContext (`fsm/context.py`)

```python
class FSMContext:
    storage: BaseStorage
    key: StorageKey

    async def set_state(state: StateType = None) -> None
    async def get_state() -> str | None
    async def set_data(data: Mapping[str, Any]) -> None
    async def get_data() -> dict[str, Any]
    async def get_value(key, default=None) -> Any
    async def update_data(data=None, **kwargs) -> dict[str, Any]
    async def clear() -> None   # state=None و data={}
```

### Storage (`fsm/storage/`)

- `BaseStorage` (ABC): متدهای `set_state`, `get_state`, `set_data`, `get_data`, `get_value`, `update_data`, `close`.
- `MemoryStorage` — پیش‌فرض، در حافظه.
- `RedisStorage` — نیاز به extra `redis` و `redis[hiredis]`.
- `MongoStorage` (motor) — نیاز به extra `mongo`.
- `PymongoStorage` (pymongo) — نیاز به extra `mongo`.

### StorageKey

```python
@dataclass(frozen=True)
class StorageKey:
    bot_id: str
    chat_id: str
    user_id: str
    destiny: str = "default"
```

### KeyBuilder

- `KeyBuilder` (ABC) با متد `build(key, part) → str`.
- `DefaultKeyBuilder(prefix="fsm", separator=":", with_bot_id=False, with_destiny=False)`.

### BaseEventIsolation

- برای lock کردن رویدادها در سطح FSM (مثلاً جلوگیری از race بین handlerهای هم‌زمان یک کاربر).
- `DisabledEventIsolation` — پیش‌فرض، بدون قفل.

### Strategy

- `FSMStrategy` (enum): نحوهٔ تفسیر storage key. پیش‌فرض `USER_IN_CHAT`.

### Scenes (Wizard) (`fsm/scene.py`)

یک مفهوم اختیاری برای مکالمات چندمرحله‌ای پیچیده:

- `class Scene` (با `__init_subclass__` برای ثبت handlers).
- `Scene.as_handler(**kwargs)` → یک entry handler برمی‌گرداند که می‌توان آن را روی یک command مثل `Command("start")` ثبت کرد.
- `Scene.as_router(name=None) → Router`.
- `@scene.on_event("new_message", ...filters...)` یا از طریق کلاس‌های داخلی.
- اکشن‌ها: `SceneAction.enter`, `leave`, `exit`, `back`.
- `SceneWizard.goto(scene)`, `leave()`, `exit()`, `back()`.
- `HistoryManager` — برای push/pop در history.

---

## 6. Filters

فایل‌ها در `aiorubi/filters/`:

- `base.py`: کلاس‌های پایه (معمولاً از Filter در magic-filter ارث می‌برند).
- `command.py`: `Command` (و احتمالاً `CommandObject`).
- `state.py`: `StateFilter`.
- `callback_data.py`: `CallbackData` (Factory + Filter).
- `magic_data.py`: `MagicData`.
- `logic.py`: ترکیب‌کننده‌های AND/OR/NOT.
- `exception.py`: `ExceptionMessageFilter`.

### MagicFilter

```python
from aiorubi import F

@dispatcher.new_message()
async def handler(msg: Message):
    if F.text == "hello":
        ...

# یا به‌عنوان decorator filter
@dispatcher.new_message(F.text.startswith("/"))
```

`MagicFilter.as_(name)` → نتیجه را در `data[name]` ذخیره می‌کند (برای injection در handler).

### StateFilter

برای اتصال handler به یک state خاص.

### Command

```python
from aiorubi.filters.command import Command

@dispatcher.new_message(Command("start"))
async def handler(msg: Message): ...
```

پارامترها: `commands`, `prefix` (پیش‌فرض "/"), `ignore_case` (پیش‌فرض True)، `ignore_state`.

### CallbackData

مکانیزم ساخت‌یافته برای دکمه‌های inline_message (مشابه aiogram).

```python
from aiorubi.filters.callback_data import CallbackData

cb = CallbackData("action", "id")

@dispatcher.inline_message(cb.filter())
async def handler(call, callback_data):
    ...
```

---

## 7. Handlers

فایل‌ها در `aiorubi/handlers/`:

- `base.py`: `BaseHandler`.
- `message.py`: handler برای messageها.
- `inline_message.py`: handler برای inline messageها (دکمه‌ها).
- `poll.py`: handler برای pollها.
- `error.py`: error handler.

(این handlerها عموماً به صورت داخلی توسط decoratorهای Dispatcher/Router استفاده می‌شوند و لازم نیست کاربر مستقیماً از آن‌ها استفاده کند.)

---

## 8. Middlewares

فایل‌ها در `aiorubi/dispatcher/middlewares/`:

- `base.py`: `BaseMiddleware` (کلاس پایه).
- `manager.py`: `MiddlewareManager`.
- `error.py`: `ErrorsMiddleware` (نصب خودکار).
- `user_context.py`: `UserContextMiddleware` (نصب خودکار).

### الگو

```python
class MyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # before
        result = await handler(event, data)
        # after
        return result
```

### نصب

```python
router.new_message.outer_middleware(MyMiddleware())
router.new_message.middleware(MyMiddleware())  # inner
```

یا روی خود Dispatcher (در سازنده، outer نصب می‌شود).

---

## 9. Types — مدل‌های پایامی

### Update (`types/update.py`)

```python
class Update(RubikaObject):
    type: UpdateType       # NEW_MESSAGE / UPDATED_MESSAGE / ...
    chat_id: str
    new_message: Message | None
    updated_message: Message | None
    removed_message: RemovedMessage | None
    inline_message: InlineMessage | None
    started_bot: StartedBot | None
    stopped_bot: StoppedBot | None
    update_time: DateTime | None

    @property
    def event_type(self) -> str  # "new_message" / "inline_message" / ...
    @property
    def event(self) -> RubikaObject
    @property
    def message_id(self) -> str | None
```

یک `model_validator` در حالت `before` دارد که:
- envelope `{"update": {...}}` را باز می‌کند.
- برای inline_message بدون type، type را `INLINE_MESSAGE` می‌گذارد.
- `new_message` و `updated_message` را با `chat_id` پدر mix می‌کند.
- اگر `removed_message_id` خام بیاید، آن را به `RemovedMessage` تبدیل می‌کند.
- برای `STARTED_BOT` / `STOPPED_BOT`، دادهٔ کمینه می‌سازد.

### Message

(در بخش ۲ بالا توضیح داده شد.)

### MessageID

```python
class MessageID(RubikaObject):
    message_id: str
```

### RemovedMessage

```python
class RemovedMessage(RubikaObject):
    message_id: str
    chat_id: str | None
```

### StartedBot / StoppedBot

```python
class StartedBot(RubikaObject):
    chat_id: str | None

class StoppedBot(RubikaObject):
    chat_id: str | None
```

### InlineMessage

پیامی که در پاسخ به کلیک روی دکمهٔ شیشه‌ای (inline keypad) می‌آید.

### Chat

اطلاعات چت (group/channel/private).

### AuxData

```python
class AuxData(RubikaObject):
    start_id: str | None
    button_id: str | None
```

### File

```python
class File(RubikaObject):
    file_id: str
    file_name: str | None
    mime_type: str | None
    ...
```

### Location

```python
class Location(RubikaObject):
    latitude: str | float
    longitude: str | float
```

### Sticker

### ContactMessage

```python
class ContactMessage(RubikaObject):
    first_name: str
    last_name: str | None
    phone_number: str
```

### Poll / PollStatus

### ForwardedFrom / ForwardedNoLink

### MetaData / MetaDataPart

### Keypad / KeypadRow

```python
class Keypad(RubikaObject):
    rows: list[KeypadRow]

class KeypadRow(RubikaObject):
    buttons: list[Button]   # یا subclassها
```

### Button (پایه) و زیرکلاس‌ها

- `Button` — ساده.
- `ButtonSelection` / `ButtonSelectionItem`.
- `ButtonCalendar`.
- `ButtonNumberPicker`.
- `ButtonStringPicker`.
- `ButtonTextbox`.
- `ButtonLocation`.

### BotInfo

```python
class BotInfo(RubikaObject):
    bot_id: str
    bot_title: str
    username: str | None
    ...
```

### BotCommand

```python
class BotCommand(RubikaObject):
    command: str
    description: str
```

### InputFile

برای آپلود فایل. می‌تواند از مسیر، URL، bytes، یا `io.IOBase` ساخته شود.

### Downloadable / DownloadUrl / UploadUrl

برای متد download.

### GetUpdatesResponse

```python
class GetUpdatesResponse(RubikaObject):
    updates: list[Update]
    next_offset_id: str | None
```

### ResponseParameters

### ErrorEvent

```python
class ErrorEvent(RubikaObject):
    exception: Exception
    update: Update | None
```

---

## 10. Enums

فایل‌ها در `aiorubi/enums/`:

- `UpdateType`: `NEW_MESSAGE`, `UPDATED_MESSAGE`, `REMOVED_MESSAGE`, `INLINE_MESSAGE`, `STARTED_BOT`, `STOPPED_BOT`.
- `UpdateEndpointType`: نوع endpoint (مثل `RECEIVE_UPDATE`).
- `UpdateEndpointStatusType`.
- `PollType`: نوع نظرسنجی (مثلاً `REGULAR`, `QUIZ`).
- `PollStatus`: وضعیت (Open/Closed).
- `MetadataType`: نوع entity در متن (link، mention، ...).
- `MessageSenderType`: `USER`, `BOT`.
- `ForwardedFromType`.
- `FileType`: `IMAGE`, `VIDEO`, `VOICE`, `MUSIC`, `GIF`, `FILE`, `STICKER`, ...
- `ChatType`: `PRIVATE`, `GROUP`, `CHANNEL`.
- `ChatKeypadType`: `NEW`, `REMOVE`.
- `ButtonType`: نوع دکمه.
- `ButtonTextboxTypeLine`, `ButtonTextboxTypeKeypad`.
- `ButtonSelectionType`, `ButtonSelectionSearch`, `ButtonSelectionGet`.
- `ButtonLocationType`.
- `ButtonCalendarType`.

---

## 11. Exceptions

- `aiorubi.exceptions`:
  - `RubikaAPIError(Exception)` — خطای کلی API.
  - `SceneException(Exception)` — خطای Scene.
  - زیرکلاس‌های احتمالی برای خطاهای خاص (مثل validation، rate limit).

---

## 12. Methods (لایهٔ پایین)

در `aiorubi/methods/`:

- `base.py`: `RubikaMethod`, `Request`, `Response`.
- هر متد یک کلاس مستقل است: `SendMessage`, `SendFile`, `EditMessageText`, `GetUpdates`, ...

### RubikaMethod

کلاس پایه برای همهٔ متدها. احتمالاً یکی از pydantic.BaseModel یا Generic[T] است.

### نگاشت به Rubika Bot API endpoint

هر متد نگاشت می‌شود به URL:
```
https://botapi.rubika.ir/v3/{token}/{endpoint}
```

مثلاً `SendMessage` → `sendMessage`.

### الگوی فراخوانی

```python
result: SomeReturnType = await bot(SendMessage(chat_id="...", text="..."))
```

---

## 13. Utils

- `utils/magic_filter.py`: `MagicFilter` (extension از magic-filter).
- `utils/token.py`: `validate_token`.
- `utils/payload.py`: `build_payload`.
- `utils/backoff.py`: `Backoff`, `BackoffConfig` (برای retry در polling).
- `utils/dataclass.py`: ابزار dataclass.
- `utils/formatting.py`: قالب‌بندی متن (HTML/Markdown غیرفعال).
- `utils/text_decorations.py`: HTML/Markdown decorators (فعلاً کامنت شده).
- `utils/link.py`: ساخت لینک عمیق (مثل `https://rubika.ir/joingroup/...`).
- `utils/deep_linking.py`: ابزارهای مرتبط با deep link.
- `utils/magic_filter.py`: `MagicFilter` (پوشش برای magic-filter).
- `utils/warnings.py`: helperهای warning.
- `utils/mypy_hacks.py`: lru_cache (برای سازگاری).
- `utils/class_attrs_resolver.py`: ابزار MRO attribute resolution.

---

## 14. Webhook

- `webhook/aiohttp_server.py`: `SimpleWebhookServer` یا مشابه.
- `webhook/security.py`: helperهای امنیتی.

### الگو

```python
from aiorubi.webhook.aiohttp_server import SimpleWebhookServer

async def handler(update: dict):
    await dp.feed_raw_update(bot, update)

server = SimpleWebhookServer(token=bot.token, handler=handler)
await server.run_app(...)
```

---

## 15. Session

- `client/session/base.py`: `BaseSession` (ABC).
- `client/session/aiohttp.py`: `AiohttpSession` (پیاده‌سازی با aiohttp).
- `client/session/middlewares/`: middlewareهای سطح session (proxy, logging).

### تنظیم پروکسی

نیاز به extra `proxy`:
```python
from aiohttp_socks import ProxyConnector

connector = ProxyConnector.from_url("socks5://user:pass@host:port")
session = AiohttpSession(connector=connector)
bot = Bot(token, session=session)
```

---

## 16. نمونهٔ کامل Hello World

```python
import asyncio
import logging

from aiorubi import Bot, Dispatcher, F
from aiorubi.filters.command import Command

BOT_TOKEN = "YOUR_RUBIKA_BOT_TOKEN"

dp = Dispatcher()


@dp.new_message(Command("start"))
async def cmd_start(message):
    await message.reply(f"سلام، {message.sender_id}!")


@dp.new_message(F.text)
async def echo(message):
    await message.answer(message.text)


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 17. ساختار پیشنهادی مستندات (`docs/`)

```
docs/
├── conf.py
├── index.rst                    # صفحهٔ اصلی
├── quickstart.rst               # نصب + Hello World
├── installation.rst             # pip + extras + از سورس
├── migration-from-aiogram.rst   # تفاوت‌ها
├── guide/
│   ├── index.rst
│   ├── dispatcher.rst
│   ├── router.rst
│   ├── fsm.rst
│   ├── filters.rst
│   ├── middlewares.rst
│   ├── handlers.rst
│   ├── flags.rst
│   ├── scenes.rst
│   ├── webhook.rst
│   └── polling.rst
├── tutorial/
│   ├── index.rst
│   ├── 01_intro.rst
│   ├── 02_commands.rst
│   ├── 03_messages_and_filters.rst
│   ├── 04_keypads.rst
│   ├── 05_files.rst
│   ├── 06_fsm.rst
│   ├── 07_router.rst
│   ├── 08_middlewares.rst
│   └── 09_webhook.rst
├── utils/
│   ├── index.rst
│   ├── magic_filter.rst
│   ├── keyboard.rst
│   └── i18n.rst
└── api/
    ├── index.rst
    ├── client/
    │   ├── bot.rst
    │   └── session.rst
    ├── dispatcher/
    │   ├── dispatcher.rst
    │   ├── router.rst
    │   └── middlewares.rst
    ├── fsm/
    │   ├── state.rst
    │   ├── context.rst
    │   ├── scene.rst
    │   └── storage/
    ├── filters.rst
    ├── types.rst
    ├── enums.rst
    ├── methods.rst
    ├── handlers.rst
    ├── webhook.rst
    └── utils.rst
```

---

## 18. تنظیمات `conf.py`

```python
project = "aiorubi"
author = "Amir S. Farahani"
copyright = f"{datetime.date.today().year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinx_rtd_theme",  # یا furo
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

html_theme = "furo"
```

---

## 19. چیزهایی که **نباید** حدس بزنیم

اگر در هنگام نوشتن مستندات به نکتهٔ مبهمی برخوردی، **از این لیست عبور کن و سؤال بپرس** (یا به صورت «TBD» علامت بزن و در review بررسی کن):

1. URL endpoint‌های دقیق Rubika Bot API برای هر متد (فقط چند مورد در bot.py کامنت شده‌اند).
2. ترتیب دقیق پارامترهای برخی متدهای ارسال.
3. خروجی دقیق `GetUpdates` وقتی آپدیتی نیست.
4. رفتار `forwarded_no_link` (str یا شیء؟).
5. محدودیت‌های rate limit (اگر Rubika چنین چیزی دارد).
6. مستندات رسمی `keypad` و انواع دکمه‌ها (در حال حاضر فقط انواع از کد قابل استخراج‌اند).

---

## 20. نگاشت سریع مفاهیم aiogram → aiorubi (برای reviewerها)

| aiogram مفهوم | aiorubi معادل |
|---|---|
| `Bot` | `Bot` |
| `Dispatcher` | `Dispatcher` |
| `Router` | `Router` |
| `F` | `F` |
| `flags` | `flags` |
| `Message` | `Message` (یکپارچه) |
| `Message.text` | `Message.text` |
| `Message.photo` | `Message.file` (اگر `file.file_type == IMAGE`) |
| `Message.voice` | `Message.file` (اگر `file.file_type == VOICE`) |
| `CallbackQuery` | `InlineMessage` (event: `inline_message`) |
| `InlineKeyboardMarkup` | `Keypad` (هنگام ارسال: `inline_keypad=...`) |
| `ReplyKeyboardMarkup` | `Keypad` (هنگام ارسال: `chat_keypad=...`) |
| `ReplyKeyboardRemove` | `edit_chat_keypad` با `ChatKeypadType.REMOVE` |
| `State`, `StatesGroup` | `State`, `StatesGroup` |
| `FSMContext` | `FSMContext` |
| `Scene`, `SceneWizard` | `Scene`, `SceneWizard` |
| `Command("start")` | `Command("start")` |
| `CallbackData` | `CallbackData` |
| `MagicData` | `MagicData` |
| `MemoryStorage` | `MemoryStorage` |
| `RedisStorage` | `RedisStorage` |
| `MongoStorage` | `MongoStorage` |
| `S3Storage` | ندارد (می‌توان نوشت) |
| `dp.start_polling(bot)` | `dp.start_polling(bot)` (هم‌نام) |
| `dp.feed_update(bot, update)` | `dp.feed_update(bot, update)` |
| `dp.feed_webhook_update` | `dp.feed_webhook_update` |
| `Bot.send_message` | `Bot.send_message` |
| `Message.reply(text)` | `Message.reply(text)` |
| `Message.answer(text)` | `Message.answer(text)` |
| `Message.answer_photo(...)` | `Message.answer_image(...)` |
| `Message.answer_voice(...)` | `Message.answer_voice(...)` |
| `Bot.download_file` | `Bot.download_file` |
| `Bot.download` | `Bot.download` |
| `Bot.session` | `Bot.session` |
| `chat_id: int` | `chat_id: str` |
| `message_id: int` | `message_id: str` |

---

**پایان PACKAGE_OVERVIEW.md**