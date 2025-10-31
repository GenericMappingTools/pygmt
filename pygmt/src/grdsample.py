"""
grdsample - Resample a grid onto a new lattice.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.src.grdinfo import grdinfo as _grdinfo

__doctest_skip__ = ["grdsample"]


@fmt_docstring
@use_alias(
    I="spacing",
    T="translate",
    f="coltypes",
    n="interpolation",
    r="registration",
)
@kwargs_to_strings(I="sequence")
def grdsample(
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    region: Sequence[float | str] | str | None = None,
    translate: bool | None = None,
    registration: str | bool | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    cores: int | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Resample a grid onto a new lattice.

    This reads a grid file and interpolates it to create a new grid
    file. It can change the registration with ``translate`` or
    ``registration``, change the grid-spacing or number of nodes with
    ``spacing``, and set a new sub-region using ``region``. A bicubic
    [Default], bilinear, B-spline or nearest-neighbor interpolation is set
    with ``interpolation``.

    When ``region`` is omitted, the output grid will cover the same region as
    the input grid. When ``spacing`` is omitted, the grid spacing of the
    output grid will be the same as the input grid. Either ``registration`` or
    ``translate`` can be used to change the grid registration. When omitted,
    the output grid will have the same registration as the input grid.

    Full GMT docs at :gmt-docs:`grdsample.html`.

    {aliases}
       - R = region
       - V = verbose
       - x = cores

    Parameters
    ----------
    {grid}
    {outgrid}
    {spacing}
    {region}
    translate : bool
        Translate between grid and pixel registration; if the input is
        grid-registered, the output will be pixel-registered and vice-versa.
    registration : str or bool
        [**g**\|\ **p**\ ].
        Set registration to **g**\ ridline or **p**\ ixel.
    {verbose}
    {coltypes}
    {interpolation}
    {cores}

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
    >>> # Create a new grid from an input grid, change the registration,
    >>> # and set both x- and y-spacings to 0.5 arc-degrees
    >>> new_grid = pygmt.grdsample(grid=grid, translate=True, spacing=[0.5, 0.5])
    """
    aliasdict = AliasSystem().add_common(
        R=region,
        V=verbose,
        x=cores,
    )
    aliasdict.merge(kwargs)

    # Normalize file inputs to DataArray for consistent behavior with virtual files.
    # This avoids subtle differences between GMT reading from files vs virtual grids.
    if not isinstance(grid, xr.DataArray):
        try:
            grid = xr.load_dataarray(grid, engine="gmt", raster_kind="grid")
        except Exception:  
            pass

    # If translate (-T) is requested (present in aliasdict), remove any -r to avoid conflict
    if aliasdict.get("T"):
        aliasdict.pop("r", None)

    # 2. Handle registration for filename inputs only (do not mutate DataArray)
    if not isinstance(grid, xr.DataArray):
        # registration explicitly, infer registration from the input grid so that
        # -R rounding and output alignment match the DataArray code path.
        if registration is None and not aliasdict.get("T"):
            try:
                info = _grdinfo(grid, per_column="n")
                parts = info.split()
                reg_flag = int(parts[-2])  # 0 = gridline, 1 = pixel
                registration = "p" if reg_flag == 1 else "g"
            except Exception:  
                registration = None

    # When translate=True, we only pass -T and avoid -r to prevent conflicts.
    if registration is not None and not aliasdict.get("T"):
        aliasdict["r"] = registration

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            # Final guard: ensure -r isn't passed together with -T
            if aliasdict.get("T"):
                aliasdict.pop("r", None)
            lib.call_module(
                module="grdsample", args=build_arg_list(aliasdict, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
