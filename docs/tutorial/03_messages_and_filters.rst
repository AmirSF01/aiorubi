.. _tutorial-messages:

=================================
3. Messages, media & event types
=================================

Rubika delivers several kinds of updates. So far we only handled
``new_message``. In this chapter we will look at the ``Message``
model, the other observers, and how to react to media.


The Message model
=================

Every message — text, image, voice, poll, … — is one
:class:`~aiorubi.types.message.Message` object. Content lives in
dedicated attributes:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Present when
   * - ``text``
     - plain text message
   * - ``file``
     - image, video, voice, music, gif or generic file
   * - ``sticker``
     - sticker message
   * - ``location``
     - shared location
   * - ``contact_message``
     - shared contact
   * - ``poll``
     - native poll

Exactly one of them is set (plus always ``message_id``, ``time``,
``sender_id``, ``chat_id``).

.. code-block:: python

   @dp.new_message(F.file)
   async def got_file(message):
       f = message.file
       await message.answer(
           f"فایل گرفتم: {f.file_name} "
           f"(حجم {f.size} بایت)"
       )

``F.file`` is truthy only when the message actually carries a file.


Other observers
===============

A :class:`Router <aiorubi.dispatcher.router.Router>` exposes one
observer per Rubika update type:

.. list-table::
   :header-rows: 1

   * - Observer
     - Event object
   * - ``new_message``
     - :class:`~aiorubi.types.message.Message`
   * - ``updated_message``
     - :class:`~aiorubi.types.message.Message` (edited version)
   * - ``removed_message``
     - :class:`~aiorubi.types.removed_message.RemovedMessage`
   * - ``inline_message``
     - :class:`~aiorubi.types.inline_message.InlineMessage`
   * - ``started_bot``
     - :class:`~aiorubi.types.started_bot.StartedBot`
   * - ``stopped_bot``
     - :class:`~aiorubi.types.stopped_bot.StoppedBot`
   * - ``errors``
     - :class:`~aiorubi.types.error_event.ErrorEvent`

Example — reacting to edits:

.. code-block:: python

   @dp.updated_message()
   async def edited(message):
       await message.answer("پیامت رو ویرایش کردی! 👀")


Message shortcuts
=================

The ``Message`` object carries shortcuts for the most common replies.
Each has a ``reply_*`` (quotes the message) and an ``answer_*``
(does not quote) variant:

.. code-block:: python

   await message.reply(text)              # SendMessage
   await message.reply_image(image)       # send_image + reply_to
   await message.answer_video(video)      # send_video, no quote
   await message.reply_location(lat, lon)
   await message.answer_poll("سوال؟", ["بله", "خیر"])
   await message.reply_contact(first_name, phone_number)

All of them accept the same optional keyword arguments as their
``Bot.send_*`` counterpart (``inline_keypad``, ``chat_keypad``,
``metadata``, ``disable_notification``, …).


Reply and answer — the difference
=================================

.. code-block:: python

   # This sends "سلام" quoting the user's message:
   await message.reply("سلام")

   # This sends "سلام" as a standalone message in the same chat:
   await message.answer("سلام")

Inside a ``new_message`` handler both go to the same ``chat_id`` —
``reply`` merely sets ``reply_to_message_id``.


sender_id — the user behind the message
=======================================

Rubika messages carry the sender id as a string:

.. code-block:: python

   @dp.new_message(Command("whoami"))
   async def whoami(message):
       await message.answer(
           f"chat_id = {message.chat_id}\n"
           f"sender_id = {message.sender_id}\n"
           f"sender_type = {message.sender_type}"
       )

.. note::

   These ids are **strings** (e.g. ``"3827491023"``), never integers.
   Storing them in a JSON column or dict key works out of the box.


Errors as an event
==================

Exceptions raised inside any handler are caught by the built-in error
middleware and routed to the ``errors`` observer. We will use this in
chapter 8 to build a proper error handler.


Recap
=====

You now know the ``Message`` model, all seven observers, and the
``reply_*``/``answer_*`` shortcut family. Next: interactive keypads —
the heart of any Rubika bot.
