======
Guides
======

Concept-by-concept guides for aiorubi. Each page is self-contained; read
them in order if you are new to the framework.

.. toctree::
   :maxdepth: 1

   dispatcher
   router
   handlers
   middlewares
   flags
   filter
   fsm
   storages
   scenes
   webhook

Quick links
-----------

* :doc:`dispatcher` — the root of the update pipeline: observers, polling
  and webhooks, workflow data.
* :doc:`router` — splitting a bot into mountable modules.
* :doc:`handlers` — function and class-based handlers, argument injection.
* :doc:`middlewares` — outer/inner middleware chains.
* :doc:`flags` — passing metadata from decorators to handlers.
* :doc:`filter` — built-in filters, MagicFilter (``F``) and custom filters.
* :doc:`fsm` — finite state machine: states, context, strategies.
* :doc:`storages` — Memory, Redis and MongoDB FSM storages, key builders.
* :doc:`scenes` — wizard-style multi-step dialogs on top of the FSM.
* :doc:`webhook` — receiving updates over HTTP with aiohttp.
