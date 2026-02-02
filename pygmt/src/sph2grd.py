"""
sph2grd - Compute grid from spherical harmonic coefficients.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias

__doctest_skip__ = ["sph2grd"]


@fmt_docstring
@use_alias(b="binary", h="header")
def sph2grd(
    data: PathLike | TableLike,
    outgrid: PathLike | None = None,
    spacing: Sequence[float | str] | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    incols: int | str | Sequence[int | str] | None = None,
    registration: Literal["gridline", "pixel"] | bool = False,
    cores: int | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Compute grid from spherical harmonic coefficients.

    Reads a spherical harmonics coefficient table with records of L, M,
    C[L,M], S[L,M] and evaluates the spherical harmonic model on the
    specified grid.

    Full GMT docs at :gmt-docs:`sph2grd.html`.

    $aliases
       - G = outgrid
       - I = spacing
       - R = region
       - V = verbose
       - r = registration
       - i = incols
       - x = cores

    Parameters
    ----------
    data
        Pass in data with L, M, C[L,M], S[L,M] values by
        providing a file name to an ASCII data table, a 2-D
        $table_classes.
    $outgrid
    $spacing
    $region
    $verbose
    $binary
    $header
    $incols
    $registration
    $cores

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Create a new grid from the remote file "EGM96_to_36.txt",
    >>> # set the grid spacing to 1 arc-degree, and the region to global ("g")
    >>> new_grid = pygmt.sph2grd(data="@EGM96_to_36.txt", spacing=1, region="g")
    """
    aliasdict = AliasSystem(
        I=Alias(spacing, name="spacing", sep="/", size=2),
    ).add_common(
        R=region,
        V=verbose,
        i=incols,
        r=registration,
        x=cores,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="sph2grd", args=build_arg_list(aliasdict, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
