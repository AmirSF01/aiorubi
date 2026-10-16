.. _tutorial-middlewares:

=========================================
8. Middlewares & global error handling
=========================================

Middlewares run **around** every handler on an observer. Use them for
cross-cutting concerns: timing, authentication, throttling, database
sessions, error reporting.


Your first middleware
=====================

A middleware is any callable with the signature
``(handler, event, data) -> result``:

.. code-block:: python

   import logging
   import time

   logger = logging.getLogger("timing")


   class TimingMiddleware:
       async def __call__(self, handler, event, data):
           start = time.monotonic()
           result = await handler(event, data)   # run the handler
           took = (time.monotonic() - start) * 1000
           logger.info("handled in %.1f ms", took)
           return result

Register it on an observer:

.. code-block:: python

   dp.new_message.outer_middleware(TimingMiddleware())

From now on every ``new_message`` update is timed.


Outer vs inner
==============

* **outer middleware** runs *before filters* — for every incoming
  update, handled or not. Use it for things that must always happen
  (loading a user from DB, throttling).
* **inner middleware** runs *after filters matched*, immediately
  around the handler itself. Use it for handler-scoped concerns
  (opening a DB session per handler).

.. code-block:: python

   dp.new_message.outer_middleware(LoadUserMiddleware())
   dp.new_message.middleware(DbSessionMiddleware())

The same two registration methods exist on every router observer.


Injecting data
==============

Middlewares communicate with handlers through ``data`` — the same
dict that powers dependency injection. Anything a middleware puts
into ``data`` can be declared as a handler argument:

.. code-block:: python

   class LoadUserMiddleware:
       async def __call__(self, handler, event, data):
           data["user"] = await db.get_user(event.sender_id)
           return await handler(event, data)


   @dp.new_message(Command("profile"))
   async def profile(message, user):
       await message.answer(f"سلام {user.name}!")


Error handling
==============

aiorubi already wraps every update in a built-in error middleware.
To *react* to errors, register a handler on the ``errors`` observer:

.. code-block:: python

   from aiorubi.types import ErrorEvent

   @dp.errors()
   async def on_error(event: ErrorEvent):
       logger.exception("Update crashed", exc_info=event.exception)
       if event.update is not None:
           await bot.send_message(
               event.update.chat_id,
               "یه خطا پیش اومد 😔 دوباره تلاش کن.",
           )

``event.exception`` is the raised exception; ``event.update`` is the
update being processed (may be ``None``).


Throttling example
==================

A complete, practical middleware — one message per second per user:

.. code-block:: python

   import time
   from collections import defaultdict


   class ThrottleMiddleware:
       def __init__(self, rate: float = 1.0):
           self.rate = rate
           self.last = defaultdict(float)

       async def __call__(self, handler, event, data):
           now = time.monotonic()
           if now - self.last[event.sender_id] < self.rate:
               return  # silently drop
           self.last[event.sender_id] = now
           return await handler(event, data)


   dp.new_message.outer_middleware(ThrottleMiddleware(rate=1.0))


Recap
=====

You can write middlewares, choose between outer and inner, inject
per-request data into handlers, and handle errors globally. Final
chapter: deploying behind a webhook.
