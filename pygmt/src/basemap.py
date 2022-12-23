"""
basemap - Plot base maps and frames for the figure.
"""

from pygmt.clib import Session
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
    F="box",
    Td="rose",
    Tm="compass",
    U="timestamp",
    V="verbose",
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

    Full option list at :gmt-docs:`basemap.html`

    {aliases}

    Parameters
    ----------
    {projection}
    zscale/zsize : float or str
        Set z-axis scaling or z-axis size.
    {region}
        *Required if this is the first plot command.*
    {frame}
    map_scale : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *length*.
        Draws a simple map scale centered on the reference point specified.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draws a rectangular border around the
        map scale or rose. Alternatively, specify a different pen with
        **+p**\ *pen*. Add **+g**\ *fill* to fill the scale panel [Default is
        no fill]. Append **+c**\ *clearance* where *clearance* is either gap,
        xgap/ygap, or lgap/rgap/bgap/tgap where these items are uniform,
        separate in x- and y-direction, or individual side spacings between
        scale and border. Append **+i** to draw a secondary, inner border as
        well. We use a uniform gap between borders of 2p and the
        :gmt-term:`MAP_DEFAULTS_PEN` unless other values are specified. Append
        **+r** to draw rounded rectangular borders instead, with a 6p corner
        radius. You can override this radius by appending another value.
        Finally, append **+s** to draw an offset background shaded region.
        Here, *dx/dy* indicates the shift relative to the foreground frame
        [Default is 4p/-4p] and shade sets the fill style to use for shading
        [Default is gray50].
    rose : str
        Draws a map directional rose on the map at the location defined by
        the reference and anchor points.
    compass : str
        Draws a map magnetic rose on the map at the location defined by the
        reference and anchor points
    {timestamp}
    {verbose}
    {panel}
    {coltypes}
    {perspective}
    {transparency}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    if not args_in_kwargs(args=["B", "L", "Td", "Tm", "c"], kwargs=kwargs):
        kwargs["B"] = True  # Plotting frames if required arguments not given
    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_string(kwargs))
