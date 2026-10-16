# aiorubi reference: FSM and Scenes

Verified against `aiorubi/fsm/` (v1.2.x).

## States

```python
from aiorubi.fsm.state import State, StatesGroup, default_state, any_state
from aiorubi.fsm.context import FSMContext   # for type hints

class Order(StatesGroup):
    waiting_name = State()      # full name: "Order:waiting_name"
    waiting_qty = State()
    confirm = State()
```

- `StatesGroup` subclasses declare `State()` class attributes; state strings are
  `"Group:state"` (nested groups nest further: `"Group:Child:state"`).
- `default_state` = no state (None); `any_state` matches everything (`"*"`).
- A `State` object can be passed **directly as a filter** (it is `StateFilter`
  sugar), as can a `StatesGroup` class or instance.

## FSMContext

Injected into handlers as the `state` kwarg (unless `Dispatcher(disable_fsm=True)`):

```python
@dp.new_message(Command("order"))
async def start_order(message, state: FSMContext):
    await state.set_state(Order.waiting_qty)
    await state.update_data(item=message.text)

@dp.new_message(Order.waiting_qty)                    # State as filter
async def get_qty(message, state: FSMContext):
    data = await state.update_data(qty=message.text)
    await state.set_state(None)                       # or state.clear() for state+data
    await message.answer(f"Ordered {data['item']} x{data['qty']}")
```

Methods: `set_state(state=None)`, `get_state() -> str | None`,
`set_data(mapping)`, `get_data() -> dict`, `get_value(key, default=None)`,
`update_data(**kwargs) -> dict` (merge), `clear()` (state + data).

**Escape-hatch pattern**: register the cancel handler *before* state-bound ones —
first matching handler wins:

```python
@dp.new_message(Command("cancel"), any_state)   # any_state or StateFilter(any_state)
async def cancel(message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled.")
# ... state-bound handlers registered AFTER this
```

### FSM strategy

`Dispatcher(fsm_strategy=...)` with `aiorubi.fsm.strategy.FSMStrategy`:
default `USER_IN_CHAT`; also `CHAT` (per chat, ignoring user) and
`GLOBAL_USER` (per user across chats).

### Storages

Default is in-process `MemoryStorage`. Persistent options (extras:

```python
from aiorubi.fsm.storage.memory import MemoryStorage
from aiorubi.fsm.storage.redis import RedisStorage        # needs redis extra
from aiorubi.fsm.storage.mongo import MongoStorage        # motor; deprecated
from aiorubi.fsm.storage.pymongo import PymongoStorage    # pymongo

dp = Dispatcher(storage=RedisStorage.from_url("redis://localhost:6379/0"))
```

- `RedisStorage.from_url(...)`; `RedisStorage.create_isolation()` for
  `SimpleEventIsolation` (per-key locking).
- `MongoStorage` is documented as deprecated (will be removed); prefer
  `PymongoStorage`.
- Keys: `StorageKey(bot_id, chat_id, user_id)` — all **`str`**; built by
  `DefaultKeyBuilder` (customizable via `KeyBuilder` subclass).
- Custom storage: subclass `BaseStorage` (async methods: `set_state`, `get_state`,
  `set_data`, `get_data`, `get_value`, `update_data`, `close`).

## Scenes (wizard-style FSM)

Scenes give multi-scene dialogs without hand-managing states. A `Scene` subclass
declares its own handler set; entering a scene switches the active handler set.

```python
from aiorubi.fsm.scene import Scene, on, After, SceneRegistry
from aiorubi.filters.command import Command

class Dialog(Scene, state="dialog"):
    @on.new_message(Command("cancel"))
    async def cancel(self, message):
        await self.wizard.exit()
        await message.answer("Bye!")

    @on.new_message(F.text)
    async def echo(self, message):
        await self.wizard.update_data(last=message.text)
        await message.answer(f"you said: {message.text}")

    @on.new_message(Command("done"), after=After.exit())
    async def done(self, message):
        await message.answer("Done.")
```

Key pieces (all in `aiorubi.fsm.scene`):

- `Scene` subclass with class kwarg `state="name"` (plus optional
  `reset_data_on_enter`, `reset_history_on_enter`, `inline_message_without_state`,
  `attrs_resolver`).
- `on` — an `OnMarker` with observers `new_message`, `updated_message`,
  `removed_message`, `inline_message`. Use as `@on.<observer>(*filters)`.
- `After` — post-handler transition: `After.exit()`, `After.back()`,
  `After.goto(SomeScene)`, or `after=After.enter(OtherScene)` via
  `@on...(..., after=...)` / `.enter(Scene)` / `.leave()` / `.back()` /
  `.exit()` action containers.
- `SceneWizard` — injected as `self.wizard` (constructor param of every scene
  instance): `await wizard.enter(scene)`, `wizard.leave()`, `wizard.exit()`,
  `wizard.back()`, `wizard.goto(scene)`, `wizard.retake()`, plus
  `set_data / get_data / get_value / update_data / clear_data`.
- Registration:

```python
from aiorubi.fsm.scene import SceneRegistry

registry = SceneRegistry(router=dp)
registry.add(Dialog)          # registers handlers + middleware automatically
```

- `SceneConfig` class kwargs control `reset_data_on_enter` / `reset_history_on_enter`;
  history is kept per user via `HistoryManager` (rolling size-10 snapshot for `back()`).
- `Scene.as_router(name=...)` can also produce a `Router` for manual inclusion.

## Deep dive

`docs/guide/fsm.rst`, `docs/guide/storages.rst`, `docs/guide/scenes.rst`,
`docs/tutorial/06_fsm.rst`.
