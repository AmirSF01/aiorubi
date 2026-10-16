=====================================
aiorubi |version| documentation
=====================================

**aiorubi** is a modern, fully asynchronous library for the `Rubika Bot API <https://rubika.ir/botapi>`_ written in Python 3.10+ using :doc:`asyncio <python:library/asyncio>` and `aiohttp <https://github.com/aio-libs/aiohttp>`_.

It is heavily inspired by `aiogram <https://docs.aiogram.dev/>`_ and brings the same ergonomic API surface — *Routers*, *Dispatchers*, *Filters*, *Finite State Machines*, *Middlewares* — to the Rubika messaging platform.

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: 🚀 Quickstart
      :link: quickstart
      :link-type: doc

      Get your first bot running in under five minutes.

   .. grid-item-card:: 📚 Tutorial
      :link: tutorial/index
      :link-type: doc

      Step-by-step lessons from ``/start`` to webhooks.

   .. grid-item-card:: 🧭 Guides
      :link: guide/index
      :link-type: doc

      In-depth discussion of every framework concept.

   .. grid-item-card:: 🛠 API Reference
      :link: api/index
      :link-type: doc

      Auto-generated reference for every public class and function.

Features
--------

* **Asynchronous first** — built on top of ``asyncio`` and ``aiohttp``.
* **Routers & Dispatchers** — split your bot into reusable, mountable modules exactly like aiogram.
* **Finite State Machines** — declarative conversation flows with :class:`StatesGroup` and :class:`FSMContext`, with swappable storages (memory, Redis, MongoDB).
* **Scenes** — higher-level wizard abstraction for multi-step dialogs.
* **Filters** — :doc:`MagicFilter <guide/filter>` (``F.text``, ``F.sender_id``, …), :class:`Command`, :class:`ButtonId` callback-data factory, :class:`StateFilter`, and custom filter composition.
* **Middlewares** — both *outer* and *inner* middleware chains per observer, including a built-in error middleware.
* **Flags** — propagate contextual flags from decorator to handler.
* **Keypads** — inline keypads, chat keypads, calendars, number pickers, text boxes, location pickers, selection lists.
* **Webhook & Long-polling** — equally first-class, with aiohttp-based webhook helpers.
* **Fully typed** — annotated with ``typing`` and ``pydantic`` models; great IDE auto-completion.

.. warning::

   Although the *patterns* mirror aiogram 3.x, ``aiorubi`` targets the Rubika Bot API, **not** the Telegram Bot API. Identifiers such as ``chat_id`` and ``message_id`` are ``str`` (not ``int``) and message structure differs — see :doc:`migration-from-aiogram`.

.. tip::

   Coding agents (Claude Code, Cursor, ...) can load a ready-made, code-verified
   skill for working with this library from ``docs/skill/SKILL.md`` and the
   reference sheets in ``docs/skill/references/``.

Installation
------------

.. code-block:: console

   $ pip install aiorubi

For optional extras (Redis, MongoDB, proxy, speed-ups, i18n):

.. code-block:: console

   $ pip install "aiorubi[redis,mongo,proxy,fast,i18n]"

See :doc:`installation` for the full installation guide.

Table of contents
-----------------

.. toctree::
   :caption: Getting started
   :maxdepth: 1

   quickstart
   installation
   migration-from-aiogram

.. toctree::
   :caption: Tutorial
   :maxdepth: 1

   tutorial/index

.. toctree::
   :caption: Guides
   :maxdepth: 1

   guide/index

.. toctree::
   :caption: API Reference
   :maxdepth: 2

   api/index

.. toctree::
   :caption: Project
   :maxdepth: 1

   changelog
   license
