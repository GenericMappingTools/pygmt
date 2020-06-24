"""
Non-plot GMT modules.
"""
import xarray as xr


from .clib import Session
from .helpers import (
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
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


@fmt_docstring
@use_alias(
    G="outgrid",
    R="region",
    J="projection",
    N="extend",
    S="circ_subregion",
    Z="z_subregion",
)
@kwargs_to_strings(R="sequence")
def grdcut(grid, **kwargs):
    """
    Extract subregion from a grid.

    Produce a new *outgrid* file which is a subregion of *grid*. The
    subregion is specified with *region*; the specified range must not exceed
    the range of *grid* (but see *extend*). If in doubt, run
    :meth:`pygmt.grdinfo` to check range. Alternatively, define the subregion
    indirectly via a range check on the node values or via distances from a
    given point. Finally, you can give *projection* for oblique projections to
    determine the corresponding rectangular *region* setting that will give a
    grid that fully covers the oblique domain.

    Full option list at :gmt-docs:`grdcut.html`

    {aliases}

    Parameters
    ----------
    grid : str
        The name of the input grid file.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {J}
    {R}
    extend : bool or int or float
        Allow grid to be extended if new *region* exceeds existing boundaries.
        Give a value to initialize nodes outside current region.
    circ_subregion : str
        ``'lon/lat/radius[unit][+n]'``.
        Specify an origin (*lon* and *lat*) and *radius*; append a distance
        *unit* and we determine the corresponding rectangular region so that
        all grid nodes on or inside the circle are contained in the subset.
        If **+n** is appended we set all nodes outside the circle to NaN.
    z_subregion :
        ``'[min/max][+n|N|r]'``.
        Determine a new rectangular region so that all nodes outside this
        region are also outside the given z-range [-inf/+inf]. To indicate no
        limit on *min* or *max* only, specify a hyphen (-). Normally, any NaNs
        encountered are simply skipped and not considered in the
        range-decision. Append **+n** to consider a NaN to be outside the given
        z-range. This means the new subset will be NaN-free. Alternatively,
        append **+r** to consider NaNs to be within the data range. In this
        case we stop shrinking the boundaries once a NaN is found [Default
        simply skips NaNs when making the range decision]. Finally, if your
        core subset grid is surrounded by rows and/or columns that are all
        NaNs, append **+N** to strip off such columns before (optionally)
        considering the range of the core subset for further reduction of the
        area.

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the *outgrid* parameter is set:

        - xarray.DataArray if *outgrid* is not set
        - None if *outgrid* is set (grid output will be stored in *outgrid*)
    """
    kind = data_kind(grid)

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(grid)
            elif kind == "grid":
                raise NotImplementedError(
                    "xarray.DataArray is not supported as the input grid yet!"
                )
                # file_context = lib.virtualfile_from_grid(grid)
                # See https://github.com/GenericMappingTools/gmt/pull/3532
                # for a feature request.
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))

            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdcut", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            result = xr.open_dataarray(outgrid)
        else:
            result = None  # if user sets an outgrid, return None

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
