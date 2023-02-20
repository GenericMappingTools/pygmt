"""
GMT accessor methods.
"""
from pathlib import Path

import xarray as xr
from pygmt.exceptions import GMTInvalidInput
from pygmt.src.grdinfo import grdinfo


@xr.register_dataarray_accessor("gmt")
class GMTDataArrayAccessor:
    """
    GMT extension for :class:`xarray.DataArray`.

    The extension provides easy ways to access and change the GMT specific
    properties about grids. Currently, two properties are available:

    - ``registration``: Gridline (0) or Pixel (1) registration
    - ``gtype``: Cartesian (0) or Geographic (1) coordinate system

    You can access these GMT specific properties about your grid as follows:

    >>> from pygmt.datasets import load_earth_relief
    >>> # Use the global Earth relief grid with 1 degree spacing
    >>> grid = load_earth_relief(resolution="01d", registration="pixel")
    >>> # See if grid uses Gridline (0) or Pixel (1) registration
    >>> grid.gmt.registration
    1
    >>> # See if grid uses Cartesian (0) or Geographic (1) coordinate system
    >>> grid.gmt.gtype
    1

    You can also set the GMT specific properties for grids created by yourself:

    >>> import numpy as np
    >>> import pygmt
    >>> import xarray as xr
    >>> # create a DataArray in gridline coordinates of sin(lon) * cos(lat)
    >>> interval = 2.5
    >>> lat = np.arange(90, -90 - interval, -interval)
    >>> lon = np.arange(0, 360 + interval, interval)
    >>> longrid, latgrid = np.meshgrid(lon, lat)
    >>> data = np.sin(np.deg2rad(longrid)) * np.cos(np.deg2rad(latgrid))
    >>> grid = xr.DataArray(
    ...     data, coords=[("latitude", lat), ("longitude", lon)]
    ... )
    >>> # set it to a gridline-registered geographic grid
    >>> grid.gmt.registration = 0
    >>> grid.gmt.gtype = 1
    """

    def __init__(self, xarray_obj):
        self._obj = xarray_obj

        self._source = self._obj.encoding.get("source")
        if self._source is not None and Path(self._source).exists():
            try:
                # Get grid registration and grid type from the last two columns of
                # the shortened summary information of `grdinfo`.
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
        Registration type of the grid, either Gridline (0) or Pixel (1).
        """
        return self._registration

    @registration.setter
    def registration(self, value):
        if value in (0, 1):
            self._registration = value
        else:
            raise GMTInvalidInput(
                f"Invalid grid registration value: {value}, should be either "
                "0 for Gridline registration or 1 for Pixel registration."
            )

    @property
    def gtype(self):
        """
        Coordinate system type of the grid, either Cartesian (0) or Geographic
        (1).
        """
        return self._gtype

    @gtype.setter
    def gtype(self, value):
        if value in (0, 1):
            self._gtype = value
        else:
            raise GMTInvalidInput(
                f"Invalid coordinate system type: {value}, should be "
                "either 0 for Cartesian or 1 for Geographic."
            )
