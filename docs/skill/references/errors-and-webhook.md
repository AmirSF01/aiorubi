# aiorubi reference: Errors and webhook deployment

Verified against `aiorubi/exceptions.py` and `aiorubi/webhook/` (v1.2.x).

## Exception hierarchy

```
AiorubiError                              # base (aiorubi.exceptions)
├── DetailedAiorubiError
│   ├── RubikaAPIError                    # API-level; has .method
│   │   ├── RubikaNetworkError            # HTTP client failures
│   │   ├── RubikaTooRequests             # flood control; .retry_after (may be None)
│   │   ├── RubikaInvalidInput
│   │   ├── RubikaInvalidAccess
│   │   └── RubikaServerError             # 5xx / SERVER_ERROR
│   └── UnsupportedKeywordArgument        # kwargs passed where filters expected
├── CallbackAnswerException
└── SceneException
```

Also: `ClientDecodeError` (malformed API response), `DataNotDictLikeError`,
and `TokenValidationError` (from `aiorubi.utils.token`, raised by `Bot(token)`).

Catch `RubikaAPIError` around API calls; it carries the failed
`.method` object.

## Error handlers

`@dp.errors(...)` (alias `@dp.error`) receives an `ErrorEvent` with
`.update` and `.exception`:

```python
from aiorubi.filters import ExceptionTypeFilter
from aiorubi.exceptions import RubikaAPIError
from aiorubi.types import ErrorEvent

@dp.errors(ExceptionTypeFilter(RubikaAPIError))
async def on_api_error(event: ErrorEvent):
    log.error("API call failed: %s", event.exception)

@dp.errors()                                   # catch-all — register LAST
async def on_any_error(event: ErrorEvent):
    ...
```

Errors that reach a handler **inside** processing propagate through
`ErrorsMiddleware` (auto-installed outer middleware), so a matching error
handler prevents unhandled-exception logs. `ExceptionTypeFilter(*types)` and
`ExceptionMessageFilter(...)` narrow which errors a handler takes.

## Webhook deployment

Rubika POSTs updates to your registered endpoint; the 60s server timeout means
your route should answer quickly.

### 1. Register the endpoint

```python
from aiorubi.enums import UpdateEndpointType

await bot.update_bot_endpoints(
    url="https://example.com/webhook",
    type=UpdateEndpointType.RECEIVE_UPDATE,
)
```

### 2a. aiohttp server with the built-in handler

```python
from aiohttp import web
from aiorubi.webhook.aiohttp_server import SimpleRequestHandler, setup_application

webhook = SimpleRequestHandler(dispatcher=dp, bot=bot)   # handle_in_background=True by default
app = web.Application()
webhook.register(app, "/webhook")
setup_application(app, dp, bot=bot)                      # wires startup/shutdown + workflow data

web.run_app(app, host="0.0.0.0", port=8080)
```

- `SimpleRequestHandler(dispatcher, bot, handle_in_background=True)` — one bot.
- `TokenBasedRequestHandler(dispatcher, bot_settings={...})` — multi-bot; resolves
  the bot from a `bot_token` path variable.
- `handle_in_background`: both concrete handlers default to `True` (the abstract
  `BaseRequestHandler` defaults to `False`). `True` feeds the update as a task
  and answers Rubika immediately; `False` awaits processing before responding —
  mind Rubika's 60s timeout.
- IP filtering helper: `ip_filter_middleware(ip_filter)`.

### 2. Manual (any framework)

```python
async def handle(request):                       # e.g. aiohttp route
    payload = await request.json()
    await dp.feed_raw_update(bot, payload)       # or feed_update(bot, Update(**payload))
    return web.Response(status=200)
```

`setup_application(app, dispatcher, **kwargs)` handles `startup`/`shutdown`
emission and injects `dispatcher.workflow_data` into handlers.

## Operational notes

- Polling has built-in exponential backoff
  (`BackoffConfig(min_delay=1.0, max_delay=5.0, factor=1.3, jitter=0.1)`).
- `RubikaTooRequests` (flood) may carry `retry_after`; Rubika does not always
  provide it — throttle proactively.
- Signal handling (`SIGINT`/`SIGTERM`) is skipped on Windows; on Windows stop
  via `dp.stop_polling()` or let `KeyboardInterrupt` propagate through
  `run_polling`.
- Close sessions: `start_polling` closes bot sessions by default
  (`close_bot_session=True`); with webhooks, call `handler.close()` /
  `bot.session.close()` in your app's shutdown hook.

## Deep dive

`docs/guide/webhook.rst`, `docs/tutorial/09_webhook.rst`.
