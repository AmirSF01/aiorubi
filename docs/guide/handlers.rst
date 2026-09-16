========
Handlers
========

A handler is the code that runs when an update passes all filters of one
observer. Handlers are plain ``async`` callables registered on an observer
with either the decorator or the ``register`` form (see
:doc:`router`).

.. code-block:: python

   @dp.new_message(Command("start"))
   async def cmd_start(message):
       await message.reply("Hello!")

Argument injection
==================

Handlers do not receive a fixed positional list — aiorubi inspects the
signature and passes only the names the handler declares, drawn from the
update context. Declare exactly what you need:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Name
     - Value
   * - ``message``, ``inline_message``, ``event``
     - The event object for the observer (a
       :class:`~aiorubi.types.message.Message`, an
       :class:`~aiorubi.types.inline_message.InlineMessage`, …).
   * - ``bot``
     - The :class:`~aiorubi.client.bot.Bot` instance.
   * - ``event_update``
     - The raw :class:`~aiorubi.types.update.Update` envelope.
   * - ``state`` / ``raw_state``
     - The FSM context / state string (see :doc:`fsm`).
   * - ``scenes``
     - The :class:`~aiorubi.fsm.scene.ScenesManager`, when scenes are
       installed (see :doc:`scenes`).
   * - ``command``
     - The :class:`~aiorubi.filters.command.CommandObject`, injected by the
       ``Command`` filter.
   * - ``button_id``
     - The unpacked ``ButtonId``, injected by ``ButtonId.filter()``.
   * - any workflow-data key
     - Values from ``Dispatcher(**kwargs)`` / ``dp["key"] = ...``.
   * - ``**kwargs``
     - Everything at once.

.. code-block:: python

   @dp.new_message(Command("start"))
   async def cmd_start(message: Message, bot: Bot, command: CommandObject):
       await message.answer(f"command={command.command}, args={command.args}")

Unknown declared names are simply not passed; a handler that declares a
name absent from the context gets nothing for it — use ``**kwargs`` or a
default value if you are unsure.

The first positional parameter conventionally receives the event, but the
mechanism is name-based: ``(message)`` and ``(msg=message)``-style names
only matter for readability. Anything your handler does not declare is not
passed at all.

Message shortcuts
=================

:class:`~aiorubi.types.message.Message` carries shortcuts that build and
bind API calls:

.. code-block:: python

   await message.reply(text)        # quotes the message (reply_to_message_id)
   await message.answer(text)       # plain send into the same chat
   await message.reply_image(file)  # send_file with FileType.IMAGE, quoted
   await message.answer_file(file)
   await message.reply_video(file)
   await message.reply_music(file)
   await message.reply_voice(file)
   await message.reply_gif(file)

All of them accept the keyword arguments of the underlying
``Bot.send_message`` / ``Bot.send_file`` (``inline_keypad=``,
``chat_keypad=``, ``metadata=``, …). :class:`InlineMessage` provides
``answer(text, **kwargs)`` for reacting to button clicks.

Class-based handlers
====================

Subclass :class:`~aiorubi.handlers.base.BaseHandler` and implement
``handle()``. The class is registered like a function; instantiation
happens per update:

.. code-block:: python

   from aiorubi.handlers.base import BaseHandler

   class EchoHandler(BaseHandler[Message]):
       async def handle(self) -> None:
           message: Message = self.event
           await message.answer(self.event.text or "")

   dp.new_message.register(EchoHandler)

Available inside ``handle()``:

* ``self.event`` — the event object.
* ``self.data`` — the whole context dict (including ``state``, filters'
  injected values, workflow data).
* ``self.bot`` — shortcut property for ``self.data["bot"]``.
* ``self.update`` — the raw :class:`~aiorubi.types.update.Update` envelope.

Class-based handlers are convenient when a handler needs constructor-time
configuration shared across updates:

.. code-block:: python

   class RateLimited(BaseHandler[Message]):
       def __init__(self, event, limit: int, **kwargs):
           super().__init__(event, **kwargs)
           self._limit = limit

       async def handle(self) -> None: ...

Controlling propagation
=======================

* Return normally — the observer stops; no other handler runs.
* Raise :class:`~aiorubi.dispatcher.event.bases.SkipHandler` (or call
  ``skip()``) — the observer continues with the *next* handler:

  .. code-block:: python

     from aiorubi.dispatcher.event.bases import SkipHandler, skip

     @dp.new_message(F.text)
     async def filter_commands(message):
         if message.text.startswith("/"):
             skip()          # let the command handlers take it

* Returning a :class:`~aiorubi.methods.base.RubikaMethod` from a webhook
  dispatch answers the webhook with that method.

A handler may also be registered with no filters at all — it then matches
every event of that observer and is typically used as the fallback:

.. code-block:: python

   @dp.new_message()          # must be registered last
   async def fallback(message):
       await message.answer("I don't understand that yet.")

Error handlers
==============

Exceptions escaping any handler are caught by the built-in
:class:`~aiorubi.dispatcher.middlewares.error.ErrorsMiddleware` and routed
to the ``error`` observer. The event there is an
:class:`~aiorubi.types.error_event.ErrorEvent` wrapping ``exception`` and
the original ``update``:

.. code-block:: python

   from aiorubi.types.error_event import ErrorEvent

   @dp.error()
   async def on_error(event: ErrorEvent):
       logging.exception("Handler failed", exc_info=event.exception)

Combine with :class:`~aiorubi.filters.exception.ExceptionTypeFilter` /
``ExceptionMessageFilter`` (see :doc:`filter`) to specialise.

See also
========

* :doc:`filter` — everything about filters.
* :doc:`fsm` — the ``state`` argument in detail.
* :doc:`middlewares` — wrapping handlers with cross-cutting logic.
