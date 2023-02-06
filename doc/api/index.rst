.. _api:

API Reference
=============

.. automodule:: pygmt

.. currentmodule:: pygmt

Plotting
--------

Figure class overview
~~~~~~~~~~~~~~~~~~~~~

All plotting is handled through the :class:`pygmt.Figure` class and its methods.

.. autosummary::
    :toctree: generated

    Figure

Plotting map elements
~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    Figure.basemap
    Figure.coast
    Figure.colorbar
    Figure.inset
    Figure.legend
    Figure.logo
    Figure.solar
    Figure.text

Plotting tabular data
~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    Figure.contour
    Figure.histogram
    Figure.meca
    Figure.plot
    Figure.plot3d
    Figure.rose
    Figure.ternary
    Figure.velo
    Figure.wiggle

Plotting raster data
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    Figure.grdcontour
    Figure.grdimage
    Figure.grdview
    Figure.image

Configuring layout
~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    Figure.set_panel
    Figure.shift_origin
    Figure.subplot

Saving and displaying the figure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    Figure.savefig
    Figure.show
    Figure.psconvert

Configuring the display settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following function is provided directly through the :mod:`pygmt` top level
package.

.. autosummary::
    :toctree: generated

    set_display

Color palette table generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following functions are provided directly through the :mod:`pygmt` top level
package.

.. autosummary::
    :toctree: generated

    grd2cpt
    makecpt


Data Processing
---------------

Operations on tabular data
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    binstats
    blockmean
    blockmedian
    blockmode
    filter1d
    nearneighbor
    project
    select
    sph2grd
    sphdistance
    sphinterpolate
    surface
    triangulate
    triangulate.regular_grid
    triangulate.delaunay_triples
    xyz2grd

Operations on raster data
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    dimfilter
    grd2xyz
    grdclip
    grdcut
    grdfill
    grdfilter
    grdgradient
    grdhisteq
    grdhisteq.equalize_grid
    grdhisteq.compute_bins
    grdlandmask
    grdproject
    grdsample
    grdtrack
    grdvolume

Crossover analysis with x2sys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated

    x2sys_init
    x2sys_cross

Input/output
------------

.. autosummary::
    :toctree: generated

    load_dataarray

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

.. currentmodule:: pygmt

Datasets
--------

PyGMT provides access to GMT's datasets through the :mod:`pygmt.datasets` module.
These functions will download the datasets automatically the first time they are used
and store them in GMT's user data directory.

.. autosummary::
    :toctree: generated

    datasets.list_sample_data
    datasets.load_earth_age
    datasets.load_earth_free_air_anomaly
    datasets.load_earth_geoid
    datasets.load_earth_magnetic_anomaly
    datasets.load_earth_mask
    datasets.load_earth_relief
    datasets.load_earth_vertical_gravity_gradient
    datasets.load_sample_data


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


.. currentmodule:: pygmt

GMT C API
---------

The :mod:`pygmt.clib` package is a wrapper for the GMT C API built using :mod:`ctypes`.
Most calls to the C API happen through the :class:`pygmt.clib.Session` class.

.. autosummary::
    :toctree: generated

    clib.Session

:gmt-docs:`GMT modules <modules.html>` are executed through
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
    clib.Session.put_strings
    clib.Session.put_vector
    clib.Session.write_data
    clib.Session.open_virtual_file
    clib.Session.extract_region
    clib.Session.get_libgmt_func
