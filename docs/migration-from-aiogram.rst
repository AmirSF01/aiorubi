==========================
Migration from aiogram 3.x
==========================

``aiorubi`` is a port of `aiogram <https://docs.aiogram.dev/>`_ 3.x to the
**Rubika Bot API**. The architecture, the names, the file layout and
the *ergonomics* are intentionally almost identical so that aiogram
users feel at home, and so that the rich aiogram learning material
remains 90 % applicable.

This page is a **field guide** for the 10 % that isn't.

If you have never used aiogram before, you can safely skip this
chapter and jump straight to :doc:`tutorial/index`.


What stays the same
-------------------

* **Module layout**: ``aiorubi.client``, ``aiorubi.dispatcher``,
  ``aiorubi.fsm``, ``aiorubi.filters``, ``aiorubi.handlers``,
  ``aiorubi.methods``, ``aiorubi.types``, ``aiorubi.webhook``, ….
* **Routers and Dispatchers**: same ``@dp.<event>()`` decorator
  pattern, same ``include_router`` mechanism.
* **FSM**: ``State``, ``StatesGroup``, ``FSMContext``,
  ``MemoryStorage`` / ``RedisStorage`` / ``MongoStorage`` —
  identical API.
* **Scenes**: ``Scene``, ``SceneWizard``, ``ScenesManager`` — identical
  API.
* **Filters**: ``Command``, ``CommandStart``, ``StateFilter``,
  ``MagicData``, ``ExceptionTypeFilter``, ``F`` and friends. (A
  ``CallbackData`` factory is not shipped yet — see
  :doc:`guide/filter` for the available toolkit.)
* **Middlewares**: outer/inner semantics, ``BaseMiddleware``,
  ``MiddlewareManager``.
* **Flags**: ``flags`` generator and decorator usage.
* **Shortcuts**: ``message.reply`` / ``message.answer`` /
  ``message.reply_image`` / etc.


What is *different* — at a glance
---------------------------------

* **Identifiers are strings, not integers.**
  Rubika issues string ids, so ``chat_id``, ``message_id``, ``user_id``
  and ``bot_id`` are all :class:`str` in aiorubi.

  .. code-block:: python

      # aiogram
      chat_id: int
      message_id: int

      # aiorubi
      chat_id: str
      message_id: str

* **The update model is unified.**
  Rubika does not give you a different class for every kind of
  message. There is one :class:`~aiorubi.types.message.Message`
  class; attached media appears as the ``file`` attribute (a
  :class:`~aiorubi.types.file.File` whose ``file_type`` distinguishes
  image, video, voice, music, gif and generic file). Other attached
  content types have their own attribute (``poll``, ``location``,
  ``contact_message``, ``sticker``).

  .. list-table::
     :header-rows: 1

     * - aiogram
       - aiorubi
     * - ``Message.photo``
       - ``Message.file`` (when ``file.file_type == FileType.IMAGE``)
     * - ``Message.video``
       - ``Message.file`` (when ``file.file_type == FileType.VIDEO``)
     * - ``Message.voice``
       - ``Message.file`` (when ``file.file_type == FileType.VOICE``)
     * - ``Message.audio``
       - ``Message.file`` (when ``file.file_type == FileType.MUSIC``)
     * - ``Message.animation``
       - ``Message.file`` (when ``file.file_type == FileType.GIF``)
     * - ``Message.sticker``
       - ``Message.sticker``
     * - ``Message.poll``
       - ``Message.poll``
     * - ``Message.location``
       - ``Message.location``
     * - ``Message.contact``
       - ``Message.contact_message``

* **The event names are renamed.**

  .. list-table::
     :header-rows: 1

     * - aiogram
       - aiorubi
     * - ``message``
       - ``new_message``
     * - ``edited_message``
       - ``updated_message``
     * - ``callback_query``
       - ``inline_message``
     * - ``my_chat_member`` / ``chat_member``
       - ``started_bot`` / ``stopped_bot``

* **There is one ``Keypad`` type, not two.**
  Rubika keypads come in two *display modes* — *inline* (under a
  message) and *chat* (at the bottom of the chat). Both are
  :class:`~aiorubi.types.keypad.Keypad` instances; the distinction is
  made at the call site via the ``inline_keypad=`` / ``chat_keypad=``
  keyword arguments.

  .. code-block:: python

      # aiogram
      await message.answer("Pick:", reply_markup=inline_kb)
      await message.answer("Pick:", reply_markup=reply_kb)

      # aiorubi
      await message.answer("Pick:", inline_keypad=inline_kb)
      await message.answer("Pick:", chat_keypad=reply_kb)

  To **remove** a chat keypad, call
  :meth:`Bot.remove_chat_keypad <aiorubi.client.bot.Bot.remove_chat_keypad>` —
  there is no ``ReplyKeyboardRemove`` class.

