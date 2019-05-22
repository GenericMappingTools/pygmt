"""
GMT modules for Sampling of 1-D and 2-D Data
"""
import pandas as pd
import xarray as xr

from .clib import Session
from .helpers import (
    build_arg_string,
    fmt_docstring,
    GMTTempFile,
    data_kind,
    dummy_context,
)
from .exceptions import GMTInvalidInput


@fmt_docstring
def grdtrack(table: pd.DataFrame, grid: xr.DataArray, newcolname: str = "z_", **kwargs):
    """
    Sample grids at specified (x,y) locations.

    Grdtrack reads one or more grid files and a table with (x,y) [or (lon,lat)]
    positions in the first two columns (more columns may be present). It interpolates
    the grid(s) at the positions in the table and writes out the table with the
    interpolated values added as (one or more) new columns. A bicubic [Default],
    bilinear, B-spline or nearest-neighbor (see -n) interpolation is used, requiring
    boundary conditions at the limits of the region.

    Parameters
    ----------
    table: pandas.DataFrame
        Table with (x, y) or (lon, lat) values in the first two columns. More columns
        may be present.

    grid: xarray.DataArray or file (netcdf)
        Gridded array from which to sample values from.

    newcolname: str
        Name for the new column in the table where the sampled values will be placed.
        Defaults to "z_".

    Returns
    -------
    ret: pandas.DataFrame
        Table with (x, y, ..., z_) or (lon, lat, ..., z_) values.

    """
    with GMTTempFile(suffix=".csv") as tmpfile:
        with Session() as lib:
            # Store the pandas.DataFrame table in virtualfile
            if data_kind(table) == "matrix":
                table_context = lib.virtualfile_from_matrix(table.values)
            else:
                raise GMTInvalidInput(f"Unrecognized data type {type(table)}")

            # Store the xarray.DataArray grid in virtualfile
            if data_kind(grid) == "grid":
                grid_context = lib.virtualfile_from_grid(grid)
            elif data_kind(grid) == "file":
                grid_context = dummy_context(grid)
            else:
                raise GMTInvalidInput(f"Unrecognized data type {type(grid)}")

            # Run grdtrack on the temporary (csv) table and (netcdf) grid virtualfiles
            with table_context as csvfile:
                with grid_context as grdfile:
                    kwargs.update({"G": grdfile})
                    arg_str = " ".join(
                        [csvfile, build_arg_string(kwargs), "->" + tmpfile.name]
                    )
                    lib.call_module(module="grdtrack", args=arg_str)

        # Read temporary csv output to a pandas table
        column_names = table.columns.to_list() + [newcolname]
        result = pd.read_csv(tmpfile.name, sep="\t", names=column_names)

    return result
