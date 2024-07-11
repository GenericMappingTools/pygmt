"""
GMT accessor for :class:`xarray.DataArray`.
"""

from pathlib import Path

import xarray as xr
from pygmt.exceptions import GMTInvalidInput
from pygmt.src.grdinfo import grdinfo


@xr.register_dataarray_accessor("gmt")
class GMTDataArrayAccessor:
    """
    GMT accessor for :class:`xarray.DataArray`.

    The accessor extends :class:`xarray.DataArray` to store GMT-specific
    properties about grids, which are important for PyGMT to correctly process
    and plot the grids.

    Notes
    -----

    Due to the limitations of xarray accessors, the GMT accessors are created
    once per :class:`xarray.DataArray` instance. You may lose these
    GMT-specific properties when manipulating grids (e.g., arithmetic and slice
    operations) or when accessing a :class:`xarray.DataArray` from a
    :class:`xarray.Dataset`. In these cases, you need to manually set these
    properties before passing the grid to PyGMT.

    Examples
    --------

    For GMT's built-in remote datasets, these GMT-specific properties are
    automatically determined and you can access them as follows:

    >>> from pygmt.datasets import load_earth_relief
    >>> # Use the global Earth relief grid with 1 degree spacing
    >>> grid = load_earth_relief(resolution="01d", registration="pixel")
    >>> # See if grid uses Gridline (0) or Pixel (1) registration
    >>> grid.gmt.registration
    1
    >>> # See if grid uses Cartesian (0) or Geographic (1) coordinate system
    >>> grid.gmt.gtype
    1

    For :class:`xarray.DataArray` grids created by yourself, grid properties
    ``registration`` and ``gtype`` default to 0 (i.e., a gridline-registered,
    Cartesian grid). You need to set the correct properties before
    passing it to PyGMT functions:

    >>> import numpy as np
    >>> import pygmt
    >>> import xarray as xr
    >>> # create a DataArray in gridline coordinates of sin(lon) * cos(lat)
    >>> interval = 2.5
    >>> lat = np.arange(90, -90 - interval, -interval)
    >>> lon = np.arange(0, 360 + interval, interval)
    >>> longrid, latgrid = np.meshgrid(lon, lat)
    >>> data = np.sin(np.deg2rad(longrid)) * np.cos(np.deg2rad(latgrid))
    >>> grid = xr.DataArray(data, coords=[("latitude", lat), ("longitude", lon)])
    >>> # default to a gridline-registrated Cartesian grid
    >>> grid.gmt.registration, grid.gmt.gtype
    (0, 0)
    >>> # set it to a gridline-registered geographic grid
    >>> grid.gmt.registration = 0
    >>> grid.gmt.gtype = 1
    >>> grid.gmt.registration, grid.gmt.gtype
    (0, 1)

    Note that the accessors are created once per :class:`xarray.DataArray`
    instance, so you may lose these GMT-specific properties after manipulating
    your grid.

    Inplace assignment operators like ``*=`` don't create new instances, so the
    properties are still kept:

    >>> grid *= 2.0
    >>> grid.gmt.registration, grid.gmt.gtype
    (0, 1)

    Other grid operations (e.g., arithmetic or slice operations) create new
    instances, so the properties will be lost:

    >>> # grid2 is a slice of the original grid
    >>> grid2 = grid[0:30, 50:80]
    >>> # properties are reset to the default values for new instance
    >>> grid2.gmt.registration, grid2.gmt.gtype
    (0, 0)
    >>> # need to set these properties before passing the grid to PyGMT
    >>> grid2.gmt.registration = grid.gmt.registration
    >>> grid2.gmt.gtype = grid.gmt.gtype
    >>> grid2.gmt.registration, grid2.gmt.gtype
    (0, 1)

    Accessing a :class:`xarray.DataArray` from a :class:`xarray.Dataset` always
    creates new instances, so these properties are always lost. The workaround
    is to assign the :class:`xarray.DataArray` into a variable:

    >>> ds = xr.Dataset({"zval": grid})
    >>> ds.zval.gmt.registration, ds.zval.gmt.gtype
    (0, 0)
    >>> # manually set these properties won't work as expected
    >>> ds.zval.gmt.registration, ds.zval.gmt.gtype = 0, 1
    >>> ds.zval.gmt.registration, ds.zval.gmt.gtype
    (0, 0)
    >>> # workaround: assign the DataArray into a variable
    >>> zval = ds.zval
    >>> zval.gmt.registration, zval.gmt.gtype
    (0, 0)
    >>> zval.gmt.registration, zval.gmt.gtype = 0, 1
    >>> zval.gmt.registration, zval.gmt.gtype
    (0, 1)
    """

    def __init__(self, xarray_obj):
        self._obj = xarray_obj

        self._source = self._obj.encoding.get("source")
        if self._source is not None and Path(self._source).exists():
            try:
                # Get grid registration and grid type from the last two columns
                # of the shortened summary information of `grdinfo`.
                self._registration, self._gtype = map(
                    int, grdinfo(self._source, per_column="n").split()[-2:]
                )
            except ValueError:
                self._registration = 0  # Default to Gridline registration
                self._gtype = 0  # Default to Cartesian grid type
        else:
            self._registration = 0  # Default to Gridline registration
            self._gtype = 0  # Default to Cartesian grid type
        del self._source

    @property
    def registration(self):
        """
        Registration type of the grid, either 0 (Gridline) or 1 (Pixel).
        """
        return self._registration

    @registration.setter
    def registration(self, value):
        if value not in {0, 1}:
            raise GMTInvalidInput(
                f"Invalid grid registration value: {value}, should be either "
                "0 for Gridline registration or 1 for Pixel registration."
            )
        self._registration = value

    @property
    def gtype(self):
        """
        Coordinate system type of the grid, either 0 (Cartesian) or 1 (Geographic).
        """
        return self._gtype

    @gtype.setter
    def gtype(self, value):
        if value not in {0, 1}:
            raise GMTInvalidInput(
                f"Invalid coordinate system type: {value}, should be "
                "either 0 for Cartesian or 1 for Geographic."
            )
        self._gtype = value
