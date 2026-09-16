==========
Dispatcher
==========

The :class:`~aiorubi.dispatcher.dispatcher.Dispatcher` is the root router
of the bot. It owns the update pipeline: incoming
:class:`~aiorubi.types.update.Update` objects enter here, are split by
update type, flow through the middleware chain (errors → user context →
FSM) and reach the first matching handler.

Creating a dispatcher
=====================

.. code-block:: python

   from aiorubi import Dispatcher
   from aiorubi.fsm.strategy import FSMStrategy

   dp = Dispatcher(
       storage=None,                # FSM storage; MemoryStorage by default
       fsm_strategy=FSMStrategy.USER_IN_CHAT,
       events_isolation=None,       # DisabledEventIsolation by default
       disable_fsm=False,           # True to run without FSM at all
       name=None,                   # optional router name for debugging
   )

All extra keyword arguments are kept in ``dp.workflow_data`` and passed to
every handler as keyword arguments — a simple global context:

.. code-block:: python

   dp = Dispatcher(db=my_database)

   @dp.new_message(Command("stats"))
   async def stats(message, db):        # injected from workflow_data
       ...

   dp["db"] = other_database            # mutable at runtime
   dp.get("db")                         # dict-like access

The dispatcher is a :class:`~aiorubi.dispatcher.router.Router`, so all
observer registration methods and ``include_router`` work on it. Unlike a
plain router it **cannot** be included into another router — setting
``parent_router`` raises :class:`RuntimeError`.

Observers
=========

Rubika delivers a single raw update type; the dispatcher's built-in
``update`` observer (``dp.update``) splits it into the specialised
observers:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Observer
     - Event object
   * - ``dp.new_message``
     - :class:`~aiorubi.types.message.Message`
   * - ``dp.updated_message``
     - :class:`~aiorubi.types.message.Message` (with ``is_edited``)
   * - ``dp.removed_message``
     - :class:`~aiorubi.types.removed_message.RemovedMessage`
   * - ``dp.inline_message``
     - :class:`~aiorubi.types.inline_message.InlineMessage` (button clicks)
   * - ``dp.started_bot``
     - :class:`~aiorubi.types.started_bot.StartedBot`
   * - ``dp.stopped_bot``
     - :class:`~aiorubi.types.stopped_bot.StoppedBot`
   * - ``dp.error`` (alias ``dp.errors``)
     - :class:`~aiorubi.types.error_event.ErrorEvent`

Registration uses either the decorator or the explicit form — both are
equivalent:

.. code-block:: python

   @dp.new_message(Command("start"))
   async def cmd_start(message): ...

   dp.new_message.register(cmd_start, Command("start"))

Unknown update types (new Rubika API features) are warned about and
skipped. Because a handler never fires for them, keep your aiorubi version
up to date.

Polling
=======

.. method:: start_polling(*bots, limit=100, polling_interval=0.5, handle_as_tasks=True, backoff_config=DEFAULT_BACKOFF_CONFIG, handle_signals=True, close_bot_session=True, tasks_concurrency_limit=None)

Starts the long-polling loop for one or more bots:

.. code-block:: python

   async def main():
       bot = Bot(token=TOKEN)
       await bot.me()                 # resolve bot info once
       await dp.start_polling(bot)

Notable parameters:

* ``handle_as_tasks=True`` — process each update in its own
  :class:`asyncio.Task` (concurrent); ``False`` awaits updates serially.
* ``tasks_concurrency_limit`` — cap concurrent updates (a semaphore), only
  with ``handle_as_tasks=True``.
* ``backoff_config`` —
  :class:`~aiorubi.utils.backoff.BackoffConfig` for retry delays when the
  API is unreachable; polling never dies on network errors.
* ``handle_signals`` — SIGINT/SIGTERM stop the loop gracefully.

``await dp.stop_polling()`` stops the loop programmatically; it raises
:class:`RuntimeError` if polling is not running.

Lifecycle hooks
---------------

.. code-block:: python

   @dp.startup()
   async def on_startup():
       await db.connect()

   @dp.shutdown()
   async def on_shutdown():
       await db.close()      # FSM storage is closed automatically

``await dp.emit_startup()`` / ``await dp.emit_shutdown()`` propagate the
event through all included routers.

Webhooks
========

.. method:: feed_webhook_update(bot, update, _timeout=55, **kwargs)

Entry point for HTTP-delivered updates. Returns a
:class:`~aiorubi.methods.base.RubikaMethod` to answer synchronously, or
``None``. If the handler takes longer than ``_timeout`` (55 s; Rubika
allows 60), the handler moves to the background and any returned method is
sent later via a *silent call*.

.. code-block:: python

   response = await dp.feed_webhook_update(bot, update_dict)
   if response is not None:
       await bot(response)

Lower-level entry points:

* ``await dp.feed_update(bot, update)`` — a parsed
  :class:`~aiorubi.types.update.Update`.
* ``await dp.feed_raw_update(bot, update_dict)`` — a raw dict; validated
  for you.
* ``await dp.silent_call_request(bot, method)`` — fire a method ignoring
  API errors (used for delayed webhook answers).

See :doc:`webhook` for the aiohttp server wiring.

Built-in middlewares
====================

The dispatcher installs, in order, on the ``update`` observer:

#. :class:`~aiorubi.dispatcher.middlewares.error.ErrorsMiddleware` —
   catches handler exceptions and routes them to ``dp.error`` handlers.
#. :class:`~aiorubi.dispatcher.middlewares.user_context.UserContextMiddleware`
   — caches ``event_context`` / ``event_from_user`` / ``event_chat``.
#. :class:`~aiorubi.fsm.middleware.FSMContextMiddleware` — the FSM
   (skipped with ``disable_fsm=True``); adds ``state``, ``raw_state``,
   ``fsm_storage``.

``dp.storage`` is a read-only alias for ``dp.fsm.storage``; ``dp.fsm`` is
the middleware instance itself.

See also
========

* :doc:`router` — organising handlers across routers.
* :doc:`fsm` — the FSM configuration arguments in detail.
* :doc:`webhook` — webhook deployment.
