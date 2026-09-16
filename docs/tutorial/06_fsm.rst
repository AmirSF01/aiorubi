.. _tutorial-fsm:

========================
6. Finite State Machine
========================

Our bot can talk, but it cannot *remember*. A note-taking bot needs
to know that "the next message the user sends is the note's body".
That is exactly what the **FSM** (Finite State Machine) is for.


Declaring states
================

States are declared as a :class:`~aiorubi.fsm.state.StatesGroup`:

.. code-block:: python

   from aiorubi.fsm.state import State, StatesGroup

   class NewNote(StatesGroup):
       title = State()   # -> "NewNote:title"
       body = State()    # -> "NewNote:body"

Each attribute becomes a :class:`~aiorubi.fsm.state.State` whose full
name is ``"Group:state"``. These objects are used as filters and as
values for ``state.set_state()``.


Reading and writing state
=========================

Every handler may accept a ``state`` keyword argument — the
:class:`~aiorubi.fsm.context.FSMContext` for this user+chat:

.. code-block:: python

   @dp.new_message(Command("new"))
   async def cmd_new(message, state):
       await state.set_state(NewNote.title)
       await message.answer("عنوان یادداشت رو بنویس:")


   @dp.new_message(NewNote.title)
   async def note_title(message, state):
       # Save the title in FSM data and advance:
       await state.update_data(title=message.text)
       await state.set_state(NewNote.body)
       await message.answer("حالا متن یادداشت رو بفرست:")


   @dp.new_message(NewNote.body)
   async def note_body(message, state):
       data = await state.get_data()
       title, body = data["title"], message.text

       # ... store the note in your database here ...

       await state.clear()   # state -> None, data -> {}
       await message.answer(f"✅ ذخیره شد:\n{title}")


The ``state`` filter
====================

Passing a ``State`` object as a filter means "run this handler only
when the user is in that state":

.. code-block:: python

   @dp.new_message(NewNote.title)
   async def note_title(message, state): ...

This is sugar for
``StateFilter(NewNote.title)``. Two special values exist:

* ``default_state`` (importable from ``aiorubi.fsm.state``) — the
  user is in *no* state;
* ``any_state`` — matches regardless of state.


Cancelling a flow
=================

A flow that cannot be cancelled traps the user. Add an escape hatch:

.. code-block:: python

   from aiorubi.fsm.state import any_state
   from aiorubi.filters.command import Command

   @dp.new_message(Command("cancel"), any_state)
   async def cmd_cancel(message, state):
       await state.clear()
       await message.answer("باشه، رد شدیم. /new برای شروع مجدد.")

.. note::

   Handlers fire **in registration order**, so the ``/cancel`` escape
   hatch must be registered **before** the state-bound handlers —
   otherwise a state handler (e.g. ``NewNote.title``) may consume the
   message first. A catch-all handler with no filters must always stay
   registered last.


FSM data — the per-user dict
============================

``state.update_data(**kw)`` merges into a per-user dictionary that
you can read back with ``await state.get_data()``:

.. code-block:: python

   await state.update_data(title="خرید", items=3)
   data = await state.get_data()          # {"title": "خرید", "items": 3}
   n = await state.get_value("items", 0)  # 3

The data travels with the storage — the default
:class:`~aiorubi.fsm.storage.memory.MemoryStorage` keeps it in RAM
(lost on restart). For production use
:class:`~aiorubi.fsm.storage.redis.RedisStorage` or
:class:`~aiorubi.fsm.storage.mongo.MongoStorage`, described in
:doc:`/guide/storages`.


FSM strategy
============

The dispatcher argument ``fsm_strategy`` decides *which* user a state
belongs to:

.. code-block:: python

   from aiorubi.fsm.strategy import FSMStrategy

   dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

The default ``USER_IN_CHAT`` gives every user their own state per
chat — the right choice for almost every bot.


Recap
=====

You can now declare state groups, gate handlers on the current state,
carry data between steps with ``update_data``/``get_data``, and
cancel flows safely. Next: organising a growing bot with routers.
