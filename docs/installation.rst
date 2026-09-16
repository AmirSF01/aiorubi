============
Installation
============


Stable release
--------------

You can install the latest stable version from PyPI:

.. code-block:: console

   $ pip install aiorubi

That gives you the core runtime dependencies:

* ``aiohttp`` — HTTP client
* ``aiofiles`` — async file IO for sending files from disk
* ``pydantic`` — data models for every API object
* ``magic-filter`` — the filtering DSL powering ``F.text`` and friends
* ``certifi`` — bundled CA bundle for HTTPS
* ``typing-extensions``


Optional extras
---------------

The package ships several *extras* that you can opt into with the
standard ``pip install aiorubi[extra1,extra2]`` syntax.

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Extra
     - Adds
     - Use it for
   * - ``fast``
     - ``uvloop`` (Linux/macOS, PyPy excluded) and ``aiodns``
     - Faster event loop and DNS resolution. Recommended on production.
   * - ``redis``
     - ``redis[hiredis]``
     - :class:`RedisStorage <aiorubi.fsm.storage.redis.RedisStorage>`
       for the FSM.
   * - ``mongo``
     - ``motor`` (async) and ``pymongo``
     - :class:`MongoStorage <aiorubi.fsm.storage.mongo.MongoStorage>`
       and :class:`PyMongoStorage <aiorubi.fsm.storage.pymongo.PyMongoStorage>`
       for the FSM.
   * - ``proxy``
     - ``aiohttp-socks``
     - Connecting through SOCKS proxies.
   * - ``i18n``
     - ``Babel``
     - Internationalisation helpers.
   * - ``docs``
     - ``Sphinx`` and a few helpers
     - Building the documentation locally (this site).


Examples
~~~~~~~~

.. code-block:: console

   # All-in-one (recommended for production)
   $ pip install aiorubi[fast,redis,mongo,proxy,i18n]

   # Just Redis-backed FSM
   $ pip install aiorubi[redis]

   # No extras (slim development setup)
   $ pip install aiorubi


From Git
--------

If you need an unreleased change, install straight from GitHub:

.. code-block:: console

   $ pip install git+https://github.com/AmirSF01/aiorubi.git@main

To install a *specific* tag (for example ``v1.2.1``):

.. code-block:: console

   $ pip install git+https://github.com/AmirSF01/aiorubi.git@v1.2.1


Verify the installation
-----------------------

The following one-liner should print the installed version and the
Rubika Bot API version it targets:

.. code-block:: python

   >>> import aiorubi
   >>> aiorubi.__version__
   '1.2.1'
   >>> aiorubi.__api_version__
   '3'


System requirements
-------------------

* **Python:** 3.10, 3.11, 3.12, 3.13 or 3.14 (3.10 is the lower bound).
* **OS:** any platform that can run ``asyncio`` and ``aiohttp``.
  Linux and macOS are the most tested; Windows works but most users
  run bots on a Linux VPS.
* **Disk space:** ~1 MB for the package itself, plus whatever your
  FSM storage needs.


Troubleshooting
---------------

``pip install aiorubi`` fails with "No matching distribution found"
   You are probably on Python 3.9 or older. ``aiorubi`` requires
   3.10+; upgrade Python or use a ``pyenv``/``uv`` environment.

``Bot`` accepts any token string without validation
   Token format is only *documented* to start with a capital letter;
   ``validate_token`` exists in ``aiorubi.utils.token`` but is not
   invoked automatically. If your token is rejected by the API
   (HTTP 401/403), double-check that no whitespace or newline was
   pasted in and that the token came from
   `@BotFather <https://rubika.ir/BotFather>`_.

``RuntimeError: Bot ID is not available yet``
   Some shortcut (e.g. ``bot.id``) needs the bot info to be loaded.
   Call ``await bot.me()`` (or ``await bot.get_me()``) before reading
   those attributes.