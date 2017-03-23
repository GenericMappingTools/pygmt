gmt-python: Bringing GMT to the Python world
============================================

**A `ctypes`-based Python interface for the Generic Mapping Tools C API.**

.. image:: http://img.shields.io/pypi/v/gmt-python.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/gmt-python
.. image:: http://img.shields.io/travis/GenericMappingTools/gmt-python/master.svg?style=flat-square
    :alt: Travis CI build status
    :target: https://travis-ci.org/GenericMappingTools/gmt-python
.. image:: http://img.shields.io/coveralls/GenericMappingTools/gmt-python/master.svg?style=flat-square
    :alt: Test coverage status
    :target: https://coveralls.io/r/GenericMappingTools/gmt-python?branch=master


Warning
-------

**This package in very early stages of design.**

We welcome feedback and ideas through
`Github issues <https://github.com/GenericMappingTools/gmt-python/issues>`__.


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



Package design
--------------

``gmt-python`` is made for the future. We will support **only Python 3.5 or
later** and require the `new "modern" mode of GMT <http://gmt.soest.hawaii.edu/boards/2/topics/4930>`__
(currently only in ``trunk`` of SVN repository).
The ``modern`` mode removes the need for ``-O -K`` and explicitly redirecting
to a ``.ps`` file.
This all happens in the background.
A final call to ``gmt psconvert`` brings the plot out of hiding and finalizes
the Postscript.


The Python API
++++++++++++++

Each GMT module has a function in the ``gmt`` package.
Command-line arguments are passes as function keyword arguments.
Data can be passed as file names or in-memory data.
Calling ``gmt.show()`` gets a PNG image back and embeds it in the
Jupyter notebook.

Example usage::

    import numpy as np
    import gmt

    data = np.loadtxt('data_file.csv')

    cpt = gmt.makecpt(C="red,green,blue", T="0,70,300,10000")
    gmt.pscoast(R='g', J='N180/10i', G='bisque', S='azure1', B='af', X='c')
    gmt.psxy(input=data, S='ci', C=cpt, h='i1', i='2,1,3,4+s0.02')
    gmt.show(dpi=600)


Package organization
++++++++++++++++++++

General layout of the Python package::


    gmt/
        core/  # Package with low-level wrappers for the C API

        modules/  # Defines the functions corresponding to GMT modules


Internals
+++++++++

Use GMT_Open_Virtual_File for input and output.
Get ``kwarg`` dict and transform into the command-line string.
Pass all that to the ctypes-wrapped GMT API function.
Convert output back to Python.
Return.
