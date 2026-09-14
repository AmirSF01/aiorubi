======
Scenes
======

Scenes are a higher-level abstraction over the FSM (see :doc:`fsm`)
for complex multi-step dialogs. A **scene** is a named state with its own
handlers, and a **wizard** moves the user between scenes. Where plain FSM
gives you *states*, scenes give you *rooms*: each room decides which
messages it listens to and where to go next.

The scene machinery lives in :mod:`aiorubi.fsm.scene` and is a direct port
of the aiogram 3.x scenes API — ``Scene``, ``SceneWizard``, ``ScenesManager``
and the ``on`` marker.

The four moving parts
=====================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Role
   * - :class:`~aiorubi.fsm.scene.Scene`
     - Base class; you subclass it. Collects handlers and actions declared
       on the class into ``__scene_config__``.
   * - :class:`~aiorubi.fsm.scene.SceneWizard`
     - Injected into every scene instance as ``self.wizard``; performs
       transitions (``goto``, ``leave``, ``exit``, ``back``, ``retake``)
       and data access.
   * - :class:`~aiorubi.fsm.scene.ScenesManager`
     - Created per update by the scenes middleware; enters/exits scenes and
       exposes ``manager.history``.
   * - :class:`~aiorubi.fsm.scene.SceneRegistry`
     - Maps state strings to scene classes and mounts the middleware on a
       router/dispatcher.

Declaring a scene
=================

.. code-block:: python

   from aiorubi.fsm.scene import Scene, on

   class Dialog(Scene, state="dialog"):
       @on.new_message(F.text == "/help")
       async def show_help(self, message):
           await message.reply("Inside a dialog scene...")

Key points:

* ``state=`` assigns the FSM state string for the whole scene
  (``"dialog"`` here). It is stored via the ordinary FSM pipeline, so all
  :doc:`storages <storages>` work unchanged.
* ``@on.new_message(...)`` marks a handler inside the scene — it is
  registered only while the scene's state is active. Available markers:
  ``on.new_message``, ``on.updated_message``, ``on.removed_message``,
  ``on.inline_message``. Every marker accepts the same filters as the
  regular observers (``Command``, ``F``, custom filters — see
  :doc:`filter`).
* Handlers are plain methods: ``self`` is the scene instance, and the
  dispatcher-injected arguments (``message``, ``state``, …) follow the
  usual rules.

The ``after=`` argument schedules a transition that runs *after* the
handler returns: ``after=After.exit()``, ``after=After.back()`` or
``after=After.goto(OtherScene)``.

Scene configuration
-------------------

Class keyword arguments (also inherited from parent scene classes):

* ``state: str | None`` — the FSM state of the scene.
* ``reset_data_on_enter: bool | None`` — wipe the FSM data when the scene
  is entered.
* ``reset_history_on_enter: bool | None`` — clear the scene history when
  the scene is entered.
* ``inline_message_without_state: bool | None`` — allow inline-message
  handlers to fire even when the state no longer matches.

.. code-block:: python

   class Wizard(Scene, state="wizard", reset_data_on_enter=True,
                reset_history_on_enter=True):
       ...

SceneWizard
===========

Transitions (all coroutines):

* ``await wizard.enter(**kwargs)`` — (re)enter the current scene: applies
  the ``reset_*_on_enter`` flags, sets the scene state and fires the
  ``enter`` action.
* ``await wizard.leave(**kwargs)`` — snapshot the current state+data into
  the history and fire the ``leave`` action.
* ``await wizard.goto(scene, **kwargs)`` — ``leave()`` the current scene,
  then enter ``scene`` (a ``Scene`` subclass, a ``State`` or a state
  string).
* ``await wizard.exit(**kwargs)`` — clear the history, fire the ``exit``
  action, then reset the FSM state to ``None`` (leave the scene world).
* ``await wizard.back(**kwargs)`` — leave the current scene *without*
  snapshotting and roll the history back to the previous record, re-entering
  that scene with its saved state and data.
