=======
Webhook
=======

Besides long-polling (see :doc:`dispatcher`), aiorubi can receive
updates over HTTP. Rubika pushes updates to a public HTTPS endpoint you
register with :meth:`Bot.update_bot_endpoints
<aiorubi.client.bot.Bot.update_bot_endpoints>`; aiorubi ships an
aiohttp-based server and request handler to receive them.

Registering the endpoint
========================

.. code-block:: python

   from aiorubi.enums import UpdateEndpointType

   status = await bot.update_bot_endpoints(
       url="https://example.com/webhook",
       type=UpdateEndpointType.RECEIVE_UPDATE,
   )

After a successful registration Rubika POSTs every update as JSON to that
URL. Give Rubika **60 seconds** to answer; the dispatcher's webhook entry
point enforces a 55-second budget and moves slower handlers to the
background (see below).

The webhook request handler
===========================

.. class:: aiorubi.webhook.aiohttp_server.BaseRequestHandler(dispatcher, handle_in_background=False, **data)

Subclass it and implement ``resolve_bot(request)`` — the method that maps
an incoming request to the :class:`~aiorubi.client.bot.Bot` that should
process it. ``register(app, *paths, **kwargs)`` then attaches the route:

.. code-block:: python

   from aiorubi.webhook.aiohttp_server import BaseRequestHandler

   class WebhookHandler(BaseRequestHandler):
       async def resolve_bot(self, request):
           return bot

   webhook_handler = WebhookHandler(dispatcher=dp, handle_in_background=True)
   webhook_handler.register(app, "/webhook")

Behaviour:

* The JSON body is parsed with the bot session's loader and passed to
  ``dp.feed_raw_update`` (a raw ``dict`` is validated into an
  :class:`~aiorubi.types.update.Update` automatically).
* ``handle_in_background=False`` (default) awaits the pipeline and answers
  with ``{"status": "OK"}``; a returned
  :class:`~aiorubi.methods.base.RubikaMethod` is still answered with the
  same body — **Rubika does not support returning API calls in the
  webhook response** (unlike Telegram), so delayed calls go through
  ``dp.silent_call_request`` in the background.
* ``handle_in_background=True`` answers immediately and processes the
  update in an :class:`asyncio.Task`.
* The handler registers its own ``close()`` on app shutdown to await
  leftover background tasks.

Note that the response writer is deliberately fixed: every answer body is
``{"status": "OK"}``.

Wiring the aiohttp application
==============================

``setup_application(app, dispatcher, **kwargs)``

Connects the application lifecycle to the dispatcher: on startup it emits
``dp.emit_startup(**workflow_data)``, on shutdown ``dp.emit_shutdown(...)``
(closing the FSM storage). Extra ``kwargs`` join the workflow data handed
to handlers.

Full example
------------

.. code-block:: python
   :caption: webhook_bot.py

   import asyncio
   import logging

   from aiohttp import web

   from aiorubi import Bot, Dispatcher
   from aiorubi.enums import UpdateEndpointType
   from aiorubi.filters.command import Command
   from aiorubi.webhook.aiohttp_server import (
       BaseRequestHandler,
       setup_application,
   )

   BOT_TOKEN = "YOUR_RUBIKA_BOT_TOKEN"
   WEBHOOK_URL = "https://example.com/webhook"
   WEBHOOK_PATH = "/webhook"

   dp = Dispatcher()

   @dp.new_message(Command("start"))
   async def cmd_start(message):
       await message.reply("Hello from a webhook bot!")

   class WebhookHandler(BaseRequestHandler):
       async def resolve_bot(self, request):
           return bot

   async def main():
       global bot
       logging.basicConfig(level=logging.INFO)

       bot = Bot(token=BOT_TOKEN)
       await bot.me()

       await bot.update_bot_endpoints(
           url=WEBHOOK_URL,
           type=UpdateEndpointType.RECEIVE_UPDATE,
       )

       app = web.Application()
       WebhookHandler(dispatcher=dp).register(app, WEBHOOK_PATH)
       setup_application(app, dp)

       runner = web.AppRunner(app)
       await runner.setup()
       site = web.TCPSite(runner, host="0.0.0.0", port=8080)
       await site.start()

       try:
           await asyncio.Event().wait()      # run forever
       finally:
           await runner.cleanup()

   if __name__ == "__main__":
       asyncio.run(main())

Security: IP filtering
======================

`aiorubi.webhook.security.IPFilter`

Rubika posts updates from its own servers. To reject requests from anyone
else, install the IP-filter middleware (it honours ``X-Forwarded-For`` when
running behind a reverse proxy and answers ``401`` for blocked sources):

.. code-block:: python

   from ipaddress import IPv4Network

   from aiorubi.webhook.aiohttp_server import ip_filter_middleware
   from aiorubi.webhook.security import IPFilter

   app.middlewares.append(
       ip_filter_middleware(IPFilter([IPv4Network("5.0.0.0/8")]))
   )

Webhook vs polling
==================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Webhook
     - Polling
   * - Needs a public HTTPS endpoint and TLS
     - Works from any machine with outbound internet
   * - Lower latency; no ``get_updates`` traffic
     - Simpler ops; built-in exponential backoff
   * - 60 s response budget; slow handlers must be backgrounded
     - No response budget
   * - ``dp.feed_webhook_update`` / ``BaseRequestHandler``
     - ``dp.start_polling``

For development behind NAT or without a domain, prefer polling; for
production on a VM with a certificate, webhooks reduce latency.

See also
========

* :doc:`dispatcher` — ``feed_webhook_update`` timeout semantics and
  ``silent_call_request``.
* :doc:`handlers` — what handlers receive in webhook mode (the same
  context as in polling).
