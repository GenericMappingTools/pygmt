"""
GMT accessor for :class:`xarray.DataArray`.
"""

import contextlib
from pathlib import Path

import xarray as xr
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTInvalidInput
from pygmt.src.grdinfo import grdinfo


@xr.register_dataarray_accessor("gmt")
class GMTDataArrayAccessor:
    """
    GMT accessor for :class:`xarray.DataArray`.

    The *gmt* accessor extends :class:`xarray.DataArray` to store GMT-specific
    properties for grids, which are important for PyGMT to correctly process and plot
    the grids. The *gmt* accessor contains the following properties:

    - ``registration``: Grid registration type :class:`pygmt.enums.GridRegistration`.
    - ``gtype``: Grid coordinate system type :class:`pygmt.enums.GridType`.

    Examples
    --------
    For GMT's built-in remote datasets, these GMT-specific properties are automatically
    determined and you can access them as follows:

    >>> from pygmt.datasets import load_earth_relief
    >>> # Use the global Earth relief grid with 1 degree spacing
    >>> grid = load_earth_relief(resolution="01d", registration="pixel")
    >>> # See if grid uses Gridline or Pixel registration
    >>> grid.gmt.registration
    <GridRegistration.PIXEL: 1>
    >>> # See if grid is in Cartesian or Geographic coordinate system
    >>> grid.gmt.gtype
    <GridType.GEOGRAPHIC: 1>

    For :class:`xarray.DataArray` grids created by yourself, ``registration`` and
    ``gtype`` default to ``GridRegistration.GRIDLINE`` and ``GridType.CARTESIAN`` (i.e.,
    a gridline-registered, Cartesian grid). You need to set the correct properties
    before passing it to PyGMT functions:

    >>> import numpy as np
    >>> import xarray as xr
    >>> import pygmt
    >>> from pygmt.enums import GridRegistration, GridType
    >>> # Create a DataArray in gridline coordinates of sin(lon) * cos(lat)
    >>> interval = 2.5
    >>> lat = np.arange(90, -90 - interval, -interval)
    >>> lon = np.arange(0, 360 + interval, interval)
    >>> longrid, latgrid = np.meshgrid(lon, lat)
    >>> data = np.sin(np.deg2rad(longrid)) * np.cos(np.deg2rad(latgrid))
    >>> grid = xr.DataArray(data, coords=[("latitude", lat), ("longitude", lon)])
    >>> # Default to a gridline-registered Cartesian grid
    >>> grid.gmt.registration
    <GridRegistration.GRIDLINE: 0>
    >>> grid.gmt.gtype
    <GridType.CARTESIAN: 0>
    >>> # Manually set it to a gridline-registered geographic grid
    >>> grid.gmt.registration = GridRegistration.GRIDLINE
    >>> grid.gmt.gtype = GridType.GEOGRAPHIC
    >>> grid.gmt.registration
    <GridRegistration.GRIDLINE: 0>
    >>> grid.gmt.gtype
    <GridType.GEOGRAPHIC: 1>

    Notes
    -----
    Due to the limitations of xarray accessors, the GMT accessors are created once per
    :class:`xarray.DataArray` instance. You may lose these GMT-specific properties when
    manipulating grids (e.g., arithmetic and slice operations) or when accessing a
    :class:`xarray.DataArray` from a :class:`xarray.Dataset`. In these cases, you need
    to manually set these properties before passing the grid to PyGMT.

    Inplace assignment operators like ``*=`` don't create new instances, so the
    properties are still kept:

    >>> grid *= 2.0
    >>> grid.gmt.registration
    <GridRegistration.GRIDLINE: 0>
    >>> grid.gmt.gtype
    <GridType.GEOGRAPHIC: 1>

    Other grid operations (e.g., arithmetic or slice operations) create new instances,
    so the properties will be lost:

    >>> # grid2 is a slice of the original grid
    >>> grid2 = grid[0:30, 50:80]
    >>> # Properties are reset to the default values for new instance
    >>> grid2.gmt.registration
    <GridRegistration.GRIDLINE: 0>
    >>> grid2.gmt.gtype
    <GridType.CARTESIAN: 0>
    >>> # Need to set these properties before passing the grid to PyGMT
    >>> grid2.gmt.registration = grid.gmt.registration
    >>> grid2.gmt.gtype = grid.gmt.gtype
    >>> grid2.gmt.registration
    <GridRegistration.GRIDLINE: 0>
    >>> grid2.gmt.gtype
    <GridType.GEOGRAPHIC: 1>

    Accessing a :class:`xarray.DataArray` from a :class:`xarray.Dataset` always creates
    new instances, so these properties are always lost. The workaround is to assign the
    :class:`xarray.DataArray` into a variable:

    >>> ds = xr.Dataset({"zval": grid})
    >>> ds.zval.gmt.registration
    <GridRegistration.GRIDLINE: 0>
    >>> ds.zval.gmt.gtype
    <GridType.CARTESIAN: 0>
    >>> # Manually set these properties won't work as expected
    >>> ds.zval.gmt.registration = GridRegistration.GRIDLINE
    >>> ds.zval.gmt.gtype = GridType.GEOGRAPHIC
    >>> ds.zval.gmt.registration, ds.zval.gmt.gtype
    (<GridRegistration.GRIDLINE: 0>, <GridType.CARTESIAN: 0>)
    >>> # workaround: assign the DataArray into a variable
    >>> zval = ds.zval
    >>> zval.gmt.registration, zval.gmt.gtype
    (<GridRegistration.GRIDLINE: 0>, <GridType.CARTESIAN: 0>)
    >>> zval.gmt.registration = GridRegistration.GRIDLINE
    >>> zval.gmt.gtype = GridType.GEOGRAPHIC
    >>> zval.gmt.registration, zval.gmt.gtype
    (<GridRegistration.GRIDLINE: 0>, <GridType.GEOGRAPHIC: 1>)
    """

    def __init__(self, xarray_obj: xr.DataArray):
        self._obj = xarray_obj

        # Default to Gridline registration and Cartesian grid type
        self._registration = GridRegistration.GRIDLINE
        self._gtype = GridType.CARTESIAN

        # If the source file exists, get grid registration and grid type from the last
        # two columns of the shortened summary information of grdinfo.
        if (_source := self._obj.encoding.get("source")) and Path(_source).exists():
            with contextlib.suppress(ValueError):
                self._registration, self._gtype = map(  # type: ignore[assignment]
                    int, grdinfo(_source, per_column="n").split()[-2:]
                )

    @property
    def registration(self) -> GridRegistration:
        """
        Grid registration type :class:`pygmt.enums.GridRegistration`.
        """
        return self._registration

    @registration.setter
    def registration(self, value: GridRegistration | int):
        # TODO(Python>=3.12): Simplify to `if value not in GridRegistration`.
        if value not in GridRegistration.__members__.values():
            msg = (
                f"Invalid grid registration: '{value}'. Should be either "
                "GridRegistration.GRIDLINE (0) or GridRegistration.PIXEL (1)."
            )
            raise GMTInvalidInput(msg)
        self._registration = GridRegistration(value)

    @property
    def gtype(self) -> GridType:
        """
        Grid coordinate system type :class:`pygmt.enums.GridType`.
        """
        return self._gtype

    @gtype.setter
    def gtype(self, value: GridType | int):
        # TODO(Python>=3.12): Simplify to `if value not in GridType`.
        if value not in GridType.__members__.values():
            msg = (
                f"Invalid grid coordinate system type: '{value}'. "
                "Should be either GridType.CARTESIAN (0) or GridType.GEOGRAPHIC (1)."
            )
            raise GMTInvalidInput(msg)
        self._gtype = GridType(value)
