"""
grdtrack - Sample grids at specified (x,y) locations.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    use_alias,
)


@fmt_docstring
@use_alias(V="verbose", f="coltypes", n="interpolation")
def grdtrack(points, grid, newcolname=None, outfile=None, **kwargs):
    """
    Sample grids at specified (x,y) locations.

    Grdtrack reads one or more grid files and a table with (x,y) [or (lon,lat)]
    positions in the first two columns (more columns may be present). It
    interpolates the grid(s) at the positions in the table and writes out the
    table with the interpolated values added as (one or more) new columns. A
    bicubic [Default], bilinear, B-spline or nearest-neighbor interpolation is
    used, requiring boundary conditions at the limits of the region (see
    ``interpolation``; Default uses “natural” conditions (second partial
    derivative normal to edge is zero) unless the grid is automatically
    recognized as periodic.)

    Full option list at :gmt-docs:`grdtrack.html`

    {aliases}

    Parameters
    ----------
    points : pandas.DataFrame or str
        Either a table with (x, y) or (lon, lat) values in the first two
        columns, or a filename (e.g. csv, txt format). More columns may be
        present.

    grid : xarray.DataArray or str
        Gridded array from which to sample values from, or a filename (netcdf
        format).

    newcolname : str
        Required if ``points`` is a :class:`pandas.DataFrame`. The name for the
        new column in the track :class:`pandas.DataFrame` table where the
        sampled values will be placed.

    outfile : str
        Required if ``points`` is a file. The file name for the output ASCII
        file.

    {V}
    {f}
    {n}

    Returns
    -------
    track: pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, ..., newcolname) if
          ``outfile`` is not set
        - None if ``outfile`` is set (track output will be stored in file set
          by ``outfile``)
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
            grid_context = lib.virtualfile_from_data(check_kind="raster", data=grid)

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
