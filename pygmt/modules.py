"""
Non-plot GMT modules.
"""
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    C="per_column",
    D="tiles",
    F="geographic",
    I="spacing",
    T="nearest_multiple",
    L="force_scan",
    M="minmax_pos",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence", D="sequence", I="sequence")
def grdinfo(grid, **kwargs):
    r"""
    Get information about a grid.

    Can read the grid from a file or given as an xarray.DataArray grid.

    Full option list at :gmt-docs:`grdinfo.html`

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
        This is the only required argument.
    {R}
    per_column : str or bool
        **n**\|\ **t**.
        Formats the report using tab-separated fields on a single line. The
        output is name *w e s n z0 z1 dx dy nx ny* [ *x0 y0 x1 y1* ]
        [ *med scale* ] [ *mean std rms* ] [ *n_nan* ] *registration gtype*.
        The data in brackets are outputted depending on the ``force_scan``
        and ``minmax_pos`` arguments. Use **t** to place file name at the end
        of the output record or, **n** or ``True`` to only output numerical
        columns. The registration is either 0 (gridline) or 1 (pixel), while
        gtype is either 0 (Cartesian) or 1 (geographic). The default value is
        ``False``. This cannot be called if ``geographic`` is also set.
    tiles : str or list
        *xoff*\ [/*yoff*][**+i**].
        Divide a single grid's domain (or the ``region`` domain, if no grid
        given) into tiles of size dx times dy (set via ``spacing``). You can
        specify overlap between tiles by appending *xoff*\ [/*yoff*]. If the
        single grid is given you may use the modifier **+i** to ignore tiles
        that have no data within each tile subregion. Default output is text
        region strings. Use ``per_column`` to instead report four columns with
        xmin xmax ymin ymax per tile, or use ``per_column="t"`` to also have
        the region string appended as trailing text.
    geographic : bool
        Report grid domain and x/y-increments in world mapping format
        The default value is ``False``. This cannot be called if
        ``per_column`` is also set.
    spacing : str or list
        *dx*\ [/*dy*]\|\ **b**\|\ **i**\|\ **r**.
        Report the min/max of the region to the nearest multiple of dx and dy,
        and output this in the form w/e/s/n (unless ``per_column`` is set). To
        report the actual grid region, append **r**. For a grid produced by
        the img supplement (a Cartesian Mercator grid), the exact geographic
        region is given with **i** (if not found then we return the actual
        grid region instead). If no argument is given then we report the grid
        increment in the form *xinc*\ [/*yinc*]. If **b** is given we write
        each grid's bounding box polygon instead. Finally, if ``tiles`` is in
        effect then *dx* and *dy* are the dimensions of the desired tiles.
    force_scan : int or str
        **0**\|\ **1**\|\ **2**\|\ **p**\|\ **a**.

        **0**\ : Report range of z after actually scanning the data, not just
        reporting what the header says.
        **1**\ : Report median and L1 scale of z (L1 scale = 1.4826 * Median
        Absolute Deviation (MAD)).
        **2**\ : Report mean, standard deviation, and root-mean-square (rms)
        of z.
        **p**\ : Report mode (LMS) and LMS scale of z.
        **a**\ : Include all of the above.
    minxmax_pos : bool
        Include the x/y values at the location of the minimum and maximum
        z-values.
    nearest_multiple : str
        [*dz*]\ [**+a**\ [*alpha*]]\ [**+s**].
        Determine min and max z-value. If *dz* is provided then we first round
        these values off to multiples of *dz*. To exclude the two tails of the
        distribution when determining the min and max you can add **+a** to
        set the *alpha* value (in percent): We then sort the grid, exclude the
        data in the 0.5*\ *alpha* and 100 - 0.5*\ *alpha* tails, and revise
        the min and max. To force a symmetrical range about zero, using
        minus/plus the max absolute value of the two extremes, append **+s**\ .
        We report the result via the text string *zmin/zmax* or *zmin/zmax/dz*
        (if *dz* was given) as expected by :meth:`pygmt.makecpt`.
    {V}

    Returns
    -------
    info : str
        A string with information about the grid.
    """
    kind = data_kind(grid, None, None)
    with GMTTempFile() as outfile:
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(grid)
            elif kind == "grid":
                file_context = lib.virtualfile_from_grid(grid)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))
            with file_context as infile:
                arg_str = " ".join(
                    [infile, build_arg_string(kwargs), "->" + outfile.name]
                )
                lib.call_module("grdinfo", arg_str)
        result = outfile.read()
    return result


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
