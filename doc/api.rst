.. _api:

API Reference
=============

High-level functions for GMT modules
------------------------------------

Each GMT module (``gmt pscoast``, ``gmt psbasemap``, etc.) is wrapped by a
function in the ``gmt`` top-level module.

.. autosummary::
    :toctree: api/
    :template: function.rst

    gmt.figure
    gmt.show
    gmt.psbasemap
    gmt.pscoast
    gmt.psconvert
    gmt.psxy


Additional utility functions:

.. autosummary::
    :toctree: api/
    :template: function.rst

    gmt.test


Low-level wrappers for the GMT C API
------------------------------------

The GMT C API is accessed using ctypes_. The ``gmt.clib`` module offers
functions and classes that wrap the C API with a pythonic interface.

Functions
+++++++++

.. autosummary::
    :toctree: api/
    :template: function.rst

    gmt.clib.call_module
    gmt.clib.create_session
    gmt.clib.destroy_session
    gmt.clib.load_libgmt

Classes
+++++++

.. autosummary::
    :toctree: api/
    :template: function.rst

    gmt.clib.APISession


.. _ctypes: https://docs.python.org/3/library/ctypes.html
