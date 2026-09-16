=======
Webhook
=======

Webhook support built on top of aiohttp.

.. autoclass:: aiorubi.webhook.aiohttp_server.SimpleRequestHandler
   :members:
   :special-members: __init__, register

.. autoclass:: aiorubi.webhook.aiohttp_server.TokenBasedRequestHandler
   :members:
   :special-members: __init__, register

.. autofunction:: aiorubi.webhook.aiohttp_server.setup_application

.. autoclass:: aiorubi.webhook.security.IPFilter
   :members:

.. autofunction:: aiorubi.webhook.aiohttp_server.ip_filter_middleware
