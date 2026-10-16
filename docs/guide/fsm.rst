====================
Finite State Machine
====================

The Finite State Machine (FSM) is aiorubi's mechanism for storing
per-conversation *state* and *data* between updates. It is what turns a
stateless ``new_message`` handler into a multi-step dialog: "What is your
name?" → "How old are you?" → "Done!".

If you have used aiogram 3.x, the FSM here works exactly the same way —
same classes, same methods, same storage model. The only platform-specific
detail is that all identifiers (``chat_id``, ``user_id``, ``bot_id``) are
strings, because Rubika issues string ids.

Quick example
=============

.. code-block:: python
   :caption: A two-step form

   from aiorubi import Bot, Dispatcher, F
   from aiorubi.filters.command import Command
   from aiorubi.fsm.state import State, StatesGroup
   from aiorubi.fsm.context import FSMContext

   class Form(StatesGroup):
       name = State()
       age = State()

   dp = Dispatcher()

   @dp.new_message(Command("start"))
   async def cmd_start(message, state: FSMContext):
       await state.set_state(Form.name)
       await message.answer("Hi! What is your name?")

   @dp.new_message(Form.name)
   async def process_name(message, state: FSMContext):
       await state.update_data(name=message.text)
       await state.set_state(Form.age)
       await message.answer("Nice to meet you. How old are you?")

   @dp.new_message(Form.age)
   async def process_age(message, state: FSMContext):
       data = await state.update_data(age=message.text)
       await state.clear()
       await message.answer(
           f"Got it: {data['name']}, {data['age']} years old."
       )

How it works:

#. Every incoming update flows through the built-in
   :class:`~aiorubi.fsm.middleware.FSMContextMiddleware`, which computes a
   :class:`~aiorubi.fsm.storage.base.StorageKey` for the update and puts an
   :class:`~aiorubi.fsm.context.FSMContext` instance into the handler's
   keyword arguments as ``state``.
#. The raw state string (or ``None``) is stored in the middleware context as
   ``raw_state`` — this is what filters such as ``StateFilter`` compare
   against, and what the :class:`~aiorubi.fsm.state.State` objects passed to
   the decorator match.
#. The handler reads and writes state and data through
   :class:`~aiorubi.fsm.context.FSMContext`, which delegates to the
   configured :doc:`storage <storages>` (memory by default).


States
======

State
-----

`aiorubi.fsm.state.State(state: str | None = None, group_name: str | None = None)`

A single FSM state. Usually you do not instantiate ``State`` directly with a
name — you declare it as a class attribute of a :class:`~aiorubi.fsm.state.StatesGroup`
and the group assigns the name for you:

.. code-block:: python

   from aiorubi.fsm.state import State, StatesGroup

   class Form(StatesGroup):
       name = State()   # Form.name.state == "Form:name"
       age = State()    # Form.age.state  == "Form:age"

The fully-qualified state string is ``"<Group>:<state>"``. For nested groups
the parent groups are joined with dots, e.g. ``"Registration:Profile:bio"``.

States can also be created standalone (without a group):

.. code-block:: python

   custom = State("my_state", group_name="custom")
   custom.state  # "custom:my_state"

Useful properties and behaviour:

* ``state.state`` — the fully-qualified state string (or ``None`` for
  :data:`~aiorubi.fsm.state.default_state`, or ``"*"`` for
  :data:`~aiorubi.fsm.state.any_state`).
* ``state.group`` — the owning :class:`~aiorubi.fsm.state.StatesGroup` class.
  Raises :class:`RuntimeError` for states that do not belong to a group.
* ``state == "Form:name"`` — states compare equal to their string form.
* ``state(event, raw_state)`` — callable predicate used by
  :class:`~aiorubi.fsm.filters.state.StateFilter`: returns ``True`` for
  ``any_state`` or when ``raw_state`` matches.

StatesGroup
-----------

`aiorubi.fsm.state.StatesGroup`

A group of states declared with a class body. The metaclass
(:class:`~aiorubi.fsm.state.StatesGroupMeta`) collects all ``State``
attributes and nested ``StatesGroup`` subclasses, and exposes them via
class-level attributes:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Attribute
     - Meaning
   * - ``__states__``
     - Tuple of the directly declared states.
   * - ``__state_names__``
     - Tuple of their fully-qualified names.
   * - ``__all_states__`` / ``__all_states_names__``
     - Same, but including states inherited from nested child groups.
   * - ``__childs__`` / ``__all_childs__``
     - Direct and transitive child groups.
   * - ``__full_group_name__``
     - Dot-joined group path, e.g. ``"Registration.Profile"``.

Membership checks work out of the box:

.. code-block:: python

   Form.name in Form            # True
   "Form:age" in Form           # True (string names are checked too)
   list(Form)                   # iterate over all states

Nested groups let you build state trees:

