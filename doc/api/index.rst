API Reference
=============

This page gives an overview of all public PyGMT objects, functions and methods.

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
    Figure.choropleth
    Figure.coast
    Figure.colorbar
    Figure.directional_rose
    Figure.hlines
    Figure.inset
    Figure.legend
    Figure.logo
    Figure.magnetic_rose
    Figure.scalebar
    Figure.solar
    Figure.text
    Figure.timestamp
    Figure.vlines

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
    Figure.tilemap

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
    grdmix
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

    info
    grdinfo

Xarray Integration
------------------

.. autosummary::
    :toctree: generated

    GMTBackendEntrypoint
    GMTDataArrayAccessor

Class-style Parameters
----------------------

.. currentmodule:: pygmt.params

.. autosummary::
    :toctree: generated
    :template: autosummary/params.rst

    Box
    Pattern
    Position

Enums
-----

.. currentmodule:: pygmt.enums

.. autosummary::
    :toctree: generated
    :nosignatures:
    :template: autosummary/enums.rst

    GridRegistration
    GridType

.. currentmodule:: pygmt

Miscellaneous
-------------

.. autosummary::
    :toctree: generated

    which
    show_versions

Datasets
--------

PyGMT provides access to GMT's datasets through the :mod:`pygmt.datasets` module.
These functions will download the datasets automatically the first time they are used
and store them in GMT's user data directory.

.. autosummary::
    :toctree: generated

    datasets.list_sample_data
    datasets.load_black_marble
    datasets.load_blue_marble
    datasets.load_earth_age
    datasets.load_earth_deflection
    datasets.load_earth_dist
    datasets.load_earth_free_air_anomaly
    datasets.load_earth_geoid
    datasets.load_earth_magnetic_anomaly
    datasets.load_earth_mask
    datasets.load_earth_mean_dynamic_topography
    datasets.load_earth_mean_sea_surface
    datasets.load_earth_relief
    datasets.load_earth_vertical_gravity_gradient
    datasets.load_mars_relief
    datasets.load_mercury_relief
    datasets.load_moon_relief
    datasets.load_pluto_relief
    datasets.load_venus_relief
    datasets.load_sample_data

In addition, there is also a special function to load XYZ tile maps via
:doc:`contextily <contextily:index>` to be used as base maps.

.. autosummary::
    :toctree: generated

    datasets.load_tile_map

.. currentmodule:: pygmt

Exceptions
----------

All custom exceptions are derived from :class:`pygmt.exceptions.GMTError`.

.. autosummary::
    :toctree: generated

    exceptions.GMTError
    exceptions.GMTCLibError
    exceptions.GMTCLibNoSessionError
    exceptions.GMTCLibNotFoundError
    exceptions.GMTInvalidInput
    exceptions.GMTOSError
    exceptions.GMTParameterError
    exceptions.GMTTypeError
    exceptions.GMTValueError
    exceptions.GMTVersionError


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
*virtual files*. These methods are context managers that automate the conversion of
Python objects to and from GMT virtual files:

.. autosummary::
    :toctree: generated

    clib.Session.virtualfile_in
    clib.Session.virtualfile_out
    clib.Session.virtualfile_to_dataset
    clib.Session.virtualfile_to_raster

Low level access (these are mostly used by the :mod:`pygmt.clib` package):

.. autosummary::
    :toctree: generated

    clib.Session.create
    clib.Session.destroy
    clib.Session.__getitem__
    clib.Session.__enter__
    clib.Session.__exit__
    clib.Session.get_default
    clib.Session.get_common
    clib.Session.create_data
    clib.Session.put_matrix
    clib.Session.put_strings
    clib.Session.put_vector
    clib.Session.read_data
    clib.Session.write_data
    clib.Session.open_virtualfile
    clib.Session.read_virtualfile
    clib.Session.extract_region
    clib.Session.get_libgmt_func
    clib.Session.virtualfile_from_grid
    clib.Session.virtualfile_from_stringio
    clib.Session.virtualfile_from_matrix
    clib.Session.virtualfile_from_vectors
