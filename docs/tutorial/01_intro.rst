.. _tutorial-intro:

==================
1. Introduction
==================

In this chapter you will create the skeleton of the bot we will build
throughout this tutorial: a **note-taking bot**. By the end of the
tutorial it will be able to store notes per user, list them, delete
them, and — along the way — you will have learned every major concept
of the framework.

Our running project layout is deliberately simple: one file per
chapter. Create a working directory::

   mkdir aiorubi-tutorial
   cd aiorubi-tutorial
   python -m venv venv && source venv/bin/activate
   pip install aiorubi

Getting a bot token
===================

1. Open `@BotFather <https://rubika.ir/BotFather>`_ in Rubika.
2. Send ``/newbot`` and follow the prompts.
3. Copy the token — it looks like ``XjF7aBc...`` (starts with a
   capital letter).
4. Store it in an environment variable so it does not end up in your
   git history::

      export RUBIKA_BOT_TOKEN="XjF7aBc..."

.. warning::

   Treat bot tokens like passwords. Anyone holding the token controls
   your bot. Never commit it, never paste it into screenshots.


The skeleton
============

Create ``bot.py``:

.. code-block:: python

   import asyncio
   import logging
   import os

   from aiorubi import Bot, Dispatcher
   from aiorubi.filters.command import Command

   dp = Dispatcher()


   @dp.new_message(Command("start"))
   async def cmd_start(message):
       """Entry point: greet the user."""
       await message.answer(
           "سلام! 👋\n"
           "من بات یادداشت هستم.\n"
           "/new — یادداشت جدید\n"
           "/list — لیست یادداشت‌ها"
       )


   async def main() -> None:
       logging.basicConfig(level=logging.INFO)

       bot = Bot(token=os.environ["RUBIKA_BOT_TOKEN"])
       await bot.me()  # load bot info so bot.id works

       try:
           await dp.start_polling(bot)
       finally:
           await bot.session.close()


   if __name__ == "__main__":
       asyncio.run(main())

Run it and send ``/start`` to your bot in Rubika — you should see the
greeting. Everything else in this tutorial will expand on this file.


What we just learned
====================

* :class:`~aiorubi.client.bot.Bot` wraps the token and the HTTP
  session. ``await bot.me()`` caches the bot's own info.
* :class:`~aiorubi.dispatcher.dispatcher.Dispatcher` is the root
  router. ``@dp.new_message(...)`` registers a handler for text
  updates.
* Handlers are plain ``async def`` functions. Their single positional
  argument is the *event* — here a :class:`~aiorubi.types.message.Message`.
* ``message.answer(text)`` is a shortcut that sends a message to the
  same chat without quoting.

In the next chapter we will add more commands and learn how filters
make handler registration precise.
