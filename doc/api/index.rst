.. _api:

API Reference
=============

.. currentmodule:: gmt

Plotting
--------

All plotting is handled through the :class:`gmt.Figure` class and its methods.

.. autosummary::
    :toctree: generated

    Figure

Plotting data and laying out the map:

.. autosummary::
    :toctree: generated

    Figure.basemap
    Figure.coast
    Figure.plot
    Figure.contour
    Figure.grdcontour
    Figure.grdimage
    Figure.logo
    Figure.image

Saving and displaying the figure:

.. autosummary::
    :toctree: generated

    Figure.savefig
    Figure.show
    Figure.psconvert


Data Processing
---------------

Operations on tabular data:

.. autosummary::
    :toctree: generated

    info

Operations on grids:

.. autosummary::
    :toctree: generated

    grdinfo


Miscellaneous
-------------

.. autosummary::
    :toctree: generated

    which
    test
    print_clib_info


Datasets
--------

GMT/Python provides access to GMT's datasets through the :mod:`gmt.datasets` package.
These functions will download the datasets automatically the first time they are used
and store them in the GMT cache folder.

.. autosummary::
    :toctree: generated

    datasets.load_earth_relief
    datasets.load_usgs_quakes
    datasets.load_japan_quakes


Exceptions
----------

All custom exceptions are derived from :class:`gmt.exceptions.GMTError`.

.. autosummary::
    :toctree: generated

    exceptions.GMTError
    exceptions.GMTInvalidInput
    exceptions.GMTVersionError
    exceptions.GMTOSError
    exceptions.GMTCLibError
    exceptions.GMTCLibNoSessionError
    exceptions.GMTCLibNotFoundError


GMT C API
---------

The :mod:`gmt.clib` package is a wrapper for the GMT C API built using :mod:`ctypes`.
Most calls to the C API happen through the :class:`gmt.clib.Session` class.

.. autosummary::
    :toctree: generated

    clib.Session

`GMT modules <http://gmt.soest.hawaii.edu/doc/latest/#man-pages>`__ are executed through
the :meth:`~gmt.clib.Session.call_module` method:

.. autosummary::
    :toctree: generated

    clib.Session.call_module

Passing memory blocks between Python variables (:class:`numpy.ndarray`,
:class:`pandas.Series`, and :class:`xarray.DataArray`) and GMT happens through *virtual
files*. These methods are context managers that automate the conversion of Python
variables to GMT virtual files:

.. autosummary::
    :toctree: generated

    clib.Session.virtualfile_from_matrix
    clib.Session.virtualfile_from_vectors
    clib.Session.virtualfile_from_grid


Low level access (these are mostly used by the :mod:`gmt.clib` package):

.. autosummary::
    :toctree: generated

    clib.Session.create
    clib.Session.destroy
    clib.Session.__getitem__
    clib.Session.__enter__
    clib.Session.__exit__
    clib.Session.get_default
    clib.Session.create_data
    clib.Session.put_matrix
    clib.Session.put_vector
    clib.Session.write_data
    clib.Session.open_virtual_file
    clib.Session.extract_region
    clib.Session.get_libgmt_func