* **Buttons are a small hierarchy.** Seven button kinds are first-class
  types: ``Button``, ``ButtonSelection``, ``ButtonCalendar``,
  ``ButtonNumberPicker``, ``ButtonStringPicker``, ``ButtonTextbox``,
  ``ButtonLocation``. Mixing them in a single keypad is allowed.
  ``button_text`` is a required string (use an empty string for a
  textless button — there is no separate icon-only button kind).

* **HTML/Markdown text decorations are not yet supported.**
  Plain text only. The ``html`` and ``md`` helpers exposed in
  ``aiorubi/__init__.py`` are commented out; do not rely on them.

* **There is no ``ChatAction`` typing/uploading status.**
  Rubika does not expose the equivalent of "typing…" status updates,
  so aiorubi ships no helper for it.

* **Inline mode, payments, games, Passport, stickers API.**
  These are Telegram-specific and are not available on Rubika. The
  equivalent surface (``inline_message`` for button clicks, plain
  ``Message`` with ``poll`` for polls) is supported.

* **Webhook timeout.**
  Rubika gives you 60 seconds to respond to a webhook. The default
  ``_timeout`` value in
  :meth:`Dispatcher.feed_webhook_update <aiorubi.dispatcher.dispatcher.Dispatcher.feed_webhook_update>`
  is 55 seconds, with a fallback that moves slow handlers into the
  background and returns immediately.


Side-by-side example
--------------------

The same "echo + /start" bot in both frameworks:

.. tab-set::

   .. tab-item:: aiogram

      .. code-block:: python

         from aiogram import Bot, Dispatcher
         from aiogram.filters import Command

         dp = Dispatcher()

         @dp.message(Command("start"))
         async def start(message):
             await message.reply(f"Hello, {message.from_user.id}!")

         @dp.message()
         async def echo(message):
             if message.text:
                 await message.answer(message.text)

         async def main():
             bot = Bot("TELEGRAM_TOKEN")
             await dp.start_polling(bot)

   .. tab-item:: aiorubi

      .. code-block:: python

         from aiorubi import Bot, Dispatcher
         from aiorubi.filters.command import Command

         dp = Dispatcher()

         @dp.new_message(Command("start"))
         async def start(message):
             await message.reply(f"Hello, {message.sender_id}!")

         @dp.new_message()
         async def echo(message):
             if message.text is not None:
                 await message.answer(message.text)

         async def main():
             bot = Bot(token="RUBIKA_BOT_TOKEN")
             await bot.me()
             await dp.start_polling(bot)

The differences are:

1. The Bot constructor takes ``token=`` (keyword) — Rubika tokens
   are sensitive to leading whitespace so the explicit kwarg avoids
   bugs.
2. Observers are renamed: ``message`` → ``new_message``.
3. ``message.from_user.id`` → ``message.sender_id``.
4. ``await bot.me()`` must be called once before the bot info becomes
   available via shortcuts like ``bot.id``.
5. No ``asyncio.run(main())`` shown — same as aiogram.


Renaming cheat-sheet
--------------------

When porting a real codebase, the tedious work is renaming. Here is a
quick reference for ``sed`` / IDE find-and-replace:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - aiogram
     - aiorubi
   * - ``from aiogram import …``
     - ``from aiorubi import …``
   * - ``from aiogram.filters import …``
     - ``from aiorubi.filters import …``
   * - ``from aiogram.fsm import …``
     - ``from aiorubi.fsm import …``
   * - ``from aiogram.types import …``
     - ``from aiorubi.types import …``
   * - ``from aiogram.enums import …``
     - ``from aiorubi.enums import …``
   * - ``@dp.message``
     - ``@dp.new_message``
   * - ``@dp.edited_message``
     - ``@dp.updated_message``
   * - ``@dp.callback_query``
     - ``@dp.inline_message``
   * - ``@dp.my_chat_member`` / ``chat_member``
     - ``@dp.started_bot`` / ``@dp.stopped_bot``
   * - ``Bot(TOKEN)``
     - ``Bot(token=TOKEN)``
   * - ``message.from_user.id``
     - ``message.sender_id``
   * - ``reply_markup=``
     - ``inline_keypad=`` / ``chat_keypad=``
   * - ``Message.photo[-1].file_id``
     - ``message.file.file_id`` (guarded by ``FileType.IMAGE``)
   * - ``callback_query.data``
     - ``inline_message.aux_data.button_id``
   * - ``CallbackQuery``
     - ``InlineMessage``
   * - ``CallbackData(...)`` factory
     - not shipped yet — filter on ``aux_data.button_id``


When *not* to migrate
---------------------

* If your bot talks to the **Telegram** Bot API, stay with aiogram.
  Rubika is a separate platform.
* If you depend on Telegram-specific features that aiorubi does not
  mirror (inline mode, payments, Telegram Passport, games, stickers
  API), you will need to wait — or sponsor the work.
* If you depend on HTML/Markdown text decorations, aiorubi does not
  expose them yet. Use plain text or patch your own formatter.