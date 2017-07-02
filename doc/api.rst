.. _api:

API Reference
=============

High-level functions for GMT modules
------------------------------------

Each GMT module (``gmt pscoas``, ``gmt grdgradient``, etc.) is wrapped by a
function in the ``gmt`` top-level module.

.. autosummary::
    :toctree: api/
    :template: function.rst

    gmt.pscoast


Low-level wrappers for the GMT C API
------------------------------------

The GMT C API is accessed using ctypes_. The ``gmt.clib`` module offers
functions and classes that wrap the C API with a pythonic interface.

.. autosummary::
    :toctree: api/
    :template: function.rst

    gmt.clib.create_session
    gmt.clib.call_module
    gmt.clib.load_libgmt


.. _ctypes: https://docs.python.org/3/library/ctypes.html
