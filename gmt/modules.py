"""
Non-plot GMT modules.
"""
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

    {gmt_module_docs}

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
def info(fname, **kwargs):
    """
    Get information about data tables.

    Reads from files and finds the extreme values in each of the columns.
    It recognizes NaNs and will print warnings if the number of columns vary
    from record to record. As an option, it will find the extent of the first
    n columns rounded up and down to the nearest multiple of the supplied
    increments. By default, this output will be in the form *-Rw/e/s/n*,
    or the output will be in column form for as many columns as there are
    increments provided. The *T* option will provide a *-Tzmin/zmax/dz* string
    for makecpt.

    {gmt_module_docs}

    Parameters
    ----------
    fname : str
        The file name of the input data table file.
    C : bool
        Report the min/max values per column in separate columns.
    I : str
        ``'[b|p|f|s]dx[/dy[/dz...]]'``.
        Report the min/max of the first n columns to the nearest multiple of
        the provided increments and output results in the form *-Rw/e/s/n*
        (unless *C* is set).
    T : str
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

    {gmt_module_docs}

    {aliases}

    Parameters
    ----------
    fname : str
        The file name that you want to check.
    G : bool or str
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
