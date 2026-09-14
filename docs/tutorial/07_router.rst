.. _tutorial-router:

=========================
7. Splitting up: Routers
=========================

So far everything lives in one file. That works until your bot has
30 handlers — then you want modules. :class:`~aiorubi.dispatcher.router.Router`
splits a bot into independent, mountable pieces.


Creating a router
=================

A ``Router`` is created, filled with handlers, and then included
into the dispatcher:

.. code-block:: python

   # notes/__init__.py
   from aiorubi import Router
   from aiorubi.filters.command import Command
   from aiorubi.fsm.state import State, StatesGroup

   router = Router(name="notes")


   class NewNote(StatesGroup):
       title = State()
       body = State()


   @router.new_message(Command("new"))
   async def cmd_new(message, state):
       await state.set_state(NewNote.title)
       await message.answer("عنوان؟")


   @router.new_message(NewNote.title)
   async def note_title(message, state):
       ...


   # bot.py
   from aiorubi import Dispatcher
   from notes import router as notes_router

   dp = Dispatcher()
   dp.include_router(notes_router)

Handlers registered on the router behave exactly as if they were
registered on the dispatcher.


Multiple routers
================

Include as many as you like — order defines priority:

.. code-block:: python

   dp.include_routers(
       admin_router,   # checked first
       notes_router,   # checked second
       common_router,  # fallback handlers live here
   )

An update flows through the routers in order; the first handler whose
filters match wins, and propagation stops there.


Nesting
=======

Routers can contain routers:

.. code-block:: python

   user_router = Router(name="user")
   user_router.include_router(notes_router)
   user_router.include_router(settings_router)

   dp.include_router(user_router)

This lets big projects mirror their package structure in the bot
layout. Deeply nested routers are cheap — propagation just walks the
tree.


Naming routers
==============

``Router(name="notes")`` makes logs readable: when an update is
handled, the dispatcher logs which router it ended up in. For
debugging unfamiliar codebases, name your routers.


Startup and shutdown hooks
==========================

Every router has its own ``startup`` and ``shutdown`` observers,
fired recursively by the dispatcher:

.. code-block:: python

   @notes_router.startup()
   async def on_startup():
       print("notes module ready")


   @notes_router.shutdown()
   async def on_shutdown():
       print("notes module going to sleep")

Use them to open and close database connections owned by the module.


Recap
=====

You can now split a bot into ``Router`` modules, mount them in
priority order, nest them, and give each module its own lifecycle
hooks. Next: intercepting every update with middlewares.
