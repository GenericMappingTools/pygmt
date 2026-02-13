"""
grdproject - Forward and inverse map transformation of grids.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias

__doctest_skip__ = ["grdproject"]


@fmt_docstring
@use_alias(n="interpolation")
def grdproject(  # noqa: PLR0913
    grid: PathLike | xr.DataArray,
    outgrid: PathLike | None = None,
    center: Sequence[float | str] | bool = False,
    spacing: float | str | Sequence[float | str] | None = None,
    dpi: int | None = None,
    inverse: bool = False,
    unit: Literal["c", "i", "p"] | None = None,
    scaling: Literal["c", "i", "p", "e", "f", "k", "M", "n", "u"] | bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    registration: Literal["gridline", "pixel"] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Forward and inverse map transformation of grids.

    This method will project a geographical gridded data set onto a rectangular grid. If
    ``inverse`` is ``True``, it will project a rectangular coordinate system to a
    geographic system. To obtain the value at each new node, its location is inversely
    projected back onto the input grid after which a value is interpolated between the
    surrounding input grid values. By default bi-cubic interpolation is used. Aliasing
    is avoided by also forward projecting the input grid nodes. If two or more nodes are
    projected onto the same new node, their average will dominate in the calculation of
    the new node value. Interpolation and aliasing is controlled with the
    ``interpolation`` parameter. The new node spacing may be determined in one of
    several ways by specifying the grid spacing, number of nodes, or resolution. Nodes
    not constrained by input data are set to NaN. The ``region`` parameter can be used
    to select a map region large or smaller than that implied by the extent of the grid
    file.

    Full GMT docs at :gmt-docs:`grdproject.html`.

    $aliases
       - C = center
       - D = spacing
       - E = dpi
       - F = scaling
       - G = outgrid
       - I = inverse
       - J = projection
       - M = unit
       - R = region
       - V = verbose
       - r = registration

    Parameters
    ----------
    $grid
    $outgrid
    center
        If ``True``, let the projected coordinates be relative to the projection center
        [Default is relative to the lower left corner]. Optionally, set offsets
        (*dx*, *dy*) in the projected units to be added (or subtracted when ``inverse``
        is set) to (from) the projected coordinates, such as false eastings and
        northings for particular projection zones [Default is ``(0, 0)``].
    $spacing
    dpi
        Set the resolution for the new grid in dots per inch.
    inverse
        When set to ``True``, do the inverse transformation, from rectangular to
        geographical [Default is ``False``].
    unit
        Set the projected measure unit. See :doc:`/techref/units#plot-units` for
        supported units [Default is set by :gmt-term:`PROJ_LENGTH_UNIT`]. Cannot be used
        with ``scaling``.
    scaling
        Force 1:1 scaling, i.e., output (or input, see ``inverse``) data are in actual
        projected meters. To specify other units, set it to
        a supported distance unit or plot unit (see :doc:`/techref/units`). Without
        ``scaling``, the output (or input, see ``inverse``) is in the units specified
        by :gmt-term:`PROJ_LENGTH_UNIT` (but see ``unit``).
    $projection
    $region
    $verbose
    $interpolation
    $registration

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
    >>> region = [10, 30, 15, 25]
    >>> grid = pygmt.datasets.load_earth_relief(resolution="30m", region=region)
    >>> # Project the geographic gridded data onto a rectangular grid
    >>> new_grid = pygmt.grdproject(grid=grid, projection="M10c", region=region)
    """
    if kwargs.get("J", projection) is None:
        raise GMTParameterError(required="projection")

    if kwargs.get("M", unit) is not None and kwargs.get("F", scaling) is not False:
        raise GMTParameterError(at_most_one=["unit", "scaling"])

    aliasdict = AliasSystem(
        C=Alias(center, name="center", sep="/", size=2),
        D=Alias(spacing, name="spacing", sep="/", size=2),
        E=Alias(dpi, name="dpi"),
        F=Alias(scaling, name="scaling"),
        I=Alias(inverse, name="inverse"),
        M=Alias(unit, name="unit"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        r=registration,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdproject", args=build_arg_list(aliasdict, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
