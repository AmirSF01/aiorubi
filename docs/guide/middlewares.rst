===========
Middlewares
===========

Middlewares wrap the handler call — the classic onion model. Use them for
cross-cutting concerns: timing, database sessions, rate limiting, user
throttling, context injection.

.. code-block:: python

   class MyMiddleware(BaseMiddleware):
       async def __call__(self, handler, event, data):
           # before the handler runs
           result = await handler(event, data)
           # after the handler ran
           return result

Inner vs outer middlewares
==========================

Every observer has **two** middleware chains:

* ``observer.outer_middleware(...)`` — runs *before* filters are checked,
  on every single event of that observer. Use for context that filters
  themselves need (the built-in FSM middleware is outer for exactly this
  reason).
* ``observer.middleware(...)`` — runs only for events that already matched
  a handler, immediately around the handler call. Cheaper; use for
  per-handler work like opening a DB session.

.. code-block:: python

   router.new_message.outer_middleware(MyMiddleware())
   router.new_message.middleware(MyInnerMiddleware())

Decorator and function-form middlewares
---------------------------------------

Besides classes, both managers accept plain async callables:

.. code-block:: python

   @dp.new_message.outer_middleware
   async def timer(handler, event, data):
       started = time.monotonic()
       result = await handler(event, data)
       loggers.dispatcher.info("took %.1f ms", (time.monotonic() - started) * 1000)
       return result

BaseMiddleware
==============

`aiorubi.dispatcher.middlewares.base.BaseMiddleware`

The base class for class-based middlewares. Subclass it and override
``__call__(handler, event, data)``:

* ``handler`` — the next step of the chain; always ``await handler(event, data)``.
* ``event`` — the event object for the observer.
* ``data`` — the context dict that will be given to filters and handlers;
  mutate it to inject dependencies:

  .. code-block:: python

     class SessionMiddleware(BaseMiddleware):
         async def __call__(self, handler, event, data):
             async with session_maker() as session:
                 data["session"] = session
                 return await handler(event, data)

The ``data`` dict is exactly the context described in
:doc:`handlers` — middleware entries become handler keyword
arguments.

Skipping the rest of the chain
------------------------------

Raise :class:`~aiorubi.dispatcher.event.bases.CancelHandler` from a
middleware to stop processing this update entirely; a plain ``return``
without calling ``handler`` also cuts the chain short.

MiddlewareManager
=================

`aiorubi.dispatcher.middlewares.manager.MiddlewareManager`

Each observer carries two instances (``observer.middleware`` and
``observer.outer_middleware``). ``wrap_middlewares(managers, callback)``
builds the onion at dispatch time — you normally never touch it directly.

Built-in middlewares
====================

The dispatcher installs three outer middlewares on the ``update`` observer
(see :doc:`dispatcher`):

#. :class:`~aiorubi.dispatcher.middlewares.error.ErrorsMiddleware` —
   converts handler exceptions into ``error``-observer events.
#. :class:`~aiorubi.dispatcher.middlewares.user_context.UserContextMiddleware`
   — puts ``event_context`` (a frozen dataclass with ``chat_id`` and
   ``user_id``), plus the compatibility aliases ``event_from_user`` and
   ``event_chat``, into the data.
#. :class:`~aiorubi.fsm.middleware.FSMContextMiddleware` — FSM support;
   acquires the event-isolation lock and provides ``state`` / ``raw_state``
   / ``fsm_storage``.

Scenes add one more outer middleware (``ScenesManager`` injection) when a
:class:`~aiorubi.fsm.scene.SceneRegistry` is created — see
:doc:`scenes`.

Propagation order
=================

For a dispatch through routers ``dp → parent → child`` the observer's
middlewares are collected **root first**: ``dp``'s outer middlewares run
before ``parent``'s, which run before ``child``'s; the inner (per-handler)
chain then wraps the winning handler. Filters and handlers always see the
data as mutated by every middleware up to that point.

Practical recipe — throttling
-----------------------------

.. code-block:: python

   class ThrottlingMiddleware(BaseMiddleware):
       def __init__(self, rate: float = 0.5) -> None:
           self._rate = rate
           self._last: dict[str, float] = {}

       async def __call__(self, handler, event, data):
           user_id = data.get("event_from_user")
           if user_id is None:
               return await handler(event, data)
           now = time.monotonic()
           if now - self._last.get(user_id, 0) < self._rate:
               return None                     # swallow the update
           self._last[user_id] = now
           return await handler(event, data)

   dp.new_message.middleware(ThrottlingMiddleware())

Register it as *inner* middleware on a high-traffic observer so the check
only costs anything for events that would run a handler anyway; as *outer*
middleware it would also gate router-level filter checks.

See also
========

* :doc:`dispatcher` — the built-in middlewares and install order.
* :doc:`handlers` — how injected data reaches handlers.
* :doc:`fsm` — the FSM middleware in depth.
