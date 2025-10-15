"""
wiggle - Plot z=f(x,y) anomalies along tracks.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


def _parse_fills(fillpositive, fillnegative):
    """
    Parse the fillpositive and fillnegative parameters.

    >>> _parse_fills("red", "blue")
    ['red+p', 'blue+n']
    >>> _parse_fills(None, "blue")
    'blue+n'
    >>> _parse_fills("red", None)
    'red+p'
    >>> _parse_fills(None, None)
    """
    _fills = []
    if fillpositive is not None:
        _fills.append(fillpositive + "+p")
    if fillnegative is not None:
        _fills.append(fillnegative + "+n")

    match len(_fills):
        case 0:
            return None
        case 1:
            return _fills[0]
        case 2:
            return _fills


@fmt_docstring
@use_alias(
    B="frame",
    D="position",
    T="track",
    W="pen",
    Z="scale",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    g="gap",
    h="header",
    i="incols",
    p="perspective",
    w="wrap",
)
@kwargs_to_strings(i="sequence_comma", p="sequence")
def wiggle(  # noqa: PLR0913
    self,
    data: PathLike | TableLike | None = None,
    x=None,
    y=None,
    z=None,
    fillpositive=None,
    fillnegative=None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot z=f(x,y) anomalies along tracks.

    Takes a matrix, (x, y, z) triplets, or a file name as input and plots z
    as a function of distance along track.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full GMT docs at :gmt-docs:`wiggle.html`.

    {aliases}
       - G = **+p**: fillpositive, **+n**: fillnegative
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

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
        Set color or pattern for filling positive wiggles [Default is no fill].
    fillnegative : str
        Set color or pattern for filling negative wiggles [Default is no fill].
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

    _fills = _parse_fills(fillpositive, fillnegative)

    aliasdict = AliasSystem(
        G=Alias(_fills, name="fillpositive/fillnegative"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(
            check_kind="vector", data=data, x=x, y=y, z=z, mincols=3
        ) as vintbl:
            lib.call_module(
                module="wiggle", args=build_arg_list(aliasdict, infile=vintbl)
            )
