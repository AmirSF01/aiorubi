.. _tutorial-commands:

=====================
2. Commands & Filters
=====================

The greeting bot works, but it answers to *any* ``/start``-like text.
In this chapter we will register several commands properly and learn
how filters decide which handler runs.


Built-in command filter
=======================

:class:`~aiorubi.filters.command.Command` is the filter you will use
most often. It matches messages whose text starts with ``/`` followed
by one of the given commands:

.. code-block:: python

   from aiorubi.filters.command import Command

   @dp.new_message(Command("start"))
   async def cmd_start(message): ...

   # Several commands, one handler:
   @dp.new_message(Command("help", "about"))
   async def cmd_help(message): ...

By default the filter:

* matches only messages that begin with ``/`` (the prefix),
* requires an exact, case-sensitive command match (pass
  ``ignore_case=True`` to relax this),
* verifies the bot mention, if the command carries one (pass
  ``ignore_mention=True`` to ignore it).

``Command`` also accepts regular-expression patterns and
:class:`~aiorubi.types.bot_command.BotCommand` objects, and exposes
the parsed :class:`~aiorubi.filters.command.CommandObject` to the
handler as the ``command`` argument:

.. code-block:: python

   @dp.new_message(Command("note"))
   async def note(message, command: CommandObject):
       args = command.args   # e.g. "shopping" for "/note shopping"

.. note::

   Import ``CommandObject`` alongside ``Command``:
   ``from aiorubi.filters.command import Command, CommandObject``.


Falling back for unknown text
=============================

Filters are checked **in registration order**. When none of the
registered filters match, the update is marked as *unhandled*. Let's
add a catch-all handler as the *last* registration:

.. code-block:: python

   @dp.new_message()
   async def unknown(message):
       # Only reached when no earlier handler matched.
       await message.answer(
           "این دستور را نمی‌شناسم. /help را امتحان کن."
       )

.. note::

   Because handlers are checked in order, a catch-all handler with no
   filters must be registered **after** every other handler on the
   same observer. If you put it first, it will swallow everything.


Magic filter F
==============

Sometimes you need finer control than "which command". That is where
the **magic filter** — the :data:`~aiorubi.F` object — comes in:

.. code-block:: python

   from aiorubi import F

   # Match messages that contain the word "hello":
   @dp.new_message(F.text.contains("hello"))
   async def hello(message):
       await message.answer("Hello to you too! 👋")

   # Match only very long texts:
   @dp.new_message(F.text.len() > 100)
   async def long_text(message):
       await message.answer("وای، چقدر طولانی!")

``F`` mirrors the attribute access of the event object, so
``F.text`` means "the ``text`` attribute of the message". Any
comparison, ``.contains()``, ``.len()``, ``.startswith()`` … works.
The full magic-filter DSL is covered in
:doc:`/guide/filter`.

Combining filters
=================

Filters compose with ``&``, ``|`` and ``~``:

.. code-block:: python

   from aiorubi import F
   from aiorubi.filters import or_f
   from aiorubi.filters.command import Command

   # Command /note that also has some arguments after it.
   # NOTE: ``Command(...) & F.text...`` does NOT work (Command is not a
   # magic-filter); either pass both filters positionally — the observer
   # ANDs them — or use the ``and_f`` combinator:
   @dp.new_message(Command("note"), F.text.len() > 6)
   async def note_with_text(message):
       ...

   # equivalent with the combinator:
   # from aiorubi.filters import and_f
   # @dp.new_message(and_f(Command("note"), F.text.len() > 6))

   # /ping as a command, or any message whose text is exactly "ping".
   # NOTE: ``Command(...) | F.text == "ping"`` does NOT work either —
   # use the ``or_f`` combinator:
   # from aiorubi.filters import or_f
   @dp.new_message(or_f(Command("ping"), F.text == "ping"))
   async def ping(message):
       await message.answer("pong!")


Passing extra data to handlers
==============================

Handlers can accept keyword arguments beyond the event. The
dispatcher injects whatever it finds in ``workflow_data`` — the dict
you passed to ``Dispatcher(...)`` — plus a few built-ins like
``bot`` and ``state``:

.. code-block:: python

   dp = Dispatcher(my_setting="production")

   @dp.new_message(Command("env"))
   async def cmd_env(message, my_setting: str):
       await message.answer(f"Running in {my_setting}")

This mechanism — **dependency injection** — is the idiomatic way to
share a database connection, config or service between handlers.


Recap
=====

In this chapter we registered multiple commands, learned the
registration-order rule, met the magic filter ``F``, combined filters
with boolean operators, and discovered dependency injection.

In the next chapter we will dive deeper into the ``Message`` model
and all the media Rubika can deliver.
