============
FSM storages
============

The FSM (see :doc:`fsm`) delegates persistence to a *storage*. aiorubi
ships one for every common backend and a small interface for writing your
own. All storages implement the same contract, so switching is a one-line
change at the :class:`~aiorubi.dispatcher.dispatcher.Dispatcher`:

.. code-block:: python

   from aiorubi import Dispatcher
   from aiorubi.fsm.storage.memory import MemoryStorage

   dp = Dispatcher(storage=MemoryStorage())   # explicit; this is the default

At shutdown the dispatcher closes the storage for you (``dispatcher.fsm.close``
is registered as a shutdown callback), so connections are released when
``await dp.stop_polling()`` / the polling loop ends.

BaseStorage — the interface
===========================

``aiorubi.fsm.storage.base.BaseStorage``

Abstract base class for all storages. To implement a custom storage,
subclass it and override the abstract methods:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Method
     - Semantics
   * - ``set_state(key, state=None)``
     - Store state (``State``, ``str`` or ``None``).
   * - ``get_state(key) -> str | None``
     - Read the current state string.
   * - ``set_data(key, data)``
     - **Replace** the data dict. Must raise
       :class:`~aiorubi.exceptions.DataNotDictLikeError` for non-dict input.
   * - ``get_data(key) -> dict[str, Any]``
     - Read the data dict (empty dict when unset).
   * - ``get_value(storage_key, dict_key, default=None)``
     - Read one key of the data. A concrete implementation exists on
       ``BaseStorage`` itself (it calls ``get_data``); override for
       efficiency.
   * - ``update_data(key, data) -> dict``
     - Merge and return new data. Also implemented on the base class via
       get → merge → set; MongoDB storages override it with an atomic
       ``$set``.
   * - ``close()``
     - Release connections. Called on dispatcher shutdown.

Every method receives a :class:`~aiorubi.fsm.storage.base.StorageKey` —
the frozen dataclass ``(bot_id, chat_id, user_id, destiny)`` described in
:doc:`fsm`.

MemoryStorage
=============

``aiorubi.fsm.storage.memory.MemoryStorage``

The default storage. Keeps records in a
``defaultdict[StorageKey, MemoryStorageRecord]`` where each record holds
``state`` and ``data``; ``get_data`` returns defensive copies.

.. warning::

   Data lives in the process memory and is lost on restart. Do not use in
   production unless losing all dialogs is acceptable.

It requires no dependencies and is the right choice for tests and quick
prototypes. ``MemoryStorage`` also provides
:class:`~aiorubi.fsm.storage.memory.DisabledEventIsolation` and
:class:`~aiorubi.fsm.storage.memory.SimpleEventIsolation` (an
``asyncio.Lock`` per key) for :ref:`event isolation <event-isolation>`.

RedisStorage
============

`aiorubi.fsm.storage.redis.RedisStorage(redis, key_builder=None, state_ttl=None, data_ttl=None, json_loads=json.loads, json_dumps=json.dumps)`

Persists state and data as Redis keys built by the key builder (see
`Key builders`_): state under ``...:state``, data JSON-serialised under
``...:data``. Setting an empty dict *deletes* the data key; setting state
``None`` deletes the state key.

Install with the ``redis`` extra:

.. code-block:: console

   $ pip install "aiorubi[redis]"

Two construction styles:

.. code-block:: python

   from redis.asyncio import Redis

   # 1. explicit client
   storage = RedisStorage(redis=Redis(host="localhost", port=6379, db=0))

   # 2. from a connection URL (recommended)
   from aiorubi.fsm.storage.redis import RedisStorage

   storage = RedisStorage.from_url(
       "redis://:password@localhost:6379/0",
       connection_kwargs={"decode_responses": False},
   )

Optional arguments:

* ``state_ttl`` / ``data_ttl`` — expiry for the respective keys, anything
  accepted by redis-py as ``ex=`` (seconds or ``timedelta``). Without TTLs
  records live forever.
* ``json_loads`` / ``json_dumps`` — swap the JSON codec, e.g. for
  ``orjson``.
* ``key_builder`` — custom :class:`~aiorubi.fsm.storage.base.KeyBuilder`.

RedisEventIsolation
-------------------

`aiorubi.fsm.storage.redis.RedisEventIsolation(redis, key_builder=None, lock_kwargs=None)`

A Redis-based lock (default ``{"timeout": 60}``) so that event isolation
works across *multiple bot processes* sharing one Redis. The shorthand is
``RedisStorage.create_isolation()`` which reuses the storage's client and
key builder:

.. code-block:: python

   storage = RedisStorage.from_url("redis://localhost:6379/0")
   dp = Dispatcher(storage=storage, events_isolation=storage.create_isolation())

.. _event-isolation:

Event isolation
===============

Polling processes updates as concurrent tasks, so two messages from the
same user may race on one FSM cell. The ``events_isolation=`` argument of
the dispatcher wraps each stateful dispatch in a lock:

* :class:`~aiorubi.fsm.storage.memory.DisabledEventIsolation` — default, no
  locking.
* :class:`~aiorubi.fsm.storage.memory.SimpleEventIsolation` — in-process
  ``asyncio.Lock`` per key.
* :class:`~aiorubi.fsm.storage.redis.RedisEventIsolation` — cross-process
  Redis lock.

