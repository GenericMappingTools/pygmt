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
    Figure.grdimage
    Figure.logo

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
    print_libgmt_info


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

The :mod:`gmt.clib` package is a wrapper for the GMT C API built using
`ctypes <https://docs.python.org/3/library/ctypes.html>`__.
Most calls to the C API happen through the :class:`gmt.clib.LibGMT` class.

.. autosummary::
    :toctree: generated

    clib.LibGMT

Main methods (this is what the rest of the library uses):

.. autosummary::
    :toctree: generated

    clib.LibGMT.call_module
    clib.LibGMT.grid_to_vfile
    clib.LibGMT.vectors_to_vfile
    clib.LibGMT.matrix_to_vfile
    clib.LibGMT.extract_region

Low level access (these are mostly used by the :mod:`gmt.clib` package):

.. autosummary::
    :toctree: generated

    clib.LibGMT.create_session
    clib.LibGMT.destroy_session
    clib.LibGMT.get_constant
    clib.LibGMT.get_default
    clib.LibGMT.create_data
    clib.LibGMT.open_virtual_file
    clib.LibGMT.put_matrix
    clib.LibGMT.put_vector
    clib.LibGMT.write_data
