GMT Python
==========

**A Python interface for the Generic Mapping Tools C API.**

`Documentation <https://genericmappingtools.github.io/gmt-python/>`_ |
`GMT modern mode <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`_ |
`Design <https://genericmappingtools.github.io/gmt-python/design.html>`_ |
`Contribute <https://genericmappingtools.github.io/gmt-python/contribute.html>`_ |
`Contact <https://gitter.im/GenericMappingTools/gmt-python>`_

.. image:: http://img.shields.io/pypi/v/gmt-python.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/gmt-python
.. image:: http://img.shields.io/travis/GenericMappingTools/gmt-python/master.svg?style=flat-square
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
or send us a message on `our Gitter chatroom <https://gitter.im/GenericMappingTools/gmt-python>`__.

See the `documentation <https://genericmappingtools.github.io/gmt-python/>`__
for our design ideas, currently implemented features, how to contribute, and
more.


Goals
-----

* Provide access to GMT modules from Python using the GMT C API (no system
  calls).
* API design familiar for veteran GMT users (arguments ``R``,
  ``J``, etc) with more newbie-friendly alternatives/aliases
  (``region=[10, 20, -30, -10]``,  ``projection='M'``, etc).
* Input and output using Python native containers: numpy ``ndarray`` or pandas
  ``DataFrame`` for data tables and `xarray <http://xarray.pydata.org>`__
  ``Dataset`` for netCDF grids.
* Integration with the `Jupyter notebook <http://jupyter.org/>`__ to display
  plots and maps inline.
* Built around the new `GMT modern mode
  <http://gmt.soest.hawaii.edu/projects/gmt/wiki/Modernization>`__.


Working features and TODO
-------------------------

- [X] Initial package layout and base documentation
- [X] Call basic functions from the C API: ``GMT_Create_Session`` and
  ``GMT_Call_Module``
- [ ] Minimal working code (modules ``pscoast``, ``begin``, and ``end``)
  producing figure on disk from data on disk
- [X] Setup testing infrastructure for generated plots, possibly taking
  advantage of matplotlib's `pytest-mpl
  <https://github.com/matplotlib/pytest-mpl>`__
- [ ] Wrapper for ``GMT Open VirtualFile`` to allow passing data in memory to
  the modules
- [ ] Wrapper for ``GMT Read VirtualFile`` get data out of data processing
  modules
- [ ] Wrapper for ``GMT_DATA`` to pass in tabular data from numpy arrays
- [ ] Wrapper for ``GMT_GRID`` to pass in grids from xarray Datasets
- [ ] Implement ``GMTSession`` context manager (created by ``gmt.begin()``)
  that calls ``gmt.end()`` on exit.


License
-------

gmt-python is free software: you can redistribute it and/or modify it under the
terms of the **BSD 3-clause License**. A copy of this license is provided in
``LICENSE.txt``.
