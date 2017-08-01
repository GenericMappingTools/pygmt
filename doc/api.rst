.. _api:

API Reference
=============

.. currentmodule:: gmt


Plotting
--------

All plotting in GMT/Python is handled by the ``gmt.Figure`` class.

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

The GMT C API is accessed using ctypes_. The ``gmt.clib`` package offers
functions and classes that wrap the C API with a pythonic interface.


Classes
+++++++

.. autosummary::
    :toctree: api/
    :template: class.rst

    clib.APISession

Functions
+++++++++

.. autosummary::
    :toctree: api/
    :template: function.rst

    clib.call_module
    clib.create_session
    clib.destroy_session
    clib.load_libgmt
    clib.get_constant


.. _ctypes: https://docs.python.org/3/library/ctypes.html
