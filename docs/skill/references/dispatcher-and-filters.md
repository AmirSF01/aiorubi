# aiorubi reference: Dispatcher, routers, filters, middleware, flags

Verified against `aiorubi/dispatcher/` and `aiorubi/filters/` (v1.2.x).

## Dispatcher and Router

`Dispatcher` **subclasses `Router`** and is the root router. Routers group
handlers; the dispatcher is the entry point.

```python
from aiorubi import Dispatcher, Router

dp = Dispatcher(
    storage=None,            # FSM storage (default MemoryStorage)
    fsm_strategy=...,        # FSMStrategy
    events_isolation=None,   # e.g. SimpleEventIsolation()
    disable_fsm=False,       # True -> no state kwarg injected
    name=None,
    **kwargs,                # extra kwargs are injected into every handler (DI)
)
dp["my_service"] = Service()  # workflow_data — injected as `my_service` kwarg too

custom = Router(name="custom")
dp.include_router(custom)     # or dp.include_routers(r1, r2, ...)
```

Sub-router handlers run **after** the root router's; within a router,
**registration order** decides (first matching handler wins).

### Observers (event types)

Registered on any router via decorator or `.register(handler, *filters)`:

| Observer | Event object |
| --- | --- |
| `new_message` | `Message` |
| `updated_message` | `Message` (edited) |
| `removed_message` | `RemovedMessage` |
| `inline_message` | `InlineMessage` (button click) |
| `started_bot` | `StartedBot` |
| `stopped_bot` | `StoppedBot` |
| `errors` (alias `error`) | `ErrorEvent` |
| `startup` / `shutdown` | lifecycle callables |
| `update` (Dispatcher only) | raw `Update` — the split point |

```python
@dp.startup
async def on_startup(bot: Bot):
    ...

@dp.new_message(Command("start"))          # decorator
async def cmd(message): ...

async def echo(message): ...               # equivalent registration
dp.new_message.register(echo)
```

## Polling and webhook entry points

- `dp.start_polling(*bots, limit=100, polling_interval=0.5, handle_as_tasks=True,
  backoff_config=..., handle_signals=True, close_bot_session=True,
  tasks_concurrency_limit=None, **kwargs)` — main runner; built-in exponential
  backoff on failures.
- `dp.run_polling(*bots, ...)` — sync wrapper (calls `asyncio.run`, uses uvloop
  if installed).
- `dp.stop_polling()` — programmatic stop; raises `RuntimeError` if not running.
- `dp.feed_raw_update(bot, payload_dict)` / `dp.feed_update(bot, update)` —
  webhook entry points.

Auto-installed outer middlewares, in order: `ErrorsMiddleware` →
`UserContextMiddleware` → `FSMContextMiddleware` (skipped with `disable_fsm=True`).

## Filters

Filters are **positional** arguments to the decorator; all must pass; first
matching handler wins; handlers fire in registration order.

```python
from aiorubi import F
from aiorubi.filters import Command, StateFilter, MagicData, and_f, or_f, invert_f
from aiorubi.filters.command import CommandStart
```

### Magic filter `F`

Module-level `F` (custom `MagicFilter` with an extra `as_(name)` operation):

```python
@dp.new_message(F.text == "ping")
@dp.new_message(F.text.startswith("/"))
@dp.new_message(F.file)                                   # has any file
@dp.new_message(F.file.file_type == FileType.IMAGE)
@dp.new_message(F.aux_data.button_id == "cmd_list")       # chat keypad click
@dp.new_message(F.text.regexp(r"age:\d+"))
async def h(message): ...

@dp.new_message(F.text.as_("user_text"))                  # inject user_text=<text>
async def h(message, user_text: str): ...
```

### Built-in filters (`aiorubi.filters`, all exported from the package `__init__`)

- `Command(*values, commands=None, prefix="/", ignore_case=False,
  ignore_mention=False, magic=None)` — string or `re.Pattern` commands;
  `prefix` may be multiple chars like `"/!"`. Injects `command: CommandObject`
  into the handler (fields: `prefix`, `command`, `mention`, `args`,
  `regexp_match`; properties `mentioned`, `text`).
  `CommandStart` is `Command("start")` plus deep-link payload handling.
- `StateFilter(*states)` — matches FSM state; sugar: pass the `State` object
  directly as a filter. Use `default_state` / `any_state` sentinels.
- `MagicData(MagicFilter)` — resolves against the whole context
  (`event` + injected data), e.g. `MagicData(F.event.chat_id == "...")`.
- `ExceptionTypeFilter(Exception)` / `ExceptionMessageFilter(...)` — for error handlers.
- Combinators: `and_f(*filters)`, `or_f(*filters)`, `invert_f(filter)`.
- `Filter`/`BaseFilter` — subclass with `async def __call__(self, event, **kwargs)`
  returning `bool` or a `dict` of injected data.

```python
@dp.new_message(and_f(Command("greet"), F.text.regexp(r"greet \w+")))
async def greet(message, command: CommandObject):
    await message.answer(f"args: {command.args}")
```

Custom filter:

```python
class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.sender_id in ADMINS
```

### Flags

`flags` (exported from `aiorubi`) attaches per-handler metadata readable by
middlewares — `FlagGenerator` creates a decorator per attribute name:

```python
from aiorubi import flags

@flags.admin_only                    # -> {"admin_only": True}
@flags.rate_limit(2.5)               # -> {"rate_limit": 2.5}
@flags.permissions(write=True)       # keyword form -> AttrDict value
@dp.new_message(Command("ban"))
async def cmd_ban(message): ...
```

## Middleware

Two kinds — **outer** (run before filters) and **inner** (after filters). Attach
via `router.<observer>.outer_middleware(mw)` or `.middleware(mw)`.

```python
from aiorubi import BaseMiddleware

class Throttling(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if is_limited(event.sender_id):
            return                      # return without calling handler = block
        data["user"] = await load_user(event.sender_id)   # DI: injects `user` kwarg
        return await handler(event, data)

dp.new_message.outer_middleware(Throttling())
```

- Signature: `(handler, event, data)`. `data` is the dependency-injection dict —
  anything you put there becomes a handler keyword argument.
- `Dispatcher(**kwargs)` / `dp[...]` / `start_polling(..., **kwargs)` also feed
  the same `data` dict (`bots`, `dispatcher` are pre-populated).
- Handlers may declare any injected names as parameters: `user`, `state` (FSM),
  `command` (from `Command`), `button_id` (from `ButtonId.filter`), etc.

## Deep dive

`docs/guide/dispatcher.rst`, `docs/guide/router.rst`, `docs/guide/filter.rst`,
`docs/guide/middlewares.rst`, `docs/guide/flags.rst`.
