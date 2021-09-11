"""
triangulate - Delaunay triangulation or Voronoi partitioning and gridding of
Cartesian data.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@use_alias(
    G="outgrid",
    I="spacing",
    J="projection",
    R="region",
    V="verbose",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    r="registration",
)
@kwargs_to_strings(R="sequence")
def triangulate(table=None, x=None, y=None, z=None, **kwargs):
    """
    Delaunay triangulation or Voronoi partitioning and gridding of Cartesian
    data.

    Triangulate reads in x,y[,z] data and performs Delaunay triangulation,
    i.e., it finds how the points should be connected to give the most
    equilateral triangulation possible. If a map projection (give *region*
    and *projection*) is chosen then it is applied before the triangulation
    is calculated.

    Must provide either ``table`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`triangulate.html`

    {aliases}

    Parameters
    ----------
    x/y/z : np.ndarray
        Arrays of x and y coordinates and values z of the data points.
    table : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    {J}
    {R}
    {I}
    outgrid : bool or str
        Use triangulation to grid the data onto an even grid (specified with
        ``region`` and ``spacing``). Set to ``True``, or pass in the name of
        the output grid file. The interpolation is performed in the original
        coordinates, so if your triangles are close to the poles you are better
        off projecting all data to a local coordinate system before using
        *triangulate* (this is true of all gridding routines) or instead
        select *sphtriangulate*.
    {V}
    {b}
    {d}
    {e}
    {f}
    {h}
    {i}
    {r}
        Only valid with ``outgrid``.

    Returns
    -------
    ret: pandas.DataFrame or xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - pandas.DataFrame if ``outgrid`` is None (default)
        - xarray.DataArray if ``outgrid`` is True
        - None if ``outgrid`` is a str (grid output is stored in ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            # Choose how data will be passed into the module
            table_context = lib.virtualfile_from_data(
                check_kind="vector", data=table, x=x, y=y, z=z
            )
            with table_context as infile:
                if "G" not in kwargs:  # table output if outgrid is unset
                    kwargs.update({">": tmpfile.name})
                else:  # NetCDF or xarray.DataArray output if outgrid is set
                    if (
                        kwargs["G"] is True
                    ):  # xarray.DataArray output if outgrid is True
                        kwargs.update({"G": tmpfile.name})
                    outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module(module="triangulate", args=arg_str)

        try:
            result = load_dataarray(outgrid) if outgrid == tmpfile.name else None
        except UnboundLocalError:  # if outgrid unset, return pd.DataFrame
            result = pd.read_csv(tmpfile.name, sep="\t", header=None)

    return result
