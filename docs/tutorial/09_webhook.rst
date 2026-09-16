.. _tutorial-webhook:

=================================
9. Deployment: polling vs webhook
=================================

So far the bot has been running with **long polling** — the process
asks Rubika "anything new?" in a loop. That is perfect for
development. In production you usually want a **webhook**: Rubika
pushes each update to *your* HTTPS endpoint as it happens.


Polling — the easy way
======================

Nothing to configure: the default
``await dp.start_polling(bot)`` already includes retry-with-backoff,
clock-skew-safe offsets and graceful shutdown. Optional knobs:

.. code-block:: python

   await dp.start_polling(
       bot,
       limit=100,                     # max updates per request
       polling_interval=0.5,          # pause when no updates
       handle_as_tasks=True,          # process concurrently
       tasks_concurrency_limit=10,    # max parallel handlers
   )


Webhook — the production way
============================

Rubika delivers updates via HTTPS POST to an endpoint you register:

.. code-block:: python

   from aiorubi.enums import UpdateEndpointType

   await bot.update_bot_endpoints(
       url="https://bot.example.com/webhook",
       type=UpdateEndpointType.RECEIVE_UPDATE,
   )

The endpoint must be:

* reachable from the public internet,
* served over HTTPS with a valid certificate,
* fast — Rubika waits up to **60 seconds**, otherwise it re-sends
  the update (aiorubi's default answer timeout is 55 s and slow
  handlers are moved to the background automatically).


Minimal aiohttp server
======================

The library ships a small aiohttp-based webhook server. The sketch
below shows the complete wiring:

.. code-block:: python

   import asyncio
   import logging

   from aiohttp import web

   from aiorubi import Bot, Dispatcher


   async def create_app() -> web.Application:
       logging.basicConfig(level=logging.INFO)

       bot = Bot(token="TOKEN")
       dp = Dispatcher()

       # ... register handlers on dp ...

       async def handle(request: web.Request) -> web.Response:
           payload = await request.json()
           # feed_raw_update parses the dict into an Update for you:
           await dp.feed_raw_update(bot, payload)
           return web.Response(status=200)

       app = web.Application()
       app.router.add_post("/webhook", handle)
       return app


   if __name__ == "__main__":
       app = asyncio.run(create_app())
       web.run_app(app, host="0.0.0.0", port=8443)

For a production-grade setup prefer the built-in
:class:`~aiorubi.webhook.aiohttp_server.SimpleRequestHandler`, which
resolves the bot, closes the session on shutdown and (optionally)
processes updates in the background:

.. code-block:: python

   from aiohttp import web

   from aiorubi import Bot, Dispatcher
   from aiorubi.webhook.aiohttp_server import (
       SimpleRequestHandler,
       setup_application,
   )

   bot = Bot(token="TOKEN")
   dp = Dispatcher()

   # ... register handlers on dp ...

   app = web.Application()
   SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, "/webhook")
   setup_application(app, dp)

   if __name__ == "__main__":
       web.run_app(app, host="0.0.0.0", port=8443)

.. note::

   ``feed_raw_update`` returns after the handler chain *starts*
   processing; ``feed_webhook_update`` additionally enforces the
   55-second answer window and returns a ``RubikaMethod`` — but
   unlike Telegram, Rubika does **not** support answering an update
   by returning an API call in the HTTP response (the webhook body is
   always ``{"status": "OK"}``), so the dispatcher makes that call
   silently on your behalf.


Behind a reverse proxy
======================

In production, terminate TLS with nginx or Caddy and forward to the
app on localhost. Make sure the proxy passes the raw body untouched
and sets no ``Transfer-Encoding`` that aiohttp cannot parse.

Example nginx fragment:

.. code-block:: nginx

   location /webhook {
       proxy_pass http://127.0.0.1:8443;
       proxy_set_header Host $host;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   }


Choosing between them
=====================

.. list-table::
   :header-rows: 1
   :widths: 25 37 38

   * - -
     - Polling
     - Webhook
   * - Setup effort
     - zero
     - needs HTTPS + public host
   * - Latency
     - up to ``polling_interval``
     - instant push
   * - Throughput
     - bounded by loop
     - scales with server
   * - Local development
     - ✅ works behind NAT
     - needs a tunnel (ngrok…)

Rule of thumb: develop with polling, ship with webhook.


Recap
=====

The tutorial is complete. You have a bot that greets, parses
commands, shows keypads, exchanges files, remembers conversation
state, is split into modules, observes its own errors, and can be
deployed either by polling or webhook.

Where to go next:

* :doc:`/guide/index` — every concept in depth.
* :doc:`/api/index` — the full API reference.
* :doc:`/migration-from-aiogram` — bring your aiogram bots over.
