"""
Non-plot GMT modules.
"""
import numpy as np
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
@use_alias(V="verbose")
def grdinfo(grid, **kwargs):
    """
    Get information about a grid.

    Can read the grid from a file or given as an xarray.DataArray grid.

    Full option list at :gmt-docs:`grdinfo.html`

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.

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


@fmt_docstring
@use_alias(C="per_column", I="spacing", T="nearest_multiple", V="verbose")
def info(table, **kwargs):
    """
    Get information about data tables.

    Reads from files and finds the extreme values in each of the columns
    reported as min/max pairs. It recognizes NaNs and will print warnings if
    the number of columns vary from record to record. As an option, it will
    find the extent of the first two columns rounded up and down to the nearest
    multiple of the supplied increments given by *spacing*. Such output will be
    in a numpy.ndarray form ``[w, e, s, n]``, which can be used directly as the
    *region* argument for other modules (hence only dx and dy are needed). If
    the *per_column* option is combined with *spacing*, then the numpy.ndarray
    output will be rounded up/down for as many columns as there are increments
    provided in *spacing*. A similar option *nearest_multiple* option will
    provide a numpy.ndarray in the form of ``[zmin, zmax, dz]`` for makecpt.

    Full option list at :gmt-docs:`gmtinfo.html`

    {aliases}

    Parameters
    ----------
    table : str or np.ndarray or pandas.DataFrame or xarray.Dataset
        Pass in either a file name to an ASCII data table, a 1D/2D numpy array,
        a pandas dataframe, or an xarray dataset made up of 1D xarray.DataArray
        data variables.
    per_column : bool
        Report the min/max values per column in separate columns.
    spacing : str
        ``'[b|p|f|s]dx[/dy[/dz...]]'``.
        Report the min/max of the first n columns to the nearest multiple of
        the provided increments and output results in the form
        ``[w, e, s, n]``.
    nearest_multiple : str
        ``'dz[+ccol]'``
        Report the min/max of the first (0'th) column to the nearest multiple
        of dz and output this in the form ``[zmin, zmax, dz]``.

    {V}

    Returns
    -------
    output : np.ndarray or str
        Return type depends on whether any of the 'per_column', 'spacing', or
        'nearest_multiple' parameters are set.

        - np.ndarray if either of the above parameters are used.
        - str if none of the above parameters are used.
    """
    kind = data_kind(table)
    with Session() as lib:
        if kind == "file":
            file_context = dummy_context(table)
        elif kind == "matrix":
            try:
                # pandas.DataFrame and xarray.Dataset types
                arrays = [array for _, array in table.items()]
            except AttributeError:
                # Python lists, tuples, and numpy ndarray types
                arrays = np.atleast_2d(np.asanyarray(table).T)
            file_context = lib.virtualfile_from_vectors(*arrays)
        else:
            raise GMTInvalidInput(f"Unrecognized data type: {type(table)}")

        with GMTTempFile() as tmpfile:
            with file_context as fname:
                arg_str = " ".join(
                    [fname, build_arg_string(kwargs), "->" + tmpfile.name]
                )
                lib.call_module("info", arg_str)
            result = tmpfile.read()

        if any(arg in kwargs for arg in ["C", "I", "T"]):
            # Converts certain output types into a numpy array
            # instead of a raw string that is less useful.
            if result.startswith(("-R", "-T")):  # e.g. -R0/1/2/3 or -T0/9/1
                result = result[2:].replace("/", " ")
            result = np.loadtxt(result.splitlines())

        return result


@fmt_docstring
@use_alias(G="download", V="verbose")
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
    {V}

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
                int, grdinfo(self._source, C="n", o="10,11").split()
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
