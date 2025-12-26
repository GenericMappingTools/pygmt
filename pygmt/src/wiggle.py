"""
wiggle - Plot z=f(x,y) anomalies along tracks.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, deprecate_parameter, fmt_docstring, use_alias


@fmt_docstring
@deprecate_parameter(
    "fillpositive", "positive_fill", "v0.18.0", remove_version="v0.20.0"
)
@deprecate_parameter(
    "fillnegative", "negative_fill", "v0.18.0", remove_version="v0.20.0"
)
@use_alias(
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
    w="wrap",
)
def wiggle(  # noqa: PLR0913
    self,
    data: PathLike | TableLike | None = None,
    x=None,
    y=None,
    z=None,
    positive_fill=None,
    negative_fill=None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    transparency: float | None = None,
    perspective: float | Sequence[float] | str | bool = False,
    incols: int | str | Sequence[int | str] | None = None,
    **kwargs,
):
    r"""
    Plot z=f(x,y) anomalies along tracks.

    Takes a matrix, (x, y, z) triplets, or a file name as input and plots z
    as a function of distance along track.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full GMT docs at :gmt-docs:`wiggle.html`.

    $aliases
       - B = frame
       - G = **+p**: positive_fill, **+n**: negative_fill
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - i = incols
       - p = perspective
       - t = transparency

    Parameters
    ----------
    x/y/z : 1-D arrays
        The arrays of x and y coordinates and z data points.
    data
        Pass in either a file name to an ASCII data table, a 2-D
        $table_classes.
        Use parameter ``incols`` to choose which columns are x, y, z,
        respectively.
    scale : str or float
        Give anomaly scale in data-units/distance-unit. Append **c**, **i**,
        or **p** to indicate the distance unit (centimeters, inches, or
        points); if no unit is given we use the default unit that is
        controlled by :gmt-term:`PROJ_LENGTH_UNIT`.
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *length*\ [**+j**\ *justify*]\ [**+al**\|\ **r**]\
        [**+o**\ *dx*\ [/*dy*]][**+l**\ [*label*]].
        Define the reference point on the map for the vertical scale bar.
    positive_fill : str
        Set color or pattern for filling positive wiggles [Default is no fill].
    negative_fill : str
        Set color or pattern for filling negative wiggles [Default is no fill].
    track : str
        Draw track [Default is no track]. Append pen attributes to use
        [Default is ``"0.25p,black,solid"``].
    pen : str
        Specify outline pen attributes [Default is no outline].
    $projection
    $region
    $frame
    $verbose
    $binary
    $panel
    $nodata
    $find
    $coltypes
    $gap
    $header
    $incols
    $perspective
    $transparency
    $wrap
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        G=[
            Alias(positive_fill, name="positive_fill", suffix="+p"),
            Alias(negative_fill, name="negative_fill", suffix="+n"),
        ],
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        i=incols,
        p=perspective,
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
