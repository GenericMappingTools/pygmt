"""
grdsample - Resample a grid onto a new lattice.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    use_alias,
)

__doctest_skip__ = ["grdsample"]


# TODO(PyGMT>=0.21.0): Remove the deprecated "translate" parameter.
@fmt_docstring
@deprecate_parameter("translate", "toggle", "v0.18.0", remove_version="v0.21.0")
@use_alias(f="coltypes", n="interpolation")
def grdsample(
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    toggle: bool = False,
    spacing: Sequence[float | str] | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    registration: Literal["gridline", "pixel"] | bool = False,
    cores: int | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    """
    Resample a grid onto a new lattice.

    This function reads a grid and interpolates it to create a new grid. It can

    - change the registration (via ``toggle`` or ``registration``)
    - change the grid-spacing or number of nodes (via ``spacing``)
    - set a new sub-region (via ``region``)

    When ``region`` is omitted, the output grid will cover the same region as the input
    grid. When ``spacing`` is omitted, the grid spacing of the output grid will be the
    same as the input grid. Either ``registration`` or ``toggle`` can be used to change
    the grid registration. When omitted, the output grid will have the same registration
    as the input grid.

    A bicubic [Default], bilinear, B-spline, or nearest-neighbor interpolation is set
    with ``interpolation``. Note that using ``region`` only is equivalent to
    :func:`pygmt.grdcut` or ``grdedit -S``. ``grdsample`` safely creates a fine mesh
    from a coarse one; the converse may suffer aliasing unless the data are filtered
    using :func:`pygmt.grdfilter` or ``grdfft``.

    Full GMT docs at :gmt-docs:`grdsample.html`.

    $aliases
       - G = outgrid
       - I = spacing
       - R = region
       - T = toggle
       - V = verbose
       - r = registration
       - x = cores

    Parameters
    ----------
    $grid
    $outgrid
    $spacing
    toggle
        Toggle between grid and pixel registration; if the input is grid-registered, the
        output will be pixel-registered and vice-versa. This is a *destructive* grid
        change; see :gmt-docs:`reference/options.html#switch-registrations`.
        *Note**: ``toggle`` and ``registration`` are mutually exclusive.
    $region
    $verbose
    $coltypes
    $interpolation
    $registration
    $cores

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
    >>> new_grid = pygmt.grdsample(grid=grid, toggle=True, spacing=[0.5, 0.5])
    """
    if kwargs.get("T", toggle) and kwargs.get("r", registration):
        raise GMTParameterError(at_most_one=["toggle", "registration"])

    aliasdict = AliasSystem(
        I=Alias(spacing, name="spacing", sep="/", size=2),
        T=Alias(toggle, name="toggle"),
    ).add_common(
        R=region,
        V=verbose,
        r=registration,
        x=cores,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdsample", args=build_arg_list(aliasdict, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
