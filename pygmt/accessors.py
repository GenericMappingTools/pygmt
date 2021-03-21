"""
GMT accessor methods.
"""
import xarray as xr
from pygmt.exceptions import GMTInvalidInput
from pygmt.src.grdinfo import grdinfo


@xr.register_dataarray_accessor("gmt")
class GMTDataArrayAccessor:
    """
    This is the GMT extension for :class:`xarray.DataArray`.

    You can access various GMT specific metadata about your grid as follows:

    >>> from pygmt.datasets import load_earth_relief
    >>> # Use the global Earth relief grid with 1 degree spacing
    >>> grid = load_earth_relief(resolution="01d")

    >>> # See if grid uses Gridline (0) or Pixel (1) registration
    >>> grid.gmt.registration
    1
    >>> # See if grid uses Cartesian (0) or Geographic (1) coordinate system
    >>> grid.gmt.gtype
    1
    """

    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        try:
            self._source = self._obj.encoding["source"]  # filepath to NetCDF source
            # From the shortened summary information of `grdinfo`,
            # get grid registration in column 10, and grid type in column 11
            self._registration, self._gtype = map(
                int, grdinfo(self._source, per_column="n", o="10,11").split()
            )
        except KeyError:
            self._registration = 0  # Default to Gridline registration
            self._gtype = 0  # Default to Cartesian grid type

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
                f"Invalid grid registration value: {value}, should be a boolean of "
                "either 0 for Gridline registration or 1 for Pixel registration"
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
                f"Invalid coordinate system type: {value}, should be a boolean of "
                "either 0 for Cartesian or 1 for Geographic"
            )