The current state string is read **after** the lock is acquired, so
handlers always observe a consistent ``raw_state``.

MongoStorage (motor) — deprecated
=================================

`aiorubi.fsm.storage.mongo.MongoStorage(client, key_builder=None, db_name="aiorubi_fsm", collection_name="states_and_data")`

.. warning::

   **Deprecated.** Use :class:`~aiorubi.fsm.storage.pymongo.PyMongoStorage`
   instead; this class will be removed in a future version.

Motor-based MongoDB storage. Install with the ``mongo`` extra:

.. code-block:: console

   $ pip install "aiorubi[mongo]"

State and data live in a single document per :class:`StorageKey`, with
``_id`` produced by the key builder:

.. code-block:: python

   from aiorubi.fsm.storage.mongo import MongoStorage

   storage = MongoStorage.from_url(
       "mongodb://user:password@localhost:27017",
       db_name="my_bot",
   )
   dp = Dispatcher(storage=storage)

``update_data`` is executed as an atomic ``$set`` on the ``data.*`` fields
rather than read-modify-write.

PymongoStorage
==============

`aiorubi.fsm.storage.pymongo.PyMongoStorage(client, key_builder=None, db_name="aiorubi_fsm", collection_name="states_and_data")`

The maintained MongoDB storage, built on pymongo's native
``AsyncMongoClient`` (same document layout and atomic ``update_data`` as
``MongoStorage``):

.. code-block:: python

   from aiorubi.fsm.storage.pymongo import PyMongoStorage

   storage = PyMongoStorage.from_url(
       "mongodb://user:password@localhost:27017",
       db_name="my_bot",
       collection_name="fsm",
   )
   dp = Dispatcher(storage=storage)

or construct it from an existing client:

.. code-block:: python

   from pymongo import AsyncMongoClient

   client = AsyncMongoClient("mongodb://localhost:27017")
   storage = PyMongoStorage(client=client, db_name="my_bot")

Key builders
============

A key builder converts a :class:`~aiorubi.fsm.storage.base.StorageKey`
into the string actually used inside the database. Both Redis and MongoDB
storages accept ``key_builder=``.

DefaultKeyBuilder
-----------------

`aiorubi.fsm.storage.base.DefaultKeyBuilder(prefix="fsm", separator=":", with_bot_id=False, with_destiny=False)`

Generates ``<prefix>:<bot_id?>:<chat_id>:<user_id>:<destiny?>:<part?>``:

.. code-block:: python

   from aiorubi.fsm.storage.base import DefaultKeyBuilder

   DefaultKeyBuilder().build(key, "state")
   # "fsm:<chat_id>:<user_id>:state"

   DefaultKeyBuilder(with_bot_id=True, with_destiny=True).build(key, "data")
   # "fsm:<bot_id>:<chat_id>:<user_id>:default:data"

Notes:

* ``with_bot_id=True`` is required when *several bots* share one database,
  otherwise their keys collide.
* ``with_destiny=True`` is required when you use non-default destinies
  (e.g. the scenes history writes to destiny ``"scenes_history"``);
  otherwise the builder raises :class:`ValueError` instead of silently
  mixing namespaces.
* ``separator`` may be any string; for MongoDB ``_id`` values a different
  separator can help readability.

Custom key builders
-------------------

Subclass :class:`~aiorubi.fsm.storage.base.KeyBuilder` and implement
``build(key, part)`` where ``part`` is ``"state"``, ``"data"``, ``"lock"``
or ``None``:

.. code-block:: python

   from aiorubi.fsm.storage.base import KeyBuilder, StorageKey

   class FlatKeyBuilder(KeyBuilder):
       """Single flat namespace, useful for key-scanning tooling."""

       def build(self, key: StorageKey, part: str | None = None) -> str:
           base = f"{key.chat_id}.{key.user_id}"
           if key.destiny != "default":
               base += f".{key.destiny}"
           return f"{base}.{part}" if part else base

   storage = RedisStorage.from_url(
       "redis://localhost:6379/0",
       key_builder=FlatKeyBuilder(),
   )

Writing your own storage
========================

Combine the interface and the key builder knowledge above:

.. code-block:: python

   from collections.abc import Mapping
   from typing import Any

   from aiorubi.fsm.state import State
   from aiorubi.fsm.storage.base import (
       BaseStorage,
       StateType,
       StorageKey,
   )

   class SQLiteStorage(BaseStorage):
       def __init__(self, path: str) -> None:
           import aiosqlite
           self._db = aiosqlite.connect(path)

       async def set_state(self, key: StorageKey, state: StateType = None) -> None:
           value = state.state if isinstance(state, State) else state
           ...  # upsert

       async def get_state(self, key: StorageKey) -> str | None:
           ...  # select

       async def set_data(self, key: StorageKey, data: Mapping[str, Any]) -> None:
           if not isinstance(data, dict):
               raise DataNotDictLikeError(type(data).__name__)
           ...  # replace

       async def get_data(self, key: StorageKey) -> dict[str, Any]:
           ...

       async def close(self) -> None:
           await self._db.close()

Register it with ``Dispatcher(storage=SQLiteStorage("bot.db"))`` — no other
code changes are needed.

See also
========

* :doc:`fsm` — how the storage is used by the FSM middleware.
* :doc:`scenes` — scenes keep their history in a separate *destiny*
  of the same storage.
