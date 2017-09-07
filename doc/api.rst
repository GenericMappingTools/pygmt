.. _api:

API Reference
=============

.. currentmodule:: gmt


Plotting
--------

.. autosummary::
    :toctree: api/
    :template: class.rst

    Figure


Utility functions
-----------------

.. autosummary::
    :toctree: api/
    :template: function.rst

    test


Low-level wrappers for the GMT C API
------------------------------------

The GMT C shared library (``libgmt``) is accessed using ctypes_.
The ``gmt.clib`` package offers the :class:`~gmt.clib.LibGMT` class that wraps
the C shared library with a pythonic interface.
Most interactions with ``libgmt`` are done through this class.

.. autosummary::
    :toctree: api/
    :template: class.rst

    clib.LibGMT


.. _ctypes: https://docs.python.org/3/library/ctypes.html
