"""
basemap - Plot base maps and frames.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias


@fmt_docstring
@use_alias(F="box", Tm="compass", f="coltypes")
def basemap(  # noqa: PLR0913
    self,
    projection: str | None = None,
    zsize: float | str | None = None,
    zscale: float | str | None = None,
    frame: str | Sequence[str] | bool = False,
    region: Sequence[float | str] | str | None = None,
    map_scale: str | None = None,
    rose: str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    transparency: float | None = None,
    perspective: float | Sequence[float] | str | bool = False,
    **kwargs,
):
    r"""
    Plot base maps and frames.

    Creates a basic or fancy basemap with axes, fill, and titles. Several map
    projections are available, and the user may specify separate tick-mark intervals for
    boundary annotation, ticking, and [optionally] gridlines.

    At least one of the parameters ``frame``, ``map_scale``, ``rose``, or ``compass``
    must be specified if not in subplot mode.

    See also the following methods that provide higher-level interfaces to the GMT's
    ``basemap`` module:

    - :meth:`pygmt.Figure.scalebar`: Add a scale bar on the plot.

    Full GMT docs at :gmt-docs:`basemap.html`.

    $aliases
       - B = frame
       - J = projection
       - Jz = zscale
       - JZ = zsize
       - L = map_scale
       - R = region
       - Td = rose
       - V = verbose
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    $projection
    zscale/zsize
        Set z-axis scaling or z-axis size.
    $region
        *Required if this is the first plot command.*
    $frame
    map_scale
        Draw a map scale bar on the plot.

        .. deprecated:: v0.19.0

            This parameter is deprecated. Use :meth:`pygmt.Figure.scalebar` instead,
            which provides a more comprehensive and flexible API for adding scale bars
            to plots. This parameter still accepts raw GMT CLI strings for the ``-L``
            option of the ``basemap`` module for backward compatibility.
    rose
        Draw a map directional rose on the map.

        .. deprecated:: v0.19.0

            This parameter is deprecated. Use :meth:`pygmt.Figure.directional_rose`
            instead, which provides a more comprehensive and flexible API for adding
            directional roses. This parameter still accepts raw GMT CLI strings for the
            ``-Td`` option of the ``basemap`` module for backward compatibility.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draw a rectangular border around the
        map scale or rose. Alternatively, specify a different pen with
        **+p**\ *pen*. Add **+g**\ *fill* to fill the scale panel [Default is
        no fill]. Append **+c**\ *clearance* where *clearance* is either gap,
        xgap/ygap, or lgap/rgap/bgap/tgap where these items are uniform,
        separate x and y, or individual side spacings between scale and
        border. Append **+i** to draw a secondary, inner border as well.
        We use a uniform gap between borders of 2 points and the
        :gmt-term:`MAP_DEFAULTS_PEN` unless other values are specified. Append
        **+r** to draw rounded rectangular borders instead, with a 6-points
        corner radius. You can override this radius by appending another value.
        Finally, append **+s** to draw an offset background shaded region.
        Here, *dx/dy* indicates the shift relative to the foreground frame
        [Default is ``"4p/-4p"``] and shade sets the fill style to use for
        shading [Default is ``"gray50"``].
    compass : str
        Draw a map magnetic rose on the map at the location defined by the
        reference and anchor points.
    $verbose
    $panel
    $coltypes
    $perspective
    $transparency
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        Jz=Alias(zscale, name="zscale"),
        JZ=Alias(zsize, name="zsize"),
        L=Alias(map_scale, name="map_scale"),  # Deprecated.
        Td=Alias(rose, name="rose"),  # Deprecated.
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
