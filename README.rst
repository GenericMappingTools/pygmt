GMT/Python
==========

**A Python interface for the Generic Mapping Tools C API.**

`Documentation <https://genericmappingtools.github.io/gmt-python/>`_ |
`Install <https://genericmappingtools.github.io/gmt-python/install.html>`_ |
`First steps <https://genericmappingtools.github.io/gmt-python/first-steps.html>`_ |
`GMT modern mode <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`_ |
`Design <https://genericmappingtools.github.io/gmt-python/design.html>`_ |
`Contact <https://gitter.im/GenericMappingTools/gmt-python>`_

.. image:: http://img.shields.io/pypi/v/gmt-python.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/gmt-python
.. image:: http://img.shields.io/travis/GenericMappingTools/gmt-python/master.svg?style=flat-square&label=linux|osx
    :alt: Travis CI build status
    :target: https://travis-ci.org/GenericMappingTools/gmt-python
.. image:: http://img.shields.io/coveralls/GenericMappingTools/gmt-python/master.svg?style=flat-square
    :alt: Test coverage status
    :target: https://coveralls.io/r/GenericMappingTools/gmt-python?branch=master
.. image:: https://img.shields.io/pypi/pyversions/gmt-python.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.python.org/pypi/gmt-python
.. image:: https://img.shields.io/gitter/room/GenericMappingTools/gmt-python.svg?style=flat-square
    :alt: Chat room on Gitter
    :target: https://gitter.im/GenericMappingTools/gmt-python


Disclaimer
----------

**This package in early stages of design and implementation.**

We welcome any feedback and ideas!
Let us know by submitting
`issues on Github <https://github.com/GenericMappingTools/gmt-python/issues>`__
or send us a message on our
`Gitter chatroom <https://gitter.im/GenericMappingTools/gmt-python>`__.

See the `documentation <https://genericmappingtools.github.io/gmt-python/>`__
for our design ideas, currently implemented features, how to contribute, and
more.


Getting started
---------------

1. `Install <https://genericmappingtools.github.io/gmt-python/install.html>`__
   (tested and working on Linux and OSX)
2. Follow the
   `First steps <https://genericmappingtools.github.io/gmt-python/first-steps.html>`__
   tutorial Jupyter notebook.
3. Take a look at the :ref:`api` for a list of modules that are already
   available.


Project goals
-------------

* Build a modern Pythonic API that appeals to Python programmers who want to
  use GMT.
* Implement readable and explicit aliases for the GMT command-line arguments
  (``region`` instead of ``R``, ``projection`` instead of ``J``, etc).
* Use the new `GMT modern mode
  <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__ for
  simplified execution and figure generation.
* Interface with the GMT C API directly using
  `ctypes <https://docs.python.org/3/library/ctypes.html>`__ (no system calls).
* Integration with the `Jupyter notebook <http://jupyter.org/>`__ to display
  plots and maps inline.
* Input and output using Python native containers: numpy ``ndarray`` or pandas
  ``DataFrame`` for data tables and `xarray <http://xarray.pydata.org>`__
  ``Dataset`` for netCDF grids.



Working features and TODO
-------------------------

- [X] Initial package layout and base documentation
- [X] Call basic functions from the C API: ``GMT_Create_Session``,
  ``GMT_Destroy_Session``, and ``GMT_Call_Module``
- [X] Setup testing infrastructure for generated plots, possibly taking
  advantage of matplotlib's `pytest-mpl
  <https://github.com/matplotlib/pytest-mpl>`__
- [X] Wrappers for basic session management functions (``begin``, ``end``, and
  ``figure``).
- [X] Implement a global modern mode session that starts at import time and is
  destroyed when the program ends. This eliminates the need for ``begin`` and
  ``end`` in the Python API.
- [X] Minimal working code producing a figure from data on disk
- [ ] Implement an object-oriented API using a ``Figure`` class (similar to
  matplotlib).
- [ ] Wrapper for the GMT VirtualFile machinery to allow communicating data in
  memory to the modules
- [ ] Wrapper for ``GMT_DATA`` to pass in tabular data from numpy arrays
- [ ] Wrapper for ``GMT_GRID`` to pass in grids from xarray Datasets


License
-------

gmt-python is free software: you can redistribute it and/or modify it under the
terms of the **BSD 3-clause License**. A copy of this license is provided in
``LICENSE.txt``.
