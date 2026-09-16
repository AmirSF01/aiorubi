=======
Filters
=======

All filters live in the :mod:`aiorubi.filters` package. The base
class is exported as both ``Filter`` and ``BaseFilter``.

Base
====

.. autoclass:: aiorubi.filters.base.Filter
   :members:

Command
=======

.. autoclass:: aiorubi.filters.command.Command
   :members:

.. autoclass:: aiorubi.filters.command.CommandStart
   :members:

.. autoclass:: aiorubi.filters.command.CommandObject
   :members:

State
=====

.. autoclass:: aiorubi.filters.state.StateFilter
   :members:

Magic data
==========

.. autoclass:: aiorubi.filters.magic_data.MagicData
   :members:

Exceptions
==========

.. autoclass:: aiorubi.filters.exception.ExceptionTypeFilter
   :members:

.. autoclass:: aiorubi.filters.exception.ExceptionMessageFilter
   :members:

Logic combinators
=================

.. autofunction:: aiorubi.filters.logic.and_f

.. autofunction:: aiorubi.filters.logic.or_f

.. autofunction:: aiorubi.filters.logic.invert_f

Magic filter
============

.. autoclass:: aiorubi.utils.magic_filter.MagicFilter
   :members:

.. data:: aiorubi.F

   The shared :class:`~aiorubi.utils.magic_filter.MagicFilter` root.
