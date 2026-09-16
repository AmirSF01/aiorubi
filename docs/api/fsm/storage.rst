=======
Storage
=======

.. toctree::
   :maxdepth: 2

Storages keep FSM state and data between updates.

Base
====

.. autoclass:: aiorubi.fsm.storage.base.BaseStorage
   :members:
   :special-members: __call__

.. autoclass:: aiorubi.fsm.storage.base.BaseEventIsolation
   :members:

.. autoclass:: aiorubi.fsm.storage.base.KeyBuilder
   :members:

.. autoclass:: aiorubi.fsm.storage.base.DefaultKeyBuilder
   :members:

.. autoclass:: aiorubi.fsm.storage.base.StorageKey
   :members:

Memory
======

.. autoclass:: aiorubi.fsm.storage.memory.MemoryStorage
   :members:
   :special-members: __init__

.. autoclass:: aiorubi.fsm.storage.memory.DisabledEventIsolation
   :members:

.. autoclass:: aiorubi.fsm.storage.memory.MemoryStorageRecord
   :members:

Redis
=====

.. autoclass:: aiorubi.fsm.storage.redis.RedisStorage
   :members:
   :special-members: __init__

Mongo
=====

.. autoclass:: aiorubi.fsm.storage.mongo.MongoStorage
   :members:
   :special-members: __init__

Pymongo
=======

.. autoclass:: aiorubi.fsm.storage.pymongo.PyMongoStorage
   :members:
   :special-members: __init__

.. note::

   ``RedisStorage`` requires the ``[redis]`` extra, ``MongoStorage``
   and ``PymongoStorage`` the ``[mongo]`` extra. autodoc therefore
   skips their members when those extras are not installed.
