.. _tutorial-files:

==============================
5. Sending & downloading files
==============================

Rubika bots can send images, videos, voices, music, gifs and generic
files — and receive them. aiorubi wraps the whole upload/download
dance behind a handful of methods.


Sending files
=============

The universal method is
:meth:`~aiorubi.client.bot.Bot.send_file`. Its first argument is a
``chat_id``; the second is either:

* a ``file_id`` string (something you received earlier), or
* an :class:`~aiorubi.types.input_file.InputFile` subclass wrapping
  local bytes — ``FSInputFile`` for filesystem paths,
  ``BufferedInputFile`` for in-memory bytes.

.. code-block:: python

   # Re-send a previously uploaded file by id:
   await bot.send_file(chat_id, "AFC3-FE98-...")

   # Send a local file:
   from aiorubi.types.input_file import FSInputFile
   await bot.send_file(chat_id, FSInputFile("/path/to/report.pdf"))


Typed shortcuts
===============

Six convenience methods pick the right ``FileType`` for you:

.. code-block:: python

   await bot.send_image(chat_id, FSInputFile("photo.jpg"))
   await bot.send_video(chat_id, FSInputFile("clip.mp4"))
   await bot.send_voice(chat_id, FSInputFile("note.ogg"))
   await bot.send_music(chat_id, FSInputFile("song.mp3"))
   await bot.send_gif(chat_id, FSInputFile("anim.gif"))
   await bot.send_file(chat_id, FSInputFile("data.zip"))

Each also accepts the usual ``text``, ``inline_keypad``,
``chat_keypad``, ``reply_to_message_id`` … keyword arguments.


Sending files via shortcuts on Message
======================================

Inside a handler the ``reply_*`` / ``answer_*`` shortcuts save you
from repeating the ``chat_id``:

.. code-block:: python

   @dp.new_message(Command("photo"))
   async def send_photo(message):
       await message.answer_image(
           FSInputFile("/bot/assets/photo.jpg"),
           text="این هم عکس من 📸",
       )


Downloading files
=================

To download content the user sent you, pass the file object (or its
``file_id``) to :meth:`~aiorubi.client.bot.Bot.download`:

.. code-block:: python

   @dp.new_message(F.file)
   async def save_file(message):
       f = message.file

       # 1) Download to a path:
       await bot.download(f, destination=f"/tmp/{f.file_id}")

       # 2) …or into memory as BytesIO:
       buf = await bot.download(f)          # returns io.BytesIO
       data = buf.getvalue()                # raw bytes

Under the hood ``download`` resolves the ``file_id`` into a temporary
URL via ``getFile`` and streams the response in 64 KB chunks.

The lower-level
:meth:`~aiorubi.client.bot.Bot.download_file` accepts a URL directly
and is what ``download`` calls internally.


Where file metadata lives
=========================

The :class:`~aiorubi.types.file.File` object on ``message.file``
carries:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Meaning
   * - ``file_id``
     - the id you can re-use to resend or download
   * - ``file_name``
     - original name, if the client sent one
   * - ``size``
     - size in bytes

.. note::

   ``file_id`` strings are stable — store them in your database to
   avoid re-uploading the same content later.


Limits and gotchas
==================

* Always guard media handlers with a filter such as ``F.file`` —
  otherwise plain-text updates will raise ``AttributeError`` inside
  your handler body.
* ``FileType`` for *sending* must match the content: sending an MP3
  with ``send_image`` will confuse the Rubika client apps.
* ``download`` returns ``None`` when you gave a path, and a
  ``BinaryIO`` when you didn't — type your variables accordingly.


Recap
=====

You can now upload local files, resend by ``file_id``, use the typed
``send_*`` shortcuts, and download received files either to disk or
to memory. Next: finite state machines — the memory of your bot.
