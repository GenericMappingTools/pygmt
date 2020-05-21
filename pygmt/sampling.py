"""
GMT modules for Sampling of 1-D and 2-D Data
"""
import pandas as pd

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
def grdtrack(points, grid, newcolname=None, outfile=None, **kwargs):
    """
    Sample grids at specified (x,y) locations.

    Grdtrack reads one or more grid files and a table with (x,y) [or (lon,lat)]
    positions in the first two columns (more columns may be present). It
    interpolates the grid(s) at the positions in the table and writes out the
    table with the interpolated values added as (one or more) new columns. A
    bicubic [Default], bilinear, B-spline or nearest-neighbor (see -n)
    interpolation is used, requiring boundary conditions at the limits of the
    region.

    Full option list at :gmt-docs:`grdtrack.html`

    Parameters
    ----------
    points: pandas.DataFrame or file (csv, txt, etc)
        Either a table with (x, y) or (lon, lat) values in the first two
        columns, or a data file name. More columns may be present.

    grid: xarray.DataArray or file (netcdf)
        Gridded array from which to sample values from.

    newcolname: str
        Required if 'points' is a pandas.DataFrame. The name for the new column
        in the track pandas.DataFrame table where the sampled values will be
        placed.

    outfile: str
        Required if 'points' is a file. The file name for the output ASCII
        file.

    Returns
    -------
    track: pandas.DataFrame or None
        Return type depends on whether the outfile parameter is set:

        - pandas.DataFrame table with (x, y, ..., newcolname) if outfile is not
          set
        - None if outfile is set (track output will be stored in outfile)

    """

    with GMTTempFile(suffix=".csv") as tmpfile:
        with Session() as lib:
            # Store the pandas.DataFrame points table in virtualfile
            if data_kind(points) == "matrix":
                if newcolname is None:
                    raise GMTInvalidInput("Please pass in a str to 'newcolname'")
                table_context = lib.virtualfile_from_matrix(points.values)
            elif data_kind(points) == "file":
                if outfile is None:
                    raise GMTInvalidInput("Please pass in a str to 'outfile'")
                table_context = dummy_context(points)
            else:
                raise GMTInvalidInput(f"Unrecognized data type {type(points)}")

            # Store the xarray.DataArray grid in virtualfile
            if data_kind(grid) == "grid":
                grid_context = lib.virtualfile_from_grid(grid)
            elif data_kind(grid) == "file":
                grid_context = dummy_context(grid)
            else:
                raise GMTInvalidInput(f"Unrecognized data type {type(grid)}")

            # Run grdtrack on the temporary (csv) points table
            # and (netcdf) grid virtualfile
            with table_context as csvfile:
                with grid_context as grdfile:
                    kwargs.update({"G": grdfile})
                    if outfile is None:  # Output to tmpfile if outfile is not set
                        outfile = tmpfile.name
                    arg_str = " ".join(
                        [csvfile, build_arg_string(kwargs), "->" + outfile]
                    )
                    lib.call_module(module="grdtrack", args=arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            column_names = points.columns.to_list() + [newcolname]
            result = pd.read_csv(tmpfile.name, sep="\t", names=column_names)
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

    return result
