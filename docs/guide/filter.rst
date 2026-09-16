=======
Filters
=======

Filters decide whether an update should reach a handler. Every observer
call — ``@dp.new_message(...)``, ``@router.inline_message(...)`` — accepts
an arbitrary number of filters as positional arguments. All filters must
pass for the handler to be triggered, and the observer stops propagation at
the **first** matching handler.

.. code-block:: python

   @dp.new_message(Command("start"), F.text)
   async def cmd_start(message):
       await message.reply("Hello!")

Built-in filters
================

All of these live in :mod:`aiorubi.filters` (re-exported from
``aiorubi.filters.command``, ``...state``, etc.):
``Command``, ``CommandStart``, ``CommandObject``, ``StateFilter``,
``MagicData``, ``ExceptionTypeFilter``, ``ExceptionMessageFilter``, the
combinators ``and_f`` / ``or_f`` / ``invert_f``, and the base class
``Filter`` (alias ``BaseFilter``).

Command
-------

`aiorubi.filters.command.Command(*values, commands=None, prefix="/", ignore_case=False, ignore_mention=False, magic=None)`

Matches text messages that start with one of the given commands. Works only
with :class:`~aiorubi.types.message.Message` events that have a ``text``.

* ``values`` / ``commands`` — command names (``"start"``) or compiled
  regular expressions; ``BotCommand`` objects are accepted too.
* ``prefix`` — allowed prefix characters, default ``"/"``. Pass ``"/!"`` to
  accept both ``/start`` and ``!start``.
* ``ignore_case`` — case-fold matching (does not apply to regexp patterns).
* ``ignore_mention`` — by default a command addressed to another bot
  (``/start@other_bot``) does not match; set ``True`` to ignore the
  mention.
* ``magic`` — an extra :class:`~aiorubi.utils.magic_filter.MagicFilter`
  applied to the parsed :class:`~aiorubi.filters.command.CommandObject`.

When the filter passes it injects the ``command`` keyword argument — a
frozen dataclass with ``prefix``, ``command``, ``mention``, ``args``,
``regexp_match`` and the helpers ``.mentioned`` and ``.text``:

.. code-block:: python

   @dp.new_message(Command("start"))
   async def cmd_start(message, command: CommandObject):
       await message.reply(f"Command: {command.command}, args: {command.args}")

:class:`~aiorubi.filters.command.CommandStart` is a shortcut for
``Command("start")`` with deep-link validation:
``CommandStart(deep_link=True, deep_link_encoded=True)`` requires a
payload argument and base64-decodes it.

StateFilter
-----------

`aiorubi.filters.state.StateFilter(*states)`

Checks the update against the current FSM state (see :doc:`fsm`).
Accepts any mix of :class:`~aiorubi.fsm.state.State` objects,
``StatesGroup`` classes/instances, raw strings, ``None`` and the ``"*"``
wildcard — at least one is required:

.. code-block:: python

   from aiorubi.filters import StateFilter

   @dp.new_message(StateFilter(Form.name))       # one state
   @dp.new_message(StateFilter(Form))            # any state of the group
   @dp.new_message(StateFilter(None, "*"))       # no state, or any state

Subclassing a ``StatesGroup`` includes the parent's states in the check.
Passing a :class:`~aiorubi.fsm.state.State` as decorator filter is
equivalent to the plain ``Form.name`` shorthand shown in :doc:`fsm`.

CallbackData (ButtonId)
-----------------------

Rubika inline keypads carry a ``button_id`` string in the
``aux_data`` of an :class:`~aiorubi.types.inline_message.InlineMessage`.
The :mod:`aiorubi.filters.callback_data` module provides a structured
wrapper for it:

``aiorubi.filters.callback_data.ButtonId``

A pydantic model base class. Subclass it with a required ``prefix=``
keyword and declare the payload fields; then use ``.pack()`` when building
keypads and ``.filter()`` as the handler filter:

.. code-block:: python

   from aiorubi import F
   from aiorubi.filters.callback_data import ButtonId

   class Nav(ButtonId, prefix="nav"):
       action: str
       page: int = 0

   # packing — when creating the keypad button
   button_id=Nav(action="next", page=2).pack()      # "nav:next:2"

   # filtering — on the inline_message observer.
   # The rule is a magic-filter expression resolved against the *unpacked*
   # Nav instance; use the module-level ``F`` object, not class attributes
   # (``Nav.action`` does not exist on the pydantic class):
   @dp.inline_message(Nav.filter(F.action == "next"))
   async def nav_next(inline_message: InlineMessage, button_id: Nav):
       ...

``Nav.filter(rule=None)`` returns an
:class:`~aiorubi.filters.callback_data.InlineMessageFilter` which unpacks
the incoming ``button_id`` and injects it as the ``button_id`` argument.
Encodable field types: ``str``, ``int``, ``float``, ``bool``, ``Enum``,
``UUID``, ``Decimal``, ``Fraction`` and ``None`` (optional fields).
The packed id must stay under 64 bytes.

MagicData
---------

`aiorubi.filters.magic_data.MagicData(magic_data: MagicFilter)`

Resolves a magic-filter expression against the whole handler *context* —
the event (as ``F.event``) plus every keyword the dispatcher provides
(``bot``, ``state``, ``raw_state``, ``event_chat``, ``event_from_user``,
…):

.. code-block:: python

   from aiorubi.filters import MagicData

   @dp.new_message(MagicData(F.event.text == "/stop"), any_state)
   async def emergency_stop(message): ...

ExceptionTypeFilter / ExceptionMessageFilter
--------------------------------------------

For the ``error`` observer, whose event is an
:class:`~aiorubi.types.error_event.ErrorEvent`:

