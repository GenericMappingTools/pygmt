"""
GMT accessor for :class:`xarray.DataArray`.
"""

import contextlib
from pathlib import Path

import xarray as xr
from pygmt.enums import GridRegistration, GridType
from pygmt.exceptions import GMTInvalidInput
from pygmt.src import (
    dimfilter,
    grdclip,
    grdcut,
    grdfill,
    grdfilter,
    grdgradient,
    grdhisteq,
    grdinfo,
    grdproject,
    grdsample,
    grdtrack,
)


@xr.register_dataarray_accessor("gmt")
class GMTDataArrayAccessor:
    """
    GMT accessor for :class:`xarray.DataArray`.

    The *gmt* accessor extends :class:`xarray.DataArray` to store GMT-specific
    properties for grids and images, which are important for PyGMT to correctly process
    and plot them. The *gmt* accessor contains the following properties:

    - ``registration``: Grid registration type :class:`pygmt.enums.GridRegistration`.
    - ``gtype``: Grid coordinate system type :class:`pygmt.enums.GridType`.

    The *gmt* accessor also provides a set of grid-operation methods that enables
    applying GMT's grid processing functionalities directly to the current
    :class:`xarray.DataArray` object. See the summary table below for the list of
    available methods.

    Notes
    -----
    When accessed the first time, the *gmt* accessor will first be initialized to the
    default values (``GridRegistration.GRIDLINE`` and ``GridType.CARTESIAN``, i.e., a
    gridline-registered, Cartesian grid), and then the properties will be updated with
    the correct grid registration and type determined from the source encoding (i.e.,
    ``grid.encoding["source"]``), if it is available.

    Due to the limitations of xarray accessors, the *gmt* accessor is created once per
    :class:`xarray.DataArray` instance. Thus, the *gmt* accessor will be re-initialized
    in cases where the :class:`xarray.DataArray` is manipulated (e.g., arithmetic and
    slice operations) or when accessing a :class:`xarray.DataArray` from a
    :class:`xarray.Dataset`. In these cases, the GMT-specific properties will result in
    incorrect values if the source encoding is not defined or is dropped due to
    operations, and users need to manually set these properties again.

    Examples
    --------
    For grids loaded from a file (e.g., via :func:`xarray.load_dataarray`) and GMT's
    built-in remote datasets, the GMT-specific properties are automatically determined
    and you can access them as follows:

    >>> from pygmt.datasets import load_earth_relief
    >>> # Use the global Earth relief grid with 1 degree spacing
    >>> grid = load_earth_relief(resolution="01d", registration="pixel")
    >>> # See if grid uses Gridline or Pixel registration
    >>> grid.gmt.registration
    <GridRegistration.PIXEL: 1>
    >>> # See if grid is in Cartesian or Geographic coordinate system
    >>> grid.gmt.gtype
    <GridType.GEOGRAPHIC: 1>
    >>> grid.encoding["source"] is not None
    True

    Inplace assignment operators like ``*=`` don't create new instances, so the
    properties are still kept:

    >>> grid *= 2.0
    >>> grid.gmt.registration
    <GridRegistration.PIXEL: 1>
    >>> grid.gmt.gtype
    <GridType.GEOGRAPHIC: 1>

    Slice operation creates a new instance, but the source encoding is kept, so the
    properties are still kept:

    >>> grid_slice = grid[0:30, 50:80]
    >>> # grid source encoding is kept in slice operation
    >>> grid_slice.encoding["source"] is not None
    True
    >>> # properties are still kept
    >>> grid_slice.gmt.registration
    <GridRegistration.PIXEL: 1>
    >>> grid_slice.gmt.gtype
    <GridType.GEOGRAPHIC: 1>

    Other grid operations (e.g., arithmetic operations) create new instances and drop
    the source encoding, so the properties will be reset to the default values:

    >>> grid2 = grid * 2.0
    >>> # grid source encoding is dropped in arithmetic operation.
    >>> "source" in grid2.encoding
    False
    >>> # properties are reset to the default values
    >>> grid2.gmt.registration
    <GridRegistration.GRIDLINE: 0>
    >>> grid2.gmt.gtype
    <GridType.CARTESIAN: 0>
    >>> # Need to set these properties before passing the grid to PyGMT
    >>> grid2.gmt.registration = grid.gmt.registration
    >>> grid2.gmt.gtype = grid.gmt.gtype
    >>> grid2.gmt.registration
    <GridRegistration.PIXEL: 1>
    >>> grid2.gmt.gtype
    <GridType.GEOGRAPHIC: 1>

    For :class:`xarray.DataArray` grids created from scratch, the source encoding is not
    available, so the properties will be set to the default values, and you need to
    manually set the correct properties before passing it to PyGMT functions:

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

    Accessing a :class:`xarray.DataArray` from a :class:`xarray.Dataset` always creates
    new instances, so these properties are always lost if the source encoding is not
    available. The workaround is to assign the :class:`xarray.DataArray` into a
    variable:

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

    Instead of calling a grid-processing function and passing the
    :class:`xarray.DataArray` object as an input, you can call the corresponding method
    directly on the object. For example, the following two are equivalent:

    >>> from pygmt.datasets import load_earth_relief
    >>> grid = load_earth_relief(resolution="30m", region=[10, 30, 15, 25])
    >>> # Create a new grid from an input grid. Set all values below 1,000 to
    >>> # 0 and all values above 1,500 to 10,000.
    >>> # Option 1:
    >>> new_grid = pygmt.grdclip(grid=grid, below=[1000, 0], above=[1500, 10000])
    >>> # Option 2:
    >>> new_grid = grid.gmt.clip(below=[1000, 0], above=[1500, 10000])
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
                _registration, _gtype = map(
                    int, grdinfo(_source, per_column="n").split()[-2:]
                )
            self._registration = GridRegistration(_registration)
            self._gtype = GridType(_gtype)

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

    def dimfilter(self, **kwargs) -> xr.DataArray:
        """
        Directional filtering of a grid in the space domain.

        See the :func:`pygmt.dimfilter` function for available parameters.
        """
        return dimfilter(grid=self._obj, **kwargs)

    def clip(self, **kwargs) -> xr.DataArray:
        """
        Clip the range of grid values.

        See the :func:`pygmt.grdclip` function for available parameters.
        """
        return grdclip(grid=self._obj, **kwargs)

    def cut(self, **kwargs) -> xr.DataArray:
        """
        Extract subregion from a grid or image or a slice from a cube.

        See the :func:`pygmt.grdcut` function for available parameters.
        """
        return grdcut(grid=self._obj, **kwargs)

    def equalize_hist(self, **kwargs) -> xr.DataArray:
        """
        Perform histogram equalization for a grid.

        See the :meth:`pygmt.grdhisteq.equalize_grid` method for available parameters.
        """
        return grdhisteq.equalize_grid(grid=self._obj, **kwargs)

    def fill(self, **kwargs) -> xr.DataArray:
        """
        Interpolate across holes in the grid.

        See the :func:`pygmt.grdfill` function for available parameters.
        """
        return grdfill(grid=self._obj, **kwargs)

    def filter(self, **kwargs) -> xr.DataArray:
        """
        Filter a grid in the space (or time) domain.

        See the :func:`pygmt.grdfilter` function for available parameters.
        """
        return grdfilter(grid=self._obj, **kwargs)

    def gradient(self, **kwargs) -> xr.DataArray:
        """
        Compute directional gradients from a grid.

        See the :func:`pygmt.grdgradient` function for available parameters.
        """
        return grdgradient(grid=self._obj, **kwargs)

    def project(self, **kwargs) -> xr.DataArray:
        """
        Forward and inverse map transformation of grids.

        See the :func:`pygmt.grdproject` function for available parameters.
        """
        return grdproject(grid=self._obj, **kwargs)

    def sample(self, **kwargs) -> xr.DataArray:
        """
        Resample a grid onto a new lattice.

        See the :func:`pygmt.grdsample` function for available parameters.
        """
        return grdsample(grid=self._obj, **kwargs)

    def track(self, **kwargs) -> xr.DataArray:
        """
        Sample a grid at specified locations.

        See the :func:`pygmt.grdtrack` function for available parameters.
        """
        return grdtrack(grid=self._obj, **kwargs)
