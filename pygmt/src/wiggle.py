"""
wiggle - Plot z=f(x,y) anomalies along tracks.
"""

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    B="frame",
    D="position",
    G="fillpositive/fillnegative-",
    R="region",
    T="track",
    V="verbose",
    W="pen",
    Z="scale",
    b="binary",
    c="panel",
    d="nodata",
    e="find",
    f="coltypes",
    g="gap",
    h="header",
    i="incols",
    p="perspective",
    t="transparency",
    w="wrap",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def wiggle(
    self,
    data: PathLike | TableLike | None = None,
    x=None,
    y=None,
    z=None,
    fillpositive=None,
    fillnegative=None,
    projection=None,
    **kwargs,
):
    r"""
    Plot z=f(x,y) anomalies along tracks.

    Takes a matrix, (x, y, z) triplets, or a file name as input and plots z
    as a function of distance along track.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full GMT docs at :gmt-docs:`wiggle.html`.

    {aliases}
       - J=projection

    Parameters
    ----------
    x/y/z : 1-D arrays
        The arrays of x and y coordinates and z data points.
    data
        Pass in either a file name to an ASCII data table, a 2-D
        {table-classes}.
        Use parameter ``incols`` to choose which columns are x, y, z,
        respectively.
    {projection}
    {region}
    scale : str or float
        Give anomaly scale in data-units/distance-unit. Append **c**, **i**,
        or **p** to indicate the distance unit (centimeters, inches, or
        points); if no unit is given we use the default unit that is
        controlled by :gmt-term:`PROJ_LENGTH_UNIT`.
    {frame}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *length*\ [**+j**\ *justify*]\ [**+al**\|\ **r**]\
        [**+o**\ *dx*\ [/*dy*]][**+l**\ [*label*]].
        Define the reference point on the map for the vertical scale bar.
    fillpositive : str
        Set color or pattern for filling positive wiggles
        [Default is no fill].
    fillnegative : str
        Set color or pattern for filling negative wiggles
        [Default is no fill].
    track : str
        Draw track [Default is no track]. Append pen attributes to use
        [Default is ``"0.25p,black,solid"``].
    {verbose}
    pen : str
        Specify outline pen attributes [Default is no outline].
    {binary}
    {panel}
    {nodata}
    {find}
    {coltypes}
    {gap}
    {header}
    {incols}
    {perspective}
    {transparency}
    {wrap}
    """
    self._activate_figure()

    if fillpositive or fillnegative:
        kwargs["G"] = []
        if fillpositive:
            kwargs["G"].append(fillpositive + "+p")
        if fillnegative:
            kwargs["G"].append(fillnegative + "+n")

    aliasdict = AliasSystem(
        J=Alias(projection, name="projection"),
    ).merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(
            check_kind="vector", data=data, x=x, y=y, z=z, mincols=3
        ) as vintbl:
            lib.call_module(
                module="wiggle", args=build_arg_list(aliasdict, infile=vintbl)
            )
