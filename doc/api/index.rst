.. _api:

API Reference
=============

.. automodule:: pygmt

.. currentmodule:: pygmt

Plotting
--------

All plotting is handled through the :class:`pygmt.Figure` class and its methods.

.. autosummary::
    :toctree: generated

    Figure

Plotting data and laying out the map:

.. autosummary::
    :toctree: generated

    Figure.basemap
    Figure.coast
    Figure.colorbar
    Figure.contour
    Figure.grdcontour
    Figure.grdimage
    Figure.grdview
    Figure.image
    Figure.inset
    Figure.legend
    Figure.logo
    Figure.meca
    Figure.plot
    Figure.plot3d
    Figure.set_panel
    Figure.shift_origin
    Figure.solar
    Figure.subplot
    Figure.text

Color palette table generation:

.. autosummary::
    :toctree: generated

    grd2cpt
    makecpt

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

    blockmean
    blockmedian
    surface

Operations on grids:

.. autosummary::
    :toctree: generated

    grdcut
    grdfilter
    grdtrack

Crossover analysis with x2sys:

.. autosummary::
    :toctree: generated

    x2sys_init
    x2sys_cross

GMT Defaults
------------

Operations on GMT defaults:

.. autosummary::
    :toctree: generated

    config

Metadata
--------

Getting metadata from tabular or grid data:

.. autosummary::
    :toctree: generated

    GMTDataArrayAccessor
    info
    grdinfo


Miscellaneous
-------------

.. autosummary::
    :toctree: generated

    which
    test
    print_clib_info
    show_versions


.. automodule:: pygmt.datasets

.. currentmodule:: pygmt

Datasets
--------

PyGMT provides access to GMT's datasets through the :mod:`pygmt.datasets` package.
These functions will download the datasets automatically the first time they are used
and store them in the GMT cache folder.

.. autosummary::
    :toctree: generated

    datasets.load_earth_relief
    datasets.load_japan_quakes
    datasets.load_ocean_ridge_points
    datasets.load_sample_bathymetry
    datasets.load_usgs_quakes
    datasets.load_fractures_compilation

.. automodule:: pygmt.exceptions

.. currentmodule:: pygmt

Exceptions
----------

All custom exceptions are derived from :class:`pygmt.exceptions.GMTError`.

.. autosummary::
    :toctree: generated

    exceptions.GMTError
    exceptions.GMTInvalidInput
    exceptions.GMTVersionError
    exceptions.GMTOSError
    exceptions.GMTCLibError
    exceptions.GMTCLibNoSessionError
    exceptions.GMTCLibNotFoundError


.. automodule:: pygmt.clib

.. currentmodule:: pygmt

GMT C API
---------

The :mod:`pygmt.clib` package is a wrapper for the GMT C API built using :mod:`ctypes`.
Most calls to the C API happen through the :class:`pygmt.clib.Session` class.

.. autosummary::
    :toctree: generated

    clib.Session

`GMT modules <https://docs.generic-mapping-tools.org/latest/modules.html>`__ are executed through
the :meth:`~pygmt.clib.Session.call_module` method:

.. autosummary::
    :toctree: generated

    clib.Session.call_module

Passing memory blocks between Python data objects (e.g. :class:`numpy.ndarray`,
:class:`pandas.Series`, :class:`xarray.DataArray`, etc) and GMT happens through
*virtual files*. These methods are context managers that automate the
conversion of Python variables to GMT virtual files:

.. autosummary::
    :toctree: generated

    clib.Session.virtualfile_from_data
    clib.Session.virtualfile_from_matrix
    clib.Session.virtualfile_from_vectors
    clib.Session.virtualfile_from_grid


Low level access (these are mostly used by the :mod:`pygmt.clib` package):

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