.. code-block:: python

   class Registration(StatesGroup):
       class Profile(StatesGroup):
           nickname = State()   # "Registration.Profile:nickname"
           bio = State()        # "Registration.Profile:bio"
       email = State()          # "Registration:email"

   Registration.get_root()      # <StatesGroup 'Registration'>

default_state and any_state
---------------------------

Two ready-made singletons are exported from :mod:`aiorubi.fsm.state`:

.. data:: default_state

   ``State()`` — matches "no state at all" (the state string is ``None``).
   Use it to register handlers that must only fire while the user is *not*
   inside any dialog:

   .. code-block:: python

      @dp.new_message(default_state)
      async def no_dialog(message):
          await message.answer("You are not in a dialog right now.")

.. data:: any_state

   ``State(state="*")`` — the wildcard. Matches any state, including "no
   state". Handlers registered with ``any_state`` are typically combined
   with another filter (e.g. a command) so they do not swallow regular
   messages:

   .. code-block:: python

      @dp.new_message(Command("cancel"), any_state)
      async def cmd_cancel(message, state: FSMContext):
          await state.clear()
          await message.answer("Cancelled.")

.. note::

   Handlers are checked in registration order and the **first** handler
   whose filters all pass wins (unless it raises
   :class:`~aiorubi.dispatcher.event.bases.SkipHandler`). Register
   ``any_state`` handlers *after* the more specific ones.


FSMContext
==========

`aiorubi.fsm.context.FSMContext(storage: BaseStorage, key: StorageKey)`

The per-update handle to the FSM. An instance is injected into every
handler as the ``state`` keyword argument (assuming FSM is enabled — see
`Disabling FSM`_). All methods are coroutines.

Setting and getting the state
-----------------------------

.. method:: set_state(state: StateType = None) -> None

   Store the new state. Accepts a :class:`~aiorubi.fsm.state.State` (usually
   ``Form.name``), a raw string, or ``None`` to reset to "no state".

   .. code-block:: python

      await state.set_state(Form.age)
      await state.set_state(None)   # back to default_state

.. method:: get_state() -> str | None

   Return the current state string, or ``None`` if no state is set.
   To test against a :class:`~aiorubi.fsm.state.State`, compare strings:

   .. code-block:: python

      if await state.get_state() == Form.age:
          ...

Reading and writing data
------------------------

The FSM data is a plain ``dict[str, Any]`` stored next to the state.

.. method:: set_data(data: Mapping[str, Any]) -> None

   **Replace** the whole data dict.

.. method:: get_data() -> dict[str, Any]

   Return a copy of the current data (never ``None`` — an empty dict when
   nothing was stored).

.. method:: update_data(data: Mapping[str, Any] | None = None, **kwargs) -> dict[str, Any]

   Merge the given keys into the stored data (like :meth:`dict.update`) and
   return the new data. Both spellings are equivalent:

   .. code-block:: python

      await state.update_data({"name": "Amir"})
      await state.update_data(name="Amir")

.. method:: get_value(key: str, default: Any | None = None) -> Any | None

   Read a single value without materialising the whole dict:

   .. code-block:: python

      name = await state.get_value("name")
      retries = await state.get_value("retries", default=0)

.. method:: clear() -> None

   Reset the FSM context: sets the state to ``None`` and replaces the data
   with an empty dict. Call this when a dialog finishes or is cancelled.

.. warning::

   Storage data must be JSON-serialisable for the
   :doc:`Redis <storages>` and :doc:`MongoDB <storages>`
   storages. Pass ``None``/``""`` instead of model objects, or store the
   ``model_dump()`` of your payload. The :class:`MemoryStorage` is more
   forgiving but raises :class:`~aiorubi.exceptions.DataNotDictLikeError`
   if you pass something that is not dict-like to ``set_data``.


Storage keys and strategies
===========================

StorageKey
----------

``aiorubi.fsm.storage.base.StorageKey``

   A frozen dataclass identifying one FSM "cell":

   .. code-block:: python

      @dataclass(frozen=True)
      class StorageKey:
          bot_id: str
          chat_id: str
          user_id: str
          destiny: str = "default"

   * ``bot_id`` — isolates data between bots sharing one storage.
   * ``chat_id`` / ``user_id`` — filled according to the FSM strategy.
   * ``destiny`` — a namespace that lets subsystems (scenes history, i18n
     context, your own features) keep independent state for the same user
     and chat. The default destiny is ``"default"``.

FSMStrategy
-----------