.. code-block:: python

   from aiorubi.filters import ExceptionTypeFilter, ExceptionMessageFilter

   @dp.error(ExceptionTypeFilter(RubikaAPIError))
   async def api_error_handler(event: ErrorEvent): ...

   @dp.error(ExceptionMessageFilter(r"^Timeout.*"))
   async def timeout_handler(event: ErrorEvent, match_exception: Match): ...

``ExceptionMessageFilter`` injects the regexp match as ``match_exception``.


MagicFilter — the ``F`` object
==============================

``F`` (exported from :mod:`aiorubi`) is a
:class:`aiorubi.utils.magic_filter.MagicFilter` instance. Indexing or
calling attributes on it *builds* a filter expression; the expression is
resolved against the event when a filter check runs:

.. code-block:: python

   F.text                     # message.text is not None
   F.text == "hello"          # equality
   F.text.startswith("/")     # method call
   F.text.contains("spam") | F.text.contains("ads")   # OR
   F.text & F.sender_id == "12345"                    # AND
   ~F.text                            # negation (NOT)
   F.sender_id != "12345"
   F.file.file_type == FileType.IMAGE
   F.location != None                 # noqa: E711 — a location is attached

The result of any expression is a valid filter, so you can mix ``F`` with
the built-ins freely.

Storing results with ``as_()``
------------------------------

aiorubi extends the upstream magic-filter with ``as_(name)``: when the
filter passes, the resolved value is injected into the handler under
``name``:

.. code-block:: python

   @dp.new_message(F.text.as_("user_text"))
   async def echo(message, user_text: str):
       await message.answer(user_text)

Writing custom filters
======================

Async and sync function filters
-------------------------------

The simplest filter is a function. It receives the event plus the same
contextual keyword arguments as a handler and returns ``bool`` — or a
``dict`` whose entries are injected into the handler:

.. code-block:: python

   async def is_admin(message, event_from_user, **kwargs):
       return str(event_from_user) in ADMINS

   dp.new_message.register(admin_handler, is_admin)

Synchronous functions work too — they are executed in a thread via
:func:`asyncio.to_thread`, so long CPU-bound checks do not block the loop.

Class-based filters
-------------------

Subclass :class:`~aiorubi.filters.base.Filter` and override the async
``__call__``. Constructor arguments make the filter configurable and
instances are reusable:

.. code-block:: python

   from aiorubi.filters.base import Filter

   class ContactMessage(Filter):
       def __init__(self, with_phone: bool = True):
           self.with_phone = with_phone

       async def __call__(self, message: Message) -> bool | dict[str, Any]:
           contact = message.contact_message
           if not contact:
               return False
           if self.with_phone and not contact.phone_number:
               return False
           return {"contact": contact}

   @dp.new_message(ContactMessage())
   async def got_contact(message, contact: ContactMessage):
       await message.reply(f"Thanks, {contact.first_name}!")

Returning ``False`` skips the handler; returning ``True`` passes; returning
a ``dict`` passes **and** merges the entries into the handler kwargs.

Lambdas and ``F`` both work as drop-in callables — the dispatcher detects
``MagicFilter`` instances (including the plain ``magic_filter`` package
object) automatically.

Combining filters
=================

* **Positional arguments** on an observer are combined with logical AND:
  all must pass.
* ``&`` / ``|`` / ``~`` on magic-filter expressions build combined
  expressions.
* ``and_f``, ``or_f`` and ``invert_f`` combine arbitrary filters
  (class-based or functions):

  .. code-block:: python

     from aiorubi.filters import and_f, or_f, invert_f

     @dp.new_message(or_f(Command("ban"), Command("unban")), is_admin)
     async def ban_handler(message, command): ...

  ``~filter`` (invert) works on any :class:`~aiorubi.filters.base.Filter`
  instance.

Filter order and short-circuiting
=================================

Two independent short-circuits are at play:

1. **Within one handler** — filters are checked in declaration order and
   the check stops at the first failure. Put cheap filters first:

   .. code-block:: python

      # good: text check is nearly free, admin check hits the DB
      @dp.new_message(F.text, is_admin)
      async def admin_echo(message): ...

2. **Within one observer** — handlers are evaluated in registration order
   and propagation stops at the first fully matching handler. A handler can
   pass control to the next one by raising
   :class:`~aiorubi.dispatcher.event.bases.SkipHandler`. Router-level
   filters (``observer.filter(...)``) are checked before handler filters.

How filters receive data
========================

Every filter call receives ``(event, **context)``. The context is built by
the middleware chain and includes at least:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Key
     - Provided by
   * - ``bot``
     - The :class:`~aiorubi.client.bot.Bot` instance (always present).
   * - ``event_update``
     - The raw :class:`~aiorubi.types.update.Update` envelope.
   * - ``event_context``, ``event_from_user``, ``event_chat``
     - :class:`~aiorubi.dispatcher.middlewares.user_context.UserContextMiddleware`.
   * - ``state``, ``raw_state``, ``fsm_storage``
     - The FSM middleware (unless FSM is disabled) — see :doc:`fsm`.
   * - ``scenes``
     - The scenes middleware, when a
       :class:`~aiorubi.fsm.scene.SceneRegistry` is installed — see
       :doc:`scenes`.
   * - dict results of earlier filters
     - e.g. ``command``, ``button_id``, ``match_exception``.

Type your filter's ``__call__`` with only the parameters it needs — any
declared parameter name is matched from the context, exactly like handler
dependency injection.

See also
========

* :doc:`fsm` — state filters and the ``raw_state`` value.
* :doc:`scenes` — scenes use the same filter syntax inside
  ``@scene.on.new_message(...)``.
* :doc:`dispatcher` — observer registration order and router filters.
