=====
Flags
=====

Flags are small pieces of metadata attached to a handler *at registration
time* and readable from middlewares, other handlers of the same dispatch,
and utility code. Where middlewares inject per-update data, flags carry
per-handler configuration.

Declaring flags
===============

The global ``flags`` object (exported from :mod:`aiorubi`) generates a
flag decorator for any attribute name:

.. code-block:: python

   from aiorubi import flags

   @dp.new_message(Command("ban"))
   @flags.admin_only
   async def cmd_ban(message): ...

``flags.<name>`` with no call simply marks the handler with
``{"<name>": True}``. To attach a value, call the decorator:

.. code-block:: python

   @flags.rate_limit(2.5)          # {"rate_limit": 2.5}
   @flags.chat_action("typing")    # chat-action helper flag
   @dp.new_message(F.text)
   async def echo(message): ...

Keyword form builds an :class:`AttrDict` value — useful for grouped
settings:

.. code-block:: python

   @flags.permissions(write=True, invite=False)
   # -> {"permissions": AttrDict(write=True, invite=False)}

The decorator is chainable: multiple ``@flags.*`` lines stack, and
re-declaring the same name replaces its value.

Flags may also be attached to any callable — class-based handlers
included:

.. code-block:: python

   @flags.admin_only
   class BanHandler(BaseHandler[Message]):
       async def handle(self) -> None: ...

Reading flags
=============

Three helpers live in :mod:`aiorubi.dispatcher.flags`:

* ``extract_flags(obj)`` — all flags of a handler.
* ``get_flag(handler, name, default=None)`` — one flag.
* ``check_flags(handler, magic)`` — query flags with a magic-filter
  expression, e.g. ``check_flags(handler, F.admin_only)``.

Inside a middleware the handler object is available under the ``"handler"``
key of ``data``:

.. code-block:: python

   class AdminGate(BaseMiddleware):
       async def __call__(self, handler, event, data):
           if get_flag(data["handler"], "admin_only", default=False):
               if str(data.get("event_from_user")) not in ADMINS:
                   return None              # silently drop
           return await handler(event, data)

Because flags are stored on the handler object (``handler.flags``), they
cost nothing per update until read.

Built-in flag usage
===================

* Filters can contribute flags at registration time:
  :class:`~aiorubi.filters.command.Command` appends itself to the
  ``commands`` flag (``update_handler_flags``) — used by command-listing
  tooling.
* The ``chat_action`` flag is recognised by aiogram-compatible tooling;
  aiorubi does not ship a built-in runner for it (no chat-action API on
  Rubika), but the flag slot is reserved.

Writing flag-driven extensions
==============================

Flags shine when combined with middlewares or the observer registry to
build conventions:

.. code-block:: python

   from aiorubi import flags

   @flags.route("games/echo")
   @dp.new_message(F.text)
   async def echo(message): ...

   # later: build an index of all handlers
   index = {}
   for h in dp.new_message.handlers:
       route = get_flag(h, "route")
       if route:
           index[route] = h.callback

Notes and pitfalls
==================

* Flag names must not start with an underscore — ``flags._private``
  raises :class:`AttributeError`.
* ``@flags.x`` and ``@flags.x(...)`` both return the original callable,
  so flag decorators never change the handler's signature or break
  :doc:`argument injection <handlers>`.
* Flags are registration-time only: changing them at runtime means
  mutating ``handler.flags`` directly (supported, but unusual).
* Order with the observer decorator matters — put ``@dp.new_message(...)``
  *above* the flags so the flags are already attached when the handler is
  registered (decorators apply bottom-up).

See also
========

* :doc:`middlewares` — the usual consumers of flags.
* :doc:`filter` — MagicFilter, which ``check_flags`` reuses.
