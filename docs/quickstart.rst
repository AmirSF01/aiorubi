==========
Quickstart
==========

This page walks you through installing ``aiorubi`` and running your
first bot in **under five minutes**. If you already know aiogram 3.x
you will feel right at home — but if not, that's fine too.


Prerequisites
-------------

* Python 3.10 or newer (``aiorubi`` supports 3.10, 3.11, 3.12, 3.13 and
  3.14).
* A Rubika bot token. To obtain it, open `@BotFather <https://rubika.ir/BotFather>`_
  in Rubika, send ``/newbot``, follow the prompts and copy the token.


Install
-------

.. code-block:: console

   $ pip install aiorubi

If you intend to use the :doc:`Redis <guide/fsm>`, MongoDB, or proxy
storages, install the matching extras:

.. code-block:: console

   $ pip install aiorubi[redis,mongo,proxy,fast]


Your first bot
--------------

Create a file called ``bot.py``:

.. code-block:: python

   import asyncio
   import logging

   from aiorubi import Bot, Dispatcher
   from aiorubi.filters.command import Command

   BOT_TOKEN = "PUT-YOUR-TOKEN-HERE"

   dp = Dispatcher()


   @dp.new_message(Command("start"))
   async def cmd_start(message):
       await message.reply(f"Hello, {message.sender_id}!")


   @dp.new_message()
   async def echo(message):
       # `message.text` is ``None`` for non-text updates, so guard it.
       if message.text is not None:
           await message.answer(message.text)


   async def main():
       logging.basicConfig(level=logging.INFO)
       bot = Bot(token=BOT_TOKEN)
       # Resolve bot info once so `bot.id` becomes available.
       await bot.me()
       await dp.start_polling(bot)


   if __name__ == "__main__":
       asyncio.run(main())

Run it:

.. code-block:: console

   $ python bot.py

Open your bot in Rubika and send ``/start``. You should get back the
"Hello, …!" reply. Send any other text and the bot will echo it back.

.. note::

   The echo handler deliberately checks ``message.text is not None``
   because Rubika can deliver image, file, location, contact, sticker
   and poll messages too — those updates do **not** have a ``text``
   attribute. See :doc:`guide/filter` for ways to filter by content
   type.


What just happened?
-------------------

Let's dissect the code, because every concept used above is reused
throughout the framework.

The :class:`~aiorubi.client.bot.Bot` object is a thin wrapper around
the Rubika Bot API. It owns the token, an :class:`aiohttp`-backed
session, and exposes one Python method per Rubika endpoint. Calling
``await bot.me()`` resolves and caches :class:`~aiorubi.types.bot_info.BotInfo`
so that helpers like ``bot.id`` are usable in logs.

The :class:`~aiorubi.dispatcher.dispatcher.Dispatcher` is the entry
point of the routing layer. It is a special :class:`Router <aiorubi.dispatcher.router.Router>`
that owns the FSM, the error middleware and the lifecycle
observers (``startup`` / ``shutdown``). In practice you almost never
register handlers directly on it — you create sub-routers and mount
them — but for a tiny bot it is perfectly fine.

A handler is just an ``async`` function. You attach it to an observer
with either the decorator syntax (``@dp.new_message()``) or the
explicit ``register`` syntax:

.. code-block:: python

   @dp.new_message(Command("start"))
   async def cmd_start(message): ...

is identical to

.. code-block:: python

   async def cmd_start(message): ...

   dp.new_message.register(cmd_start, Command("start"))

Filters are callables that decide whether an update should reach a
handler. :class:`~aiorubi.filters.command.Command` is one of the
built-ins: it accepts a list of commands (``Command("start", "help")``)
and configurable prefixes (default ``"/"``). The whole :doc:`guide/filter`
chapter explains them in detail.

``message.reply`` and ``message.answer`` are *shortcuts*. They return
a coroutine that, when awaited, calls the underlying :class:`Bot.send_message`
method. Behind the scenes ``reply`` sets ``reply_to_message_id`` to
the current message's id, while ``answer`` does not. A whole family
of these shortcuts exists — ``reply_image``, ``answer_poll``,
``reply_location``, etc.

Finally, ``await dp.start_polling(bot)`` begins the long-polling loop.
Under the hood the dispatcher calls ``bot.get_updates`` in a loop,
parses each update into an :class:`~aiorubi.types.update.Update`,
splits it into the appropriate observer (``new_message`` here) and
triggers every matching handler.


Where to go next
----------------

* :doc:`installation` — full installation matrix and extras.
* :doc:`migration-from-aiogram` — if you already know aiogram 3.x.
* :doc:`tutorial/index` — a six-chapter guided tour from
  ``/start`` to webhooks.
* :doc:`guide/index` — concept-by-concept reference.