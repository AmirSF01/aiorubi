=======
Session
=======

HTTP session layer used by :class:`~aiorubi.client.bot.Bot` to talk
to the Rubika Bot API.

Base session
============

.. autoclass:: aiorubi.client.session.base.BaseSession
   :members:
   :special-members: __call__

aiohttp implementation
======================

.. autoclass:: aiorubi.client.session.aiohttp.AiohttpSession
   :members:
   :special-members: __init__

Session middlewares
===================

.. autoclass:: aiorubi.client.session.middlewares.base.BaseRequestMiddleware
   :members:

.. autoclass:: aiorubi.client.session.middlewares.request_logging.RequestLogging
   :members:

.. autoclass:: aiorubi.client.session.middlewares.manager.RequestMiddlewareManager
   :members:
