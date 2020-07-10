"""
Non-plot GMT modules.
"""
# import logging
import xarray as xr

from .clib import Session
from .helpers import (
    build_arg_string,
    fmt_docstring,
    GMTTempFile,
    use_alias,
    data_kind,
    dummy_context,
)
from .exceptions import GMTInvalidInput


@fmt_docstring
def grdinfo(grid, **kwargs):
    """
    Get information about a grid.

    Can read the grid from a file or given as an xarray.DataArray grid.

    Full option list at :gmt-docs:`grdinfo.html`

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.

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


@fmt_docstring
@use_alias(C="per_column", I="spacing", T="nearest_multiple")
def info(fname, **kwargs):
    """
    Get information about data tables.

    Reads from files and finds the extreme values in each of the columns.
    It recognizes NaNs and will print warnings if the number of columns vary
    from record to record. As an option, it will find the extent of the first
    n columns rounded up and down to the nearest multiple of the supplied
    increments. By default, this output will be in the form *-Rw/e/s/n*,
    or the output will be in column form for as many columns as there are
    increments provided. The *nearest_multiple* option will provide a
    *-Tzmin/zmax/dz* string for makecpt.

    Full option list at :gmt-docs:`gmtinfo.html`

    {aliases}

    Parameters
    ----------
    fname : str
        The file name of the input data table file.
    per_column : bool
        Report the min/max values per column in separate columns.
    spacing : str
        ``'[b|p|f|s]dx[/dy[/dz...]]'``.
        Report the min/max of the first n columns to the nearest multiple of
        the provided increments and output results in the form *-Rw/e/s/n*
        (unless *per_column* is set).
    nearest_multiple : str
        ``'dz[+ccol]'``
        Report the min/max of the first (0'th) column to the nearest multiple
        of dz and output this as the string *-Tzmin/zmax/dz*.
    """
    if not isinstance(fname, str):
        raise GMTInvalidInput("'info' only accepts file names.")

    with GMTTempFile() as tmpfile:
        arg_str = " ".join([fname, build_arg_string(kwargs), "->" + tmpfile.name])
        with Session() as lib:
            lib.call_module("info", arg_str)
        return tmpfile.read()


@fmt_docstring
@use_alias(G="download")
def which(fname, **kwargs):
    """
    Find the full path to specified files.

    Reports the full paths to the files given through *fname*. We look for
    the file in (1) the current directory, (2) in $GMT_USERDIR (if defined),
    (3) in $GMT_DATADIR (if defined), or (4) in $GMT_CACHEDIR (if defined).

    *fname* can also be a downloadable file (either a full URL, a
    `@file` special file for downloading from the GMT Site Cache, or
    `@earth_relief_*` topography grids). In these cases, use option *download*
    to set the desired behavior. If *download* is not used (or False), the file
    will not be found.

    Full option list at :gmt-docs:`gmtwhich.html`

    {aliases}

    Parameters
    ----------
    fname : str
        The file name that you want to check.
    download : bool or str
        If the file is downloadable and not found, we will try to download the
        it. Use True or 'l' (default) to download to the current directory. Use
        'c' to place in the user cache directory or 'u' user data directory
        instead.

    Returns
    -------
    path : str
        The path of the file, depending on the options used.

    Raises
    ------
    FileNotFoundError
        If the file is not found.

    """
    with GMTTempFile() as tmpfile:
        arg_str = " ".join([fname, build_arg_string(kwargs), "->" + tmpfile.name])
        with Session() as lib:
            lib.call_module("which", arg_str)
        path = tmpfile.read().strip()
    if not path:
        raise FileNotFoundError("File '{}' not found.".format(fname))
    return path


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
    0
    >>> # See if grid uses Cartesian (0) or Geographic (1) coordinate system
    >>> grid.gmt.gtype
    1
    """

    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        try:
            self._source = self._obj.encoding["source"]
            self._info = grdinfo(self._source)
        except KeyError:
            default_reg_and_gtype = "Gridline node registration used [Cartesian grid]"
            # logging.warning(
            #    msg="Cannot find a NetCDF source for the xarray grid. "
            #    f"Will fallback to using GMT's default setting: {default_reg_and_gtype}"
            # )
            self._info = default_reg_and_gtype

    @property
    def registration(self):
        """
        Registration type of the grid, either Gridline (0) or Pixel (1).
        """
        try:
            return self._registration
        except AttributeError:
            if "Gridline node registration used" in self._info:
                self._registration = 0
            elif "Pixel node registration used" in self._info:
                self._registration = 1
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
        try:
            return self._gtype
        except AttributeError:
            if "[Cartesian grid]" in self._info:
                self._gtype = 0
            elif "[Geographic grid]" in self._info:
                self._gtype = 1
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
