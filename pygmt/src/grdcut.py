"""
grdcut - Extract subregion from a grid.
"""

from typing import Literal

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdcut"]


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    N="extend",
    S="circ_subregion",
    V="verbose",
    Z="z_subregion",
    f="coltypes",
)
@kwargs_to_strings(R="sequence")
def grdcut(
    grid, kind: Literal["grid", "image"] = "grid", outgrid: str | None = None, **kwargs
) -> xr.DataArray | None:
    r"""
    Extract subregion from a grid or image.

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
    {grid}
    kind
        The raster data kind. Valid values are ``grid`` and ``image``. When the input
        ``grid`` is a file name, it's hard to determine if the file is a grid or an
        image, so we need to specify the kind explicitly. The default is ``grid``.
    {outgrid}
    {projection}
    {region}
    extend : bool or float
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
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with a longitude range of
    >>> # 10° E to 30° E, and a latitude range of 15° N to 25° N
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a new grid from an input grid, with a longitude range of
    >>> # 12° E to 15° E and a latitude range of 21° N to 24° N
    >>> new_grid = pygmt.grdcut(grid=grid, region=[12, 15, 21, 24])
    """
    # Determine the output data kind based on the input data kind.
    match inkind := data_kind(grid):
        case "image" | "grid":
            outkind = inkind
        case "file":
            outkind = kind
        case "_":
            msg = f"Unsupported data type {type(grid)}."
            raise GMTInvalidInput(msg)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind=outkind, fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(module="grdcut", args=build_arg_list(kwargs, infile=vingrd))
            return lib.virtualfile_to_raster(
                vfname=voutgrd, kind=outkind, outgrid=outgrid
            )
