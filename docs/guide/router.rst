======
Router
======

A :class:`~aiorubi.dispatcher.router.Router` groups handlers so a bot can
be split into reusable modules — an admin module, a games module, a
payments module — each mounted into the main dispatcher.

Creating and registering handlers
=================================

.. code-block:: python

   from aiorubi import Router
   from aiorubi.filters.command import Command

   router = Router(name="games")

   @router.new_message(Command("play"))
   async def cmd_play(message):
       await message.answer("Let's play!")

   # explicit form, identical result
   async def cmd_stop(message): ...
   router.new_message.register(cmd_stop, Command("stop"))

Observers are the same as on the dispatcher: ``new_message``,
``updated_message``, ``removed_message``, ``inline_message``,
``started_bot``, ``stopped_bot`` and ``error`` / ``errors``, plus the
lifecycle observers ``startup`` / ``shutdown``. All of them support the
decorator and ``register`` forms and accept any :doc:`filters
<filter>`.

Including routers
=================

Routers form a tree. The dispatcher is always the root; child routers are
visited after the parent's own handlers:

.. code-block:: python

   from aiorubi import Dispatcher, Router

   admin = Router(name="admin")
   games = Router(name="games")
   common = Router(name="common")

   dp = Dispatcher()
   dp.include_routers(admin, games, common)   # order matters
   # shorthand for:
   #   dp.include_router(admin)
   #   dp.include_router(games)
   #   dp.include_router(common)

``include_router`` attaches the child (setting its read-only
``parent_router``), and nesting works to any depth:

.. code-block:: python

   games.include_router(chess)     # dp → games → chess

Both methods return the router, so chaining is possible. A
:class:`RuntimeError` is raised when you try to include the dispatcher
itself into anything.

Propagation order
=================

When an update arrives it flows depth-first through the tree in
registration order:

#. outer middlewares of the matching observer, from root to leaf;
#. the root router's handlers (top to bottom);
#. each included router's handlers in inclusion order, recursing into
   their sub-routers.

The **first handler whose filters all pass** wins; the remaining routers
never see the update unless the handler raises
:class:`~aiorubi.dispatcher.event.bases.SkipHandler`. Register the most
specific routers first.

Router-level filters
====================

``observer.filter(...)`` attaches filters to *every* handler of that
observer, checked before the handler's own filters — ideal for guards:

.. code-block:: python

   from aiorubi.filters import StateFilter

   admin.new_message.filter(is_admin)          # async function filter
   admin.inline_message.filter(StateFilter(None, "*"))

Router-level filters apply to all handlers registered on that observer of
that router *and are not inherited* by included sub-routers (their
observers are separate objects).

Observer name
-------------

Every observer has an ``event_name`` attribute; the ``resolve_used_update_types()``
method walks the whole tree and returns the event names that actually have
handlers — polling and webhook helpers can use it to fetch only relevant
update types.

Lifecycle
=========

.. code-block:: python

   @router.startup()
   async def on_startup(): ...

   @router.shutdown()
   async def on_shutdown(): ...

Events emitted on the dispatcher (``dp.emit_startup()`` /
``dp.emit_shutdown()``) propagate through the whole tree, so each module
manages its own resources.

Chain helpers
-------------

* ``router.chain_head`` — iterate from the root down to *this* router.
* ``router.chain_tail`` — iterate from *this* router down to the last
  sub-router.

These generators power the middleware resolution and the propagation walk;
you rarely need them directly, but they are handy for debugging the router
tree.

Typical project layout
======================

.. code-block:: text

   mybot/
   ├── __main__.py        # creates Bot + Dispatcher, includes routers
   ├── admin/
   │   ├── __init__.py
   │   └── router.py      # admin = Router(name="admin"); handlers...
   ├── games/
   │   ├── __init__.py
   │   ├── router.py
   │   └── chess.py       # chess = Router(name="chess")
   └── common/
       └── router.py

.. code-block:: python

   # __main__.py
   from aiorubi import Bot, Dispatcher
   from mybot.admin.router import router as admin_router
   from mybot.games.router import router as games_router
   from mybot.common.router import router as common_router

   dp = Dispatcher()
   dp.include_routers(admin_router, games_router, common_router)

Each module owns its filters, middlewares and lifecycle hooks — the entry
point only wires them together.

See also
========

* :doc:`dispatcher` — the root router and its extra abilities.
* :doc:`middlewares` — middleware scoping per router/observer.
* :doc:`handlers` — writing the handlers themselves.
