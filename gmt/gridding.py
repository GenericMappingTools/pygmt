"""
GMT modules for Gridding of Data Tables
"""
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
@use_alias(I="spacing", R="region")
def surface(x=None, y=None, z=None, data=None, **kwargs):
    """
    Grids table data using adjustable tension continuous curvature splines

    Takes a matrix, (x,y,z) pairs, or a file name as input.

    Must provide either *data* or *x*, *y*, and *z*.

    {gmt_module_docs}

    Parameters
    ----------
    x, y, z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.

    spacing (I) :
        ``'xinc[unit][+e|n][/yinc[unit][+e|n]]'``.
        x_inc [and optionally y_inc] is the grid spacing.

    region (R) : str or list
        ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
        Specify the region of interest.

    {aliases}

    Returns
    -------
    array: xarray.DataArray
        The output grid as a DataArray
    """
    kind = data_kind(data, x, y, z)
    if kind == "vectors" and z is None:
        raise GMTInvalidInput("Must provide z with x and y.")

    with GMTTempFile(suffix=".nc") as outfile:
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
                kwargs.update({"G": outfile.name})
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module(module="surface", args=arg_str)
        result = xr.open_dataset(outfile)
    return result