* ``await wizard.retake(**kwargs)`` — re-enter the current scene (re-runs
  its ``enter`` action).

Data shortcuts (they operate on the scene's FSM context):

``wizard.get_data()``, ``wizard.set_data(mapping)``,
``wizard.update_data(mapping=None, **kwargs)``,
``wizard.get_value(key, default=None)``, ``wizard.clear_data()``.

Actions
-------

Handlers can also be *actions* — they run on transitions instead of
updates. Declare them with the same marker objects:

.. code-block:: python

   class Game(Scene, state="game"):
       @on.new_message.enter()
       async def on_enter(self, message):
           await message.answer("Welcome to the game!")

       @on.new_message.leave()
       async def on_leave(self, message):
           await message.answer("Leaving the game")

       @on.new_message.exit()
       async def on_exit(self, message):
           await message.answer("Game session closed")

       @on.new_message.back()
       async def on_back(self, message):
           await message.answer("Going back")

``on.new_message.enter(SomeOtherScene)`` additionally jumps to the target
scene after the handler runs. Plain handlers can be chained with
transitions too: ``@on.new_message(F.text == "next").enter(NextScene)``,
``.leave()``, ``.exit()``, ``.back()``.

ScenesManager and entering scenes
=================================

The :class:`~aiorubi.fsm.scene.ScenesManager` is injected into handlers as
the ``scenes`` argument once a registry is installed. Its methods:

* ``await scenes.enter(scene, **kwargs)`` — if another scene is active it
  is *exited* first, then the requested scene is entered. ``scene`` may be
  ``None`` to reset to the default (no-scene) state.
* ``await scenes.close(**kwargs)`` — exit the active scene, if any.

Two ways to start a scene:

1. **Registry** — register all scenes up-front:

   .. code-block:: python

      from aiorubi.fsm.scene import SceneRegistry

      dp = Dispatcher(storage=storage)
      registry = SceneRegistry(dp)          # installs the middleware
      registry.add(Dialog, Game)            # each scene becomes a Router

2. **Entry handler** — turn a scene into a handler with
   ``Scene.as_handler()`` and attach it to a command:

   .. code-block:: python

      class Dialog(Scene, state="dialog"):
          ...

      @dp.new_message(Command("dialog"))
      async def start_dialog(message, scenes: ScenesManager):
          await scenes.enter(Dialog)

   or the one-liner equivalent:

   .. code-block:: python

      dp.new_message.register(Dialog.as_handler(), Command("dialog"))

HistoryManager
==============

Every :class:`~aiorubi.fsm.scene.ScenesManager` owns a
:class:`~aiorubi.fsm.scene.HistoryManager` (``manager.history``) that
remembers the last 10 scene snapshots — each a
``MemoryStorageRecord(state=..., data=...)``. Snapshots are stored in the
FSM storage under the ``scenes_history`` destiny, so they survive restarts
with persistent storages.

* ``await manager.history.snapshot()`` — push the *current* state and data
  (done automatically by ``wizard.leave()``).
* ``await manager.history.rollback() -> str | None`` — pop the latest
  snapshot and restore it (used by ``wizard.back()``).
* ``await manager.history.get()`` / ``.all()`` — peek at the last / all
  records without removing them.
* ``await manager.history.clear()`` — forget the history (used by
  ``wizard.exit()`` and ``reset_history_on_enter``).

Mounting scenes: as_router and as_handler
=========================================

``Scene.as_router(name=None)`` returns a :class:`~aiorubi.dispatcher.router.Router`
with the scene's handlers bound to its state via
:class:`~aiorubi.filters.state.StateFilter`. Include it manually when you
prefer explicit wiring:

.. code-block:: python

   dp.include_router(Dialog.as_router())
   dp.include_router(Game.as_router(name="game-scene"))

``Scene.as_handler(**kwargs)`` returns an async entry-point handler that
enters the scene (see above). ``SceneRegistry.add(..., router=...)`` /
``registry.register(...)`` combine registration with router inclusion; a
``SceneException`` is raised if two scenes share one state string.

Full example — a multi-step form
================================

.. code-block:: python
   :caption: form_bot.py

   import asyncio
   import logging

   from aiorubi import Bot, Dispatcher, F
   from aiorubi.filters.command import Command
   from aiorubi.fsm.context import FSMContext
   from aiorubi.fsm.scene import Scene, SceneRegistry, ScenesManager, on

   class Form(Scene, state="form", reset_data_on_enter=True):
       """Step 1 — collect the name."""

       @on.new_message.enter()
       async def ask_name(self, message):
           await message.answer("Welcome! What is your name? (/cancel to quit)")

       @on.new_message.exit()
       async def on_exit(self, message):
           await message.answer("Form cancelled.")

       @on.new_message(F.text == "/cancel")
       async def cancelled(self, message):
           await self.wizard.exit()

       @on.new_message(F.text)   # any text message inside this scene
       async def read_name(self, message, state: FSMContext):
           name = (message.text or "").strip()
           if len(name) < 2:
               return await message.answer("Too short. Try again:")
           await state.update_data(name=name)
           await self.wizard.goto(FormAge)

   class FormAge(Scene, state="form_age"):
       """Step 2 — collect the age."""

       @on.new_message.enter()
       async def ask_age(self, message):
           await message.answer("How old are you? (/back to fix your name)")

       @on.new_message(F.text == "/back")
       async def go_back(self, message):
           await self.wizard.back()             # returns to Form with data intact

       @on.new_message(F.text)
       async def read_age(self, message, state: FSMContext):
           if not (message.text or "").isdigit():
               return await message.answer("Send a number, please:")
           data = await state.update_data(age=int(message.text))
           await message.answer(f"Thanks, {data['name']}! You are {data['age']}.")
           await self.wizard.exit()

   async def main():
       logging.basicConfig(level=logging.INFO)

       bot = Bot(token="YOUR_RUBIKA_BOT_TOKEN")
       await bot.me()

       dp = Dispatcher()
       registry = SceneRegistry(dp)
       registry.add(Form, FormAge)

       @dp.new_message(Command("form"))
       async def start_form(message, scenes: ScenesManager):
           await scenes.enter(Form)

       await dp.start_polling(bot)

   if __name__ == "__main__":
       asyncio.run(main())

What happens, step by step:

#. ``/form`` — the entry handler calls ``scenes.enter(Form)``. The scene's
   ``enter`` action greets the user and the FSM state becomes ``"form"``.
#. The user's next message is matched by the ``F.text`` handler of the
   active scene (``Form``); ``goto(FormAge)`` snapshots ``Form`` into the
   history and enters the age scene, whose ``enter`` action (if any) fires.
#. ``/back`` in the age scene calls ``wizard.back()``: the age scene is
   left *without* snapshotting, the last history record (``Form`` with its
   data) is rolled back and ``Form`` is re-entered.
#. ``/cancel`` or finishing the last step calls ``wizard.exit()``: the
   history is cleared, the ``exit`` action says goodbye, and the FSM state
   is reset to ``None`` — the user is back in the "no scene" world.

Error handling
==============

Scene errors raise :class:`~aiorubi.exceptions.SceneException` (a subclass
of :class:`~aiorubi.exceptions.AiorubiError`), for example:

* a scene state is not registered (``Scene ... is not registered``);
* a duplicate state is registered in one registry;
* a scene handler runs without the FSM pipeline
  (``Scene context key 'state' is not available...``) — this happens when
  ``disable_fsm=True``.

Handle them in an :doc:`error handler <handlers>`:

.. code-block:: python

   from aiorubi.exceptions import SceneException

   @dp.error(ExceptionTypeFilter(SceneException))
   async def scene_error(event: ErrorEvent):
       logging.exception("Scene failure", exc_info=event.exception)

See also
========

* :doc:`fsm` — states, contexts and storages underneath.
* :doc:`storages` — where scene snapshots live (``scenes_history``
  destiny).
* :doc:`filter` — the filters accepted by ``@on.*`` decorators.
