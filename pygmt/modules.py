"""
Non-plot GMT modules.
"""
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.src.grdinfo import grdinfo


class config:  # pylint: disable=invalid-name
    """
    Set GMT defaults globally or locally.

    Change GMT defaults globally::

        pygmt.config(PARAMETER=value)

    Change GMT defaults locally by using it as a context manager::

        with pygmt.config(PARAMETER=value):
            ...

    Full GMT defaults list at :gmt-docs:`gmt.conf.html`
    """

    def __init__(self, **kwargs):
        # Save values so that we can revert to their initial values
        self.old_defaults = {}
        self.special_params = {
            "FONT": [
                "FONT_ANNOT_PRIMARY",
                "FONT_ANNOT_SECONDARY",
                "FONT_HEADING",
                "FONT_LABEL",
                "FONT_TAG",
                "FONT_TITLE",
            ],
            "FONT_ANNOT": ["FONT_ANNOT_PRIMARY", "FONT_ANNOT_SECONDARY"],
            "FORMAT_TIME_MAP": ["FORMAT_TIME_PRIMARY_MAP", "FORMAT_TIME_SECONDARY_MAP"],
            "MAP_ANNOT_OFFSET": [
                "MAP_ANNOT_OFFSET_PRIMARY",
                "MAP_ANNOT_OFFSET_SECONDARY",
            ],
            "MAP_GRID_CROSS_SIZE": [
                "MAP_GRID_CROSS_SIZE_PRIMARY",
                "MAP_GRID_CROSS_SIZE_SECONDARY",
            ],
            "MAP_GRID_PEN": ["MAP_GRID_PEN_PRIMARY", "MAP_GRID_PEN_SECONDARY"],
            "MAP_TICK_LENGTH": ["MAP_TICK_LENGTH_PRIMARY", "MAP_TICK_LENGTH_SECONDARY"],
            "MAP_TICK_PEN": ["MAP_TICK_PEN_PRIMARY", "MAP_TICK_PEN_SECONDARY"],
        }
        with Session() as lib:
            for key in kwargs:
                if key in self.special_params:
                    for k in self.special_params[key]:
                        self.old_defaults[k] = lib.get_default(k)
                else:
                    self.old_defaults[key] = lib.get_default(key)

        # call gmt set to change GMT defaults
        arg_str = " ".join(
            ["{}={}".format(key, value) for key, value in kwargs.items()]
        )
        with Session() as lib:
            lib.call_module("set", arg_str)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # revert to initial values
        arg_str = " ".join(
            ["{}={}".format(key, value) for key, value in self.old_defaults.items()]
        )
        with Session() as lib:
            lib.call_module("set", arg_str)


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
