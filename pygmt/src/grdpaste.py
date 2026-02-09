"""
grdpaste - Join two grids along their common edge.
"""

from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias

__doctest_skip__ = ["grdpaste"]


@fmt_docstring
@use_alias(f="coltypes")
def grdpaste(
    grid_a: PathLike | xr.DataArray,
    grid_b: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Join two grids along their common edge.

    Combine ``grid_a`` and ``grid_b`` into ``outgrid`` by pasting them together
    along their common edge. The two input grids must have the same grid spacings
    and registration, and must have one edge in common. If in doubt, check with
    :func:`pygmt.grdinfo` and use :func:`pygmt.grdcut` and/or
    :func:`pygmt.grdsample` if necessary to prepare the edge joint. Note: For
    geographical grids, you may have to use ``coltypes`` to handle periodic longitudes
    unless the input grids are properly recognized as such via their meta-data. For
    stitching multiple grids, see :func:`pygmt.grdblend` instead.

    Full GMT docs at :gmt-docs:`grdpaste.html`.

    $aliases
       - G = outgrid
       - V = verbose

    Parameters
    ----------
    grid_a
        The first grid file to be pasted. Can be a file name or an
        :class:`xarray.DataArray`.
    grid_b
        The second grid file to be pasted. Can be a file name or an
        :class:`xarray.DataArray`.
    $outgrid
    $verbose
    $coltypes

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
    >>> # Create two grids with a common edge
    >>> # Grid A: longitude range of 10° E to 20° E, latitude range of 15° N to 25° N
    >>> grid_a = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 20, 15, 25]
    ... )
    >>> # Grid B: longitude range of 10° E to 20° E, latitude range of 10° N to 15° N
    >>> grid_b = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 20, 10, 15]
    ... )
    >>> # Paste the two grids together along their common edge (15° N)
    >>> new_grid = pygmt.grdpaste(grid_a=grid_a, grid_b=grid_b)
    """
    aliasdict = AliasSystem().add_common(V=verbose)
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid_a) as vingrd_a,
            lib.virtualfile_in(check_kind="raster", data=grid_b) as vingrd_b,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdpaste",
                args=build_arg_list(aliasdict, infile=[vingrd_a, vingrd_b]),
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
