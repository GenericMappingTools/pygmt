"""
grdcut - Extract subregion from a grid.
"""

from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray

__doctest_skip__ = ["grdcut"]


@fmt_docstring
@use_alias(
    G="outgrid",
    R="region",
    J="projection",
    N="extend",
    S="circ_subregion",
    V="verbose",
    Z="z_subregion",
    f="coltypes",
)
@kwargs_to_strings(R="sequence")
def grdcut(grid, **kwargs):
    r"""
    Extract subregion from a grid.

    Produce a new ``outgrid`` file which is a subregion of ``grid``. The
    subregion is specified with ``region``; the specified range must not exceed
    the range of ``grid`` (but see ``extend``). If in doubt, run
    :func:`pygmt.grdinfo` to check range. Alternatively, define the subregion
    indirectly via a range check on the node values or via distances from a
    given point. Finally, you can give ``projection`` for oblique projections
    to determine the corresponding rectangular ``region`` that will give a grid
    that fully covers the oblique domain.

    Full option list at :gmt-docs:`grdcut.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {projection}
    {region}
    extend : bool or int or float
        Allow grid to be extended if new ``region`` exceeds existing
        boundaries. Give a value to initialize nodes outside current region.
    circ_subregion : str
        *lon/lat/radius*\[\ *unit*\][**+n**].
        Specify an origin (*lon* and *lat*) and *radius*; append a distance
        *unit* and we determine the corresponding rectangular region so that
        all grid nodes on or inside the circle are contained in the subset.
        If **+n** is appended we set all nodes outside the circle to NaN.
    z_subregion : str
        [*min/max*\][**+n**\|\ **N**\|\ **r**].
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

    {verbose}
    {coltypes}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with an x-range of 10 to 30,
    >>> # and a y-range of 15 to 25
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a new grid from an input grid, with an x-range of 12 to 15,
    >>> # and a y-range of 21 to 24
    >>> new_grid = pygmt.grdcut(grid=grid, region=[12, 15, 21, 24])
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="grdcut", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