``aiorubi.fsm.strategy.FSMStrategy``

   Enum controlling how ``chat_id`` and ``user_id`` are derived for the
   :class:`~aiorubi.fsm.storage.base.StorageKey`. Pass it to the
   :class:`~aiorubi.dispatcher.dispatcher.Dispatcher` constructor as
   ``fsm_strategy=``.

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Strategy
        - Key is scoped to
      * - ``FSMStrategy.USER_IN_CHAT`` *(default)*
        - Each user **inside each chat**. The same user has independent
          state in every group and in private dialog. Best choice for
          per-user forms.
      * - ``FSMStrategy.CHAT``
        - Each **chat as a whole**. All users of a group share one state —
          useful for collective workflows (polls, shared checklists).
      * - ``FSMStrategy.GLOBAL_USER``
        - Each **user across all chats**. The user's state follows them
          from private chat into groups.

   .. code-block:: python

      from aiorubi import Dispatcher
      from aiorubi.fsm.strategy import FSMStrategy

      dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)

   .. note::

      If an update carries no user context (for example a
      ``removed_message``), the FSM middleware cannot build a key and simply
      proceeds without a ``state`` — handlers will not receive the ``state``
      argument for such updates.


Disabling FSM
=============

If your bot keeps all context in its own database and does not need the
built-in FSM at all, disable it:

.. code-block:: python

   dp = Dispatcher(disable_fsm=True)

When ``disable_fsm=True``:

* The :class:`~aiorubi.fsm.middleware.FSMContextMiddleware` is not
  installed, so no ``state`` / ``raw_state`` / ``fsm_storage`` keys are
  injected into handlers and no storage round-trips happen.
* Event isolation (which is part of the FSM pipeline) is disabled with it.
* ``StateFilter`` has nothing to match — avoid state-bound handlers.

Note that the storage and events-isolation arguments are still accepted
(and ``Dispatcher.storage`` still resolves), but they are simply unused by
the pipeline.


Default storage and swapping storages
=====================================

By default the :class:`~aiorubi.dispatcher.dispatcher.Dispatcher` uses
:class:`~aiorubi.fsm.storage.memory.MemoryStorage` — a plain in-process
dict. It is perfect for development and tests, but all FSM state is lost on
restart, so production bots should swap in a persistent storage:

.. code-block:: python

   from aiorubi import Bot, Dispatcher
   from aiorubi.fsm.storage.redis import RedisStorage

   storage = RedisStorage.from_url("redis://localhost:6379/0")
   dp = Dispatcher(storage=storage)

The full catalogue of bundled storages — Redis, MongoDB via motor, MongoDB
via pymongo, plus the storage interface for writing your own — is covered
in :doc:`storages`.

Because storages are keyed by :class:`~aiorubi.fsm.storage.base.StorageKey`,
swapping is transparent: no handler code changes, only the ``storage=``
argument to the dispatcher.


Event isolation
===============

Two updates from the same user can be processed concurrently (polling runs
handlers as tasks by default). To prevent two handlers from reading and
writing the same FSM cell at the same time, the FSM middleware wraps every
stateful dispatch in an isolation lock.

Configure it with ``events_isolation=``:

.. code-block:: python

   from aiorubi.fsm.storage.memory import SimpleEventIsolation

   dp = Dispatcher(events_isolation=SimpleEventIsolation())

Bundled implementations:

* :class:`~aiorubi.fsm.storage.memory.DisabledEventIsolation` *(default)* —
  no locking at all.
* :class:`~aiorubi.fsm.storage.memory.SimpleEventIsolation` — an
  :class:`asyncio.Lock` per storage key, held while the handler runs.
* :class:`~aiorubi.fsm.storage.redis.RedisEventIsolation` — a Redis lock
  (``timeout=60`` seconds by default) so isolation also works across
  multiple bot processes sharing one Redis. The convenient way to get it is
  ``storage.create_isolation()`` on a :class:`~aiorubi.fsm.storage.redis.RedisStorage`.

The state string is read **after** the lock is acquired, which guarantees
that ``await state.get_state()`` inside the handler always observes the
latest committed state.


Recipes
=======

Counting attempts
-----------------

.. code-block:: python

   @dp.new_message(Form.age)
   async def process_age(message, state: FSMContext):
       text = message.text or ""
       if not text.isdigit():
           attempts = await state.get_value("attempts", default=0) + 1
           await state.update_data(attempts=attempts)
           if attempts >= 3:
               await state.clear()
               return await message.answer("Too many attempts. Bye!")
           return await message.answer("Send a number, please.")

Passing context between handlers
--------------------------------

Store anything JSON-serialisable in the FSM data and read it in later
handlers with :meth:`~aiorubi.fsm.context.FSMContext.get_value` — this is
the idiomatic replacement for aiogram's ``RuntimeError``-prone global
variables.

See also
========

* :doc:`storages` — persistent FSM storages and the storage interface.
* :doc:`scenes` — a higher-level wizard built on top of the FSM.
* :doc:`filter` — matching updates by state with
  :class:`~aiorubi.filters.state.StateFilter`.
* :doc:`/migration-from-aiogram` — the FSM part of the aiogram port is
  API-identical; identifiers are ``str`` instead of ``int``.
