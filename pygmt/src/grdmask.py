"""
grdmask - Create mask grid from polygons or point coverage.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, fmt_docstring

__doctest_skip__ = ["grdmask"]


def _alias_option_N(  # noqa: N802
    outside: float | Literal["z", "id"] | None = None,
    edge: float | Literal["z", "id"] | None = None,
    inside: float | Literal["z", "id"] | None = None,
) -> Alias:
    """
    Return an Alias object for the -N option.

    Builds the -N parameter string for grdmask based on the inside, edge, and
    outside values. Handles special modes "z" (use z-value from polygon data)
    and "id" (use running polygon ID).

    Examples
    --------
    >>> _alias_option_N(outside=0, edge=0, inside=1)._value
    '0/0/1'
    >>> _alias_option_N(outside=1, edge=2, inside=3)._value
    '1/2/3'
    >>> _alias_option_N(outside=0, edge=0, inside="z")._value
    'z'
    >>> _alias_option_N(outside=1, edge=0, inside="z")._value
    'z/1'
    >>> _alias_option_N(outside=0, edge="z", inside="z")._value
    'Z'
    >>> _alias_option_N(outside=0, edge=0, inside="id")._value
    'p'
    >>> _alias_option_N(outside=0, edge="id", inside="id")._value
    'P'
    """
    # Validate combinations
    if inside in {"z", "id"} and edge in {"z", "id"} and inside != edge:
        msg = f"Invalid combination: inside={inside!r} and edge={edge!r}. "
        raise GMTParameterError(
            reason=msg + "When both are special modes, they must be the same."
        )

    # Build -N argument
    if inside in {"z", "id"}:
        # Mode: -Nz, -NZ, -Np, or -NP
        mode_char = "z" if inside == "z" else "p"
        if edge == inside:
            mode_char = mode_char.upper()
        mask_values = mode_char if outside in {None, 0} else [mode_char, outside]
    else:
        mask_values = [outside, edge, inside]
    return Alias([outside, edge, inside], name="mask_values", sep="/", size={2, 3})


@fmt_docstring
def grdmask(
    data,
    outgrid: PathLike | None = None,
    spacing: Sequence[float | str] | None = None,
    region: Sequence[float | str] | str | None = None,
    outside: float | Literal["z", "id"] = 0,
    edge: float | Literal["z", "id"] = 0,
    inside: float | Literal["z", "id"] = 1,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> xr.DataArray | None:
    """
    Create mask grid from polygons or point coverage.

    Reads one or more files (or standard input) containing polygon or data point
    coordinates, and creates a binary grid file where nodes that fall inside, on the
    edge, or outside the polygons (or within the search radius from data points) are
    assigned values based on ``outside``, ``edge``, and ``inside`` parameters.

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
        Pass in either a file name, :class:`pandas.DataFrame`, :class:`numpy.ndarray`,
        or a list of file names containing the polygon(s) or data points. Input can be:

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
        
        To treats edges as inside, using the same value as ``inside``. 
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
           [0., 0., 0., 0., 1., 0.],
           [0., 0., 1., 1., 1., 0.],
           [0., 0., 1., 1., 1., 0.],
           [0., 0., 1., 1., 1., 0.],
           [0., 0., 0., 0., 0., 0.]])
    """
    if spacing is None or region is None:
        raise GMTParameterError(required=["region", "spacing"])

    aliasdict = AliasSystem(
        I=Alias(spacing, name="spacing", sep="/", size=2),
        N=_alias_option_N(outside=outside, edge=edge, inside=inside),
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
