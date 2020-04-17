"""
GMT modules for Gridding of Data Tables
"""
import xarray as xr

from .clib import Session
from .helpers import (
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    GMTTempFile,
    kwargs_to_strings,
    use_alias,
)
from .exceptions import GMTInvalidInput


@fmt_docstring
@use_alias(I="spacing", R="region", G="outfile")
@kwargs_to_strings(R="sequence")
def surface(x=None, y=None, z=None, data=None, **kwargs):
    """
    Grids table data using adjustable tension continuous curvature splines.

    Surface reads randomly-spaced (x,y,z) triples and produces gridded values
    z(x,y) by solving:

        (1 - T) * L (L (z)) + T * L (z) = 0

    where T is a tension factor between 0 and 1, and L indicates the Laplacian
    operator.

    Takes a matrix, xyz triples, or a file name as input.

    Must provide either *data* or *x*, *y*, and *z*.

    Full option list at :gmt-docs:`surface.html`

    {aliases}

    Parameters
    ----------
    x, y, z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.

    spacing (I) : str
        ``'xinc[unit][+e|n][/yinc[unit][+e|n]]'``.
        x_inc [and optionally y_inc] is the grid spacing.

    region (R) : str or list
        ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
        Specify the region of interest.

    outfile (G) : str
        Optional. The file name for the output netcdf file with extension .nc
        to store the grid in.

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the outfile (G) parameter is set:

        - xarray.DataArray if outfile (G) is not set
        - None if outfile (G) is set (grid output will be stored in outfile)
    """
    kind = data_kind(data, x, y, z)
    if kind == "vectors" and z is None:
        raise GMTInvalidInput("Must provide z with x and y.")

    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(data)
            elif kind == "matrix":
                file_context = lib.virtualfile_from_matrix(data)
            elif kind == "vectors":
                file_context = lib.virtualfile_from_vectors(x, y, z)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(data)))
            with file_context as infile:
                if "G" not in kwargs.keys():  # if outfile is unset, output to tmpfile
                    kwargs.update({"G": tmpfile.name})
                outfile = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module(module="surface", args=arg_str)

        if outfile == tmpfile.name:  # if user did not set outfile, return DataArray
            with xr.open_dataarray(outfile) as dataarray:
                result = dataarray.load()
        elif outfile != tmpfile.name:  # if user sets an outfile, return None
            result = None

    return result
