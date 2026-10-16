=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

This changelog is generated from the
`release history <https://pypi.org/project/aiorubi/#history>`_ and
the `git log <https://github.com/AmirSF01/aiorubi/commits/main>`_.


1.2.1 — 2026-08-11
==================

**Fixed**

* Move ``FileType`` import out of the ``TYPE_CHECKING`` block in
  ``aiorubi.types.message`` (broke ``send_file`` at runtime in 1.2.0).


1.2.0 — 2026-08-07
==================

**Added**

* ``reply_*`` / ``answer_*`` shortcuts on ``Message`` for file, gif,
  image, music, video, voice, contact, poll and location.


1.1.0 — 2026-08-07
==================

**Added**

* High-level :meth:`Bot.download() <aiorubi.client.bot.Bot.download>`
  method accepting a ``file_id`` string or any
  :class:`~aiorubi.types.downloadable.Downloadable` object.
* :class:`~aiorubi.types.downloadable.Downloadable` type.
* :meth:`Bot.download_file() <aiorubi.client.bot.Bot.download_file>`
  streaming downloader with configurable chunk size.

**Changed**

* Renamed internal ``build_form_data`` to ``build_payload``.


1.0.8 — 2026-08-04
==================

**Fixed**

* Initialise the polling ``offset_id`` from the Rubika server clock
  instead of the local clock, preventing clock-skew duplicates.


1.0.7 — 2026-08-04
==================

**Fixed**

* Ensure bot info is loaded before use via ``on_startup`` and
  ``resolve_bot`` in the webhook handlers.
* ``Bot.id`` now raises a descriptive :class:`RuntimeError` when the
  bot info has not been loaded yet.


1.0.6 — 2026-08-02
==================

Maintenance release (CI and packaging fixes).


1.0.5 — 2026-07-05
==================

Maintenance release.


1.0.0 — 2026-06-29
==================

**First stable release.**

* Full asynchronous Rubika Bot API client
  (:class:`~aiorubi.client.bot.Bot`).
* Dispatcher with routers, observers and middlewares.
* FSM with memory storage and scenes.
* Built-in filters (``Command``, ``StateFilter``, ``MagicData``, …).
* Long polling with automatic backoff.
* Webhook helpers for aiohttp.


0.0.1 — 2026-02-18
==================

Reserved name, empty placeholder release.
