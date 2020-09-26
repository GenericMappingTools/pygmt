"""
GMT modules for grid operations
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
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
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
    z_subregion : str
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
                file_context = lib.virtualfile_from_grid(grid)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))

            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("grdcut", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
