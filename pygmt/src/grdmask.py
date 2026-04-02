"""
grdmask - Create mask grid from polygons or point coverage.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring

__doctest_skip__ = ["grdmask"]


def _alias_option_N(  # noqa: N802
    outside: float | None = None,
    edge: float | Literal["z", "id"] | None = None,
    inside: float | Literal["z", "id"] | None = None,
    id_start: float | None = None,
) -> Alias:
    """
    Return an Alias object for the -N option.

    Builds the -N parameter string for grdmask based on the inside, edge, and
    outside values. Handles special modes "z" (use z-value from polygon data)
    and "id" (use running polygon ID).

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return AliasSystem(N=_alias_option_N(**kwargs)).get("N")
    >>> parse()
    >>> parse(outside=1, edge=2, inside=3)
    '1/2/3'
    >>> parse(outside=3)
    '3/0/1'
    >>> parse(inside="z")
    'z'
    >>> parse(outside=1, inside="z")
    'z/1'
    >>> parse(edge="z", inside="z")
    'Z'
    >>> parse(inside="id")
    'p'
    >>> parse(edge="id", inside="id")
    'P'
    >>> parse(inside="id", id_start=5)
    'p5'
    >>> parse(edge="id", inside="id", id_start=10)
    'P10'
    >>> parse(edge="id", inside="id", id_start=5, outside=3)
    'P5/3'
    >>> parse(edge="id", id_start=5, outside=3)
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTParameterError: ...
    >>> parse(edge="z")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: ...
    >>> parse(inside="z", edge="id")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: ...
    >>> parse(inside="z", id_start=5)
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTParameterError: ...
    """
    _inside_modes = {"z": "z", "id": "p"}

    if id_start is not None and inside != "id":
        raise GMTParameterError(
            reason=f"Parameter 'id_start' requires inside='id', got inside={inside!r}."
        )

    # outside/edge/inside are all omitted: keep GMT default 0/0/1
    if all(v is None for v in (outside, inside, edge)):
        return Alias(None, name="mask_values")

    # In the special mdoes, 'edge' must be None or the same as 'inside'
    if (edge in _inside_modes or inside in _inside_modes) and edge not in {
        None,
        inside,
    }:
        raise GMTValueError(
            edge,
            description="edge",
            reason=f"inside={inside!r} and edge={edge!r} must be the same.",
        )

    # Build -N argument
    if inside in _inside_modes:  # Mode: -Nz, -NZ, -Np, or -NP
        mode = "z" if inside == "z" else "p"
        if edge == inside:
            mode = mode.upper()
        # Append id_start if specified (only valid for "id" mode)
        if id_start is not None:
            mode = f"{mode}{id_start}"
        mask_values = mode if outside is None else [mode, outside]
    else:  # Build the full mask with defaults for any missing values.
        mask_values = [
            0 if outside is None else outside,
            0 if edge is None else edge,
            1 if inside is None else inside,
        ]
    return Alias(mask_values, name="mask_values", sep="/", size=(2, 3))


@fmt_docstring
def grdmask(
    data,
    outgrid: PathLike | None = None,
    spacing: Sequence[float | str] | None = None,
    region: Sequence[float | str] | str | None = None,
    outside: float | None = None,
    edge: float | Literal["z", "id"] | None = None,
    inside: float | Literal["z", "id"] | None = None,
    id_start: float | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    """
    Create mask grid from polygons or point coverage.

    Reads one or more files containing polygon or data point coordinates, and creates a
    grid where nodes that fall inside, on the edge, or outside the polygons (or within
    the search radius from data points) are assigned values based on ``outside``,
    ``edge``, and ``inside`` parameters.

    The mask grid can be used to mask out specific regions in other grids using
    :func:`pygmt.grdmath` or similar tools. For masking based on coastline features,
    consider using :func:`pygmt.grdlandmask` instead.

    Full GMT docs at :gmt-docs:`grdmask.html`.

    **Aliases**

    .. hlist::
       :columns: 3

       - G = outgrid
       - I = spacing
       - N = outside/edge/inside
       - R = region
       - V = verbose

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a 2-D $table_classes
        containg the polygon(s) or data points. Input can be:

        - **Polygon mode**: One or more files containing closed polygon coordinates
        - **Point coverage mode**: Data points (used with ``search_radius`` parameter)
    $outgrid
    $spacing
    outside
    edge
    inside
        Set the value assigned to nodes outside, on the edge, or inside the polygons.
        Can be any number, or one of ``None``, ``"NaN"``, and ``np.nan`` for NaN.

        ``inside`` can also be set to one of the following values:

        - ``"z"``: Use the z-value from polygon data (segment header ``-Zzval``,
          ``-Lheader``, or via ``-aZ=name``).
        - ``"id"``: Use a running polygon ID number.

        To treat edges as inside, use the same value as ``inside``.
    id_start
        The starting number for polygon IDs when ``inside="id"``.
        Default is 0. Only valid when ``inside="id"``.
    $region
    $verbose

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
    >>> import numpy as np
    >>> # Create a simple polygon as a triangle
    >>> polygon = np.array([[125, 30], [130, 30], [130, 35], [125, 30]])
    >>> # Create a mask grid with 1 arc-degree spacing
    >>> mask = pygmt.grdmask(data=polygon, spacing=1, region=[125, 130, 30, 35])
    >>> mask.values
    array([[0., 0., 0., 0., 0., 0.],
           [0., 0., 1., 1., 1., 0.],
           [0., 0., 0., 1., 1., 0.],
           [0., 0., 0., 0., 1., 0.],
           [0., 0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 0., 0.]], dtype=float32)
    """
    if kwargs.get("I", spacing) is None or kwargs.get("R", region) is None:
        raise GMTParameterError(required=["region", "spacing"])

    aliasdict = AliasSystem(
        I=Alias(spacing, name="spacing", sep="/", size=2),
        N=_alias_option_N(outside=outside, edge=edge, inside=inside, id_start=id_start),
    ).add_common(
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="grdmask",
                args=build_arg_list(aliasdict, infile=vintbl),
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
