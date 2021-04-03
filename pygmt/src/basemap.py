"""
basemap - Plot base maps and frames for the figure.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    args_in_kwargs,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    Jz="zscale",
    JZ="zsize",
    B="frame",
    L="map_scale",
    Td="rose",
    Tm="compass",
    U="timestamp",
    V="verbose",
    X="xshift",
    Y="yshift",
    c="panel",
    f="coltypes",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def basemap(self, **kwargs):
    r"""
    Plot base maps and frames for the figure.

    Creates a basic or fancy basemap with axes, fill, and titles. Several
    map projections are available, and the user may specify separate
    tick-mark intervals for boundary annotation, ticking, and [optionally]
    gridlines. A simple map scale or directional rose may also be plotted.

    At least one of the parameters ``frame``, ``map_scale``, ``rose`` or
    ``compass`` must be specified.

    Full option list at :gmt-docs:`basemap.html`

    {aliases}

    Parameters
    ----------
    {J}
    zscale/zsize : float or str
        Set z-axis scaling or z-axis size.
    {R}
    {B}
    map_scale : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *length*.
        Draws a simple map scale centered on the reference point specified.
    rose : str
        Draws a map directional rose on the map at the location defined by
        the reference and anchor points.
    compass : str
        Draws a map magnetic rose on the map at the location defined by the
        reference and anchor points
    {U}
    {V}
    {XY}
    {c}
    {f}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    if not args_in_kwargs(args=["B", "L", "Td", "Tm", "c"], kwargs=kwargs):
        raise GMTInvalidInput(
            "At least one of frame, map_scale, compass, rose, or panel must be specified."
        )
    with Session() as lib:
        lib.call_module("basemap", build_arg_string(kwargs))
