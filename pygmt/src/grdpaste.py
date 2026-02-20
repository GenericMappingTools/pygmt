"""
grdpaste - Join two grids along their common edge.
"""

from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias


@fmt_docstring
@use_alias(f="coltypes")
def grdpaste(
    grid1: PathLike | xr.DataArray,
    grid2: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    """
    Join two grids along their common edge.

    Requires GMT dev version (>=6.6.0).

    Combine ``grid1`` and ``grid2`` into a single grid by pasting them together
    along their common edge. The two input grids must have the same grid spacings
    and registration, and must have one edge in common. If in doubt, check with
    :func:`pygmt.grdinfo` and use :func:`pygmt.grdcut` and/or
    :func:`pygmt.grdsample` if necessary to prepare the edge joint. Note: For
    geographical grids, you may have to use ``coltypes`` to handle periodic
    longitudes unless the input grids are properly recognized as such via their
    meta-data. For stitching multiple grids, see ``grdblend`` (not implemented in
    PyGMT yet) instead.

    Full GMT docs at :gmt-docs:`grdpaste.html`.

    $aliases
       - G = outgrid
       - V = verbose

    Parameters
    ----------
    grid1
    grid2
        The two grids to be pasted. Each can be a file name or a
        :class:`xarray.DataArray` object.
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
    """
    aliasdict = AliasSystem().add_common(V=verbose)
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid1) as vingrd1,
            lib.virtualfile_in(check_kind="raster", data=grid2) as vingrd2,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdpaste",
                args=build_arg_list(aliasdict, infile=[vingrd1, vingrd2]),
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
