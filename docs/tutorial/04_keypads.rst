.. _tutorial-keypads:

================
4. Keypads
================

Keypads are Rubika's answer to keyboards. There are two display
modes, both described by a single class
:class:`~aiorubi.types.keypad.Keypad`:

* **inline keypad** — buttons shown under a specific message
  (like aiogram's inline keyboard),
* **chat keypad** — buttons pinned at the bottom of the chat
  (like aiogram's reply keyboard).


Anatomy of a keypad
===================

A keypad is a list of rows; each row is a list of buttons:

.. code-block:: python

   from aiorubi.types import Keypad, KeypadRow, Button

   keypad = Keypad(
       rows=[
           KeypadRow(buttons=[
               Button(id="btn_new", type="Simple", button_text="📝 یادداشت جدید"),
               Button(id="btn_list", type="Simple", button_text="📋 لیست"),
           ]),
           KeypadRow(buttons=[
               Button(id="btn_help", type="Simple", button_text="❓ راهنما"),
           ]),
       ]
   )

   await message.answer("چیکار می‌خوای بکنی؟", inline_keypad=keypad)

``Button`` needs three things: a unique ``id`` (what you will receive
in ``aux_data.button_id`` when tapped), a ``type`` (e.g. ``"Simple"``)
and the ``button_text`` shown to the user.


Handling button clicks — inline_message
=======================================

When the user taps an *inline* button, Rubika sends an
``InlineMessage`` update and your ``inline_message`` observer fires.
The tapped button's id arrives in ``aux_data.button_id``:

.. code-block:: python

   from aiorubi.types import InlineMessage

   @dp.inline_message(lambda c: c.aux_data.button_id == "btn_new")
   async def on_new_button(call: InlineMessage):
       await call.answer("بزن بریم! یادداشت جدید...")

A ``CallbackData`` factory is **not** currently shipped with aiorubi —
the package exposes ``Command``, ``CommandStart``, ``CommandObject``,
``StateFilter``, ``MagicData``, ``ExceptionTypeFilter``,
``ExceptionMessageFilter``, the combinators ``and_f`` / ``or_f`` /
``invert_f`` and the ``Filter`` base class. For typed callback data,
route on ``aux_data.button_id`` values directly (as shown above), or
write your own small factory filter on top of
:class:`~aiorubi.filters.base.Filter`.

Filtering on the button id is the simplest way to route clicks. The
full filter toolkit is described in :doc:`/guide/filter`.

.. note::

   ``InlineMessage`` is *not* a ``Message``. It has ``sender_id``,
   ``chat_id``, ``aux_data`` and an ``aux_data.button_id``, but no
   ``text`` and no ``reply()`` shortcuts. Use
   ``await call.answer(...)`` to respond.


Chat keypad
===========

A *chat keypad* replaces the user's typing area with buttons. Send it
via the ``chat_keypad`` keyword:

.. code-block:: python

   chat_keypad = Keypad(
       rows=[
           KeypadRow(buttons=[
               Button(id="cmd_new", type="Simple", button_text="📝 جدید"),
               Button(id="cmd_list", type="Simple", button_text="📋 لیست"),
           ]),
       ]
   )

   await bot.edit_chat_keypad(
       chat_id=message.chat_id,
       chat_keypad=chat_keypad,
   )

When the user taps a chat keypad button, the bot receives a regular
``new_message`` update whose ``aux_data.button_id`` holds the button
id — so the same ``Button.id`` routing applies:

.. code-block:: python

   @dp.new_message(F.aux_data.button_id == "cmd_list")
   async def chat_keypad_list(message):
       await send_note_list(message)


Removing a chat keypad
======================

There is no "remove keyboard" object. Instead call
:meth:`~aiorubi.client.bot.Bot.remove_chat_keypad`:

.. code-block:: python

   await bot.remove_chat_keypad(chat_id=message.chat_id)


The rich button family
======================

Besides plain ``Button``, Rubika ships interactive button types. All
of them live in ``aiorubi.types``:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Class
     - Purpose
   * - ``ButtonSelection``
     - a menu of options with search support
   * - ``ButtonCalendar``
     - a date picker
   * - ``ButtonNumberPicker``
     - up/down number picker
   * - ``ButtonStringPicker``
     - string picker
   * - ``ButtonTextbox``
     - free-text input with a keypad type
   * - ``ButtonLocation``
     - "share my location" button

Example — a number picker for quantity:

.. code-block:: python

   from aiorubi.types import ButtonNumberPicker

   keypad = Keypad(
       rows=[
           KeypadRow(buttons=[
               ButtonNumberPicker(
                   min_value=1,
                   max_value=10,
                   title="تعداد",
                   default_value=1,
               ),
           ]),
       ]
   )

Consult the API reference for the exact constructor arguments of each
button class.


Recap
=====

You can now attach interactive keypads to messages, react to inline
button clicks via the ``inline_message`` observer, pin a chat keypad
with ``edit_chat_keypad``, and remove it with
``remove_chat_keypad``. Next: sending and downloading files.
