"""
GMT modules for Gridding of Data Tables
"""
import pandas as pd
import xarray as xr

from .clib import Session
from .exceptions import GMTInvalidInput
from .helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(I="spacing", R="region", G="outfile", V="verbose")
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
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.

    spacing : str
        ``'xinc[unit][+e|n][/yinc[unit][+e|n]]'``.
        x_inc [and optionally y_inc] is the grid spacing.

    region : str or list
        ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
        Specify the region of interest.

    outfile : str
        Optional. The file name for the output netcdf file with extension .nc
        to store the grid in.

    {V}

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
                _ = result.gmt  # load GMTDataArray accessor information
        elif outfile != tmpfile.name:  # if user sets an outfile, return None
            result = None

    return result


@fmt_docstring
@use_alias(
    G="outgrid", I="spacing", J="projection", R="region", V="verbose", r="registration"
)
@kwargs_to_strings(R="sequence")
def triangulate(x=None, y=None, z=None, data=None, **kwargs):
    """
    Delaunay triangulation or Voronoi partitioning and gridding of Cartesian
    data.

    Triangulate reads in x,y[,z] data and performs Delaunay triangulation,
    i.e., it find how the points should be connected to give the most
    equilateral triangulation possible. If a map projection (give *region*
    and *projection*) is chosen then it is applied before the triangulation
    is calculated.

    Must provide either *data* or *x*, *y*, and *z*.

    Full option list at :gmt-docs:`triangulate.html`

    {aliases}

    Parameters
    ----------
    x/y/z : np.ndarray
        Arrays of x and y coordinates and values z of the data points.
    data : str or np.ndarray
        Either a data file name or a 2d numpy array with the tabular data.
    projection : str
        Select map projection.
    region
        ``'xmin/xmax/ymin/ymax[+r][+uunit]'``.
        Specify the region of interest.
    spacing : str
        ``'xinc[unit][+e|n][/yinc[unit][+e|n]]'``.
        x_inc [and optionally y_inc] is the grid spacing.
    outgrid : bool or str
        Use triangulation to grid the data onto an even grid (specified with
        *region* and *spacing*). Set to True, or pass in the name of the output
        grid file. The interpolation is performed in the original coordinates,
        so if your triangles are close to the poles you are better off
        projecting all data to a local coordinate system before using
        *triangulate* (this is true of all gridding routines) or instead
        select *sphtriangulate*.
    {V}
    {registration}
        Only valid with *outgrid*.

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the outgrid parameter is set:

        - pandas.DataFrame if outgrid is None (default)
        - xarray.DataArray if outgrid is True
        - None if outgrid is a str (grid output will be stored in outgrid)

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
                raise GMTInvalidInput(f"Unrecognized data type: {type(data)}")

            with file_context as infile:
                if "G" not in kwargs:  # table output if outgrid is unset
                    kwargs.update({">": tmpfile.name})
                else:  # NetCDF or xarray.DataArray output if outgrid is set
                    if kwargs["G"] == "":  # xarray.DataArray output if outgrid=True
                        kwargs.update({"G": tmpfile.name})
                    outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module(module="triangulate", args=arg_str)

        try:
            if outgrid == tmpfile.name:  # if user did not set outfile, return DataArray
                with xr.open_dataarray(outgrid) as dataarray:
                    result = dataarray.load()
                    _ = result.gmt  # load GMTDataArray accessor information
            elif outgrid != tmpfile.name:  # if user sets an outgrid, return None
                result = None
        except UnboundLocalError:  # if outgrid unset, return pd.DataFrame
            result = pd.read_csv(tmpfile.name, sep="\t", header=None)

    return result
