GMT Python
==================================

**A Python interface for the Generic Mapping Tools**


Warning
-------

**This package in early stages of design and implementation.**

We welcome any feedback and ideas!
Let us know by submitting
`issues on Github <https://github.com/GenericMappingTools/gmt-python/issues>`__.


Goals
-----

* Provide access to GMT modules from Python using the GMT C API (no system
  calls).
* Input and output using Python native containers: numpy ``ndarray`` or pandas
  ``DataFrame`` for data tables and `xarray <http://xarray.pydata.org>`__
  ``Dataset`` for netCDF grids.
* Integration with the `Jupyter notebook <http://jupyter.org/>`__ to display
  plots and maps inline.
* API design familiar for veteran GMT users (arguments ``R``,
  ``J``, etc) with more newbie-friendly alternatives/aliases
  (``region=[10, 20, -30, -10]``,  ``projection='M'``, etc).


Previous work
-------------

To my knowledge, there have been 3 attempts at a GMT Python interface:

* `gmtpy <https://github.com/emolch/gmtpy>`__ by
  `Sebastian Heimann <https://github.com/emolch>`__
* `pygmt <https://github.com/ian-r-rose/pygmt>`__ by
  `Ian Rose <https://github.com/ian-r-rose>`__
* `PyGMT <https://github.com/glimmer-cism/PyGMT>`__  by
  `Magnus Hagdorn <https://github.com/mhagdorn>`__

Only ``gmtpy`` has received commits since 2014 and is the more mature
alternative.
However, the project `doesn't seem to be very activate
<https://github.com/emolch/gmtpy/graphs/contributors>`__.
Both ``gmtpy`` and ``PyGMT`` use system class (through ``subprocess.Popen``)
and pass input and output through ``subprocess.PIPE``.
``pygmt`` seems to call the GMT C API directly through a hand-coded Python C
extension.
This might compromise the portability of the package across operating systems
and makes distribution very painful.

.. toctree::
    :maxdepth: 2
    :hidden:

    install.rst
    api.rst
    license.rst
