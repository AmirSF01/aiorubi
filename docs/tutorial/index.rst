===============
Tutorial
===============

Welcome to the aiorubi tutorial! By the end of this 9-chapter journey
you will have built a complete Rubika bot with commands, keypads,
file handling, finite state machines, and a webhook deployment.

.. toctree::
   :maxdepth: 1

   01_intro
   02_commands
   03_messages_and_filters
   04_keypads
   05_files
   06_fsm
   07_router
   08_middlewares
   09_webhook

To get the most out of this tutorial you need:

* Python 3.10+
* ``pip install aiorubi``
* A Rubika bot token from `@BotFather <https://rubika.ir/BotFather>`_.

We recommend reading the chapters in order — each chapter builds on
concepts from the previous one, and the running example (a "note-taking
bot" that stores notes in FSM storage) grows chapter by chapter.

.. note::

   All code in this tutorial is also available as a single file per
   chapter. Copy each chapter's code into ``bot.py`` and run
   ``python bot.py`` to see it live.

Prerequisites
-------------

If you have not yet installed aiorubi, follow
:doc:`/installation` first. If you are already familiar with
aiogram 3.x you can skim :doc:`/migration-from-aiogram` and jump to
:doc:`01_intro`.