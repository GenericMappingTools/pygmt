"""
basemap - Plot base maps and frames.
"""

import warnings
from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias
from pygmt.params import Axis, Box, Frame


@fmt_docstring
@use_alias(f="coltypes")
def basemap(  # noqa: PLR0913
    self,
    projection: str | None = None,
    zscale: float | str | None = None,
    zsize: float | str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    map_scale: str | None = None,
    compass: str | None = None,
    rose: str | None = None,
    box: Box | str | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    """
    Plot base maps and frames.

    Creates a basic or fancy basemap with axes, fill, and titles. Several map
    projections are available, and separate tick-mark intervals for axis annotation,
    ticking, and gridlines can be specified.

    If not in subplot mode (see :meth:`pygmt.Figure.subplot`), at least one of the
    parameters ``frame``, ``map_scale``, ``rose``, or ``compass`` must be specified.

    .. note::

        Parameters ``map_scale``, ``rose``, and ``compass`` are deprecated since
        v0.19.0 in favor of the dedicated higher-level methods:

        - :meth:`pygmt.Figure.scalebar`: Add a scale bar on the plot.
        - :meth:`pygmt.Figure.directional_rose`: Add a directional rose on the plot.
        - :meth:`pygmt.Figure.magnetic_rose`: Add a magnetic rose on the plot.

        These methods provide more comprehensive and flexible APIs for their respective
        plot elements. The ``box`` parameter in :meth:`pygmt.Figure.basemap` is retained
        only as a compatibility parameter for these legacy parameters. For new code,
        prefer the ``box`` parameter on the dedicated methods instead.

    Full GMT docs at :gmt-docs:`basemap.html`.

    $aliases
       - B = frame
       - F = box
       - J = projection
       - Jz = zscale
       - JZ = zsize
       - L = map_scale
       - R = region
       - Td = rose
       - Tm = compass
       - V = verbose
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    $projection
    $region
        *Required if this is the first plot command.*
    $frame
    zscale
    zsize
        Set z-axis scaling or z-axis size.
    map_scale
        Draw a map scale bar on the plot.

        .. deprecated:: v0.19.0

            Use :meth:`pygmt.Figure.scalebar` instead. This parameter is maintained
            for backward compatibility and accepts raw GMT CLI strings for the ``-L``
            option.
    compass
        Draw a map magnetic rose on the map.

        .. deprecated:: v0.19.0

            Use :meth:`pygmt.Figure.magnetic_rose` instead. This parameter is maintained
            for backward compatibility and accepts raw GMT CLI strings for the ``-Tm``
            option.
    rose
        Draw a map directional rose on the map.

        .. deprecated:: v0.19.0

            Use :meth:`pygmt.Figure.directional_rose` instead. This parameter is
            maintained for backward compatibility and accepts raw GMT CLI strings for
            the ``-Td`` option.
    box
        Draw a background box behind the scalebar, directional rose, or magnetic rose.

        .. deprecated:: v0.19.0

            Use the ``box`` parameter in :meth:`pygmt.Figure.scalebar`,
            :meth:`pygmt.Figure.directional_rose`, or :meth:`pygmt.Figure.magnetic_rose`
            instead. This parameter is maintained for backward compatibility and accepts
            either a :class:`pygmt.params.Box` object, a raw GMT CLI string, or ``True``
            for the ``-F`` option. On :meth:`pygmt.Figure.basemap`, it only applies when
            used together with the legacy ``map_scale``, ``rose``, or ``compass``
            parameters.
    $verbose
    $panel
    $coltypes
    $perspective
    $transparency
    """
    self._activate_figure()

    for name, value, recommendation in (
        ("map_scale", map_scale, "Figure.scalebar"),
        ("compass", compass, "Figure.magnetic_rose"),
        ("rose", rose, "Figure.directional_rose"),
    ):
        if value is not None and value is not False:
            warnings.warn(
                f"The {name!r} parameter has been deprecated since v0.19.0. Use {recommendation!r} instead.",
                category=FutureWarning,
                stacklevel=2,
            )

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),  # Deprecated.
        Jz=Alias(zscale, name="zscale"),
        JZ=Alias(zsize, name="zsize"),
        L=Alias(map_scale, name="map_scale"),  # Deprecated.
        Td=Alias(rose, name="rose"),  # Deprecated.
        Tm=Alias(compass, name="compass"),  # Deprecated.
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
