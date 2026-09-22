"""
Histogram - Calculate and plot histograms.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.params import Axis, Frame

__doctest_skip__ = ["histogram"]


@fmt_docstring
# TODO(PyGMT>=0.22.0): Remove the deprecated "extreme" parameter.
@deprecate_parameter("extreme", "out_range", "0.20.0", remove_version="0.22.0")
@use_alias(
    D="annotate",
    N="distribution",
    T="series",
    b="binary",
    d="nodata",
    e="find",
    h="header",
    l="label",
    w="wrap",
)
@kwargs_to_strings(T="sequence")
def histogram(
    self,
    data: PathLike | TableLike,
    histtype: Literal[
        "count", "percent", "log_count", "log_percent", "log10_count", "log10_percent"
    ] = "count",
    bar_width: float | str | None = None,
    bar_offset: float | str | None = None,
    cmap: str | bool = False,
    pen: str | None = None,
    fill: str | None = None,
    horizontal: bool = False,
    center: bool = False,
    out_range: Literal["first", "last", "both"] | None = None,
    stairs: bool = False,
    cumulative: bool | Literal["reverse"] = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    incols: int | str | Sequence[int | str] | None = None,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Calculate and plot histograms.

    Full GMT docs at :gmt-docs:`histogram.html`.

    $aliases
       - A = horizontal
       - B = frame
       - C = cmap
       - E = bar_width, **+o**: bar_offset
       - G = fill
       - J = projection
       - L = out_range
       - Q = cumulative
       - R = region
       - S = stairs
       - V = verbose
       - W = pen
       - Z = histtype, **+w**: weight
       - c = panel
       - i = incols
       - p = perspective
       - t = transparency

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a Python list, a 2-D
        $table_classes.
    histtype
        The histogram type to plot:

        - ``"counts"``: counts [Default]
        - ``"percent"``: frequency_percent
        - ``"log_count"``: log (1.0 + count)
        - ``"log_percent"``: log (1.0 + frequency_percent)
        - ``"log10_count"``: log10 (1.0 + count)
        - ``"log10_percent"``: log10 (1.0 + frequency_percent
    $cmap
    pen
        Draw bar outline (or stair-case curve) using the specified pen thickness
        [Default is no outline].
    fill
         Set color or pattern for filling bars [Default is no fill].
    annotate : bool or str
        [**+b**][**+f**\ *font*][**+o**\ *off*][**+r**].
        Annotate each bar with the count it represents. Append any of the
        following modifiers: Use **+b** to place the labels beneath the bars
        instead of above; use **+f** to change to another font than the default
        annotation font; use **+o** to change the offset between bar and
        label [Default is ``"6p"``]; use **+r** to rotate the labels from
        horizontal to vertical.
    bar_width
        Use an alternative histogram bar width than the default set via ``series``. Give
        either an alternative width in data units, or the user may append a
        :ref:`dimension unit <dimension-units>` for a fixed dimension instead.
    bar_offset
        Shift all bars along the axis by a constant value. It may be given in data units
        of plot dimension units by appending the relevant unit. Requires ``bar_width``.
    center
        Center bin on each value specified via ``series`` [Default uses the values to
        define the left edge of each bin].
    distribution : bool, float, or str
        [*mode*][**+p**\ *pen*].
        Draw the equivalent normal distribution; append desired
        *pen* [Default is ``"0.25p,black,solid"``].
        The *mode* selects which central location and scale to use:

        * 0 = mean and standard deviation [Default];
        * 1 = median and L1 scale (1.4826 \* median absolute deviation; MAD);
        * 2 = LMS (least median of squares) mode and scale.
    out_range
        Handle values that fall outside the range set by ``series``. By default, these
        values are ignored. Valid values are:

        - ``"first"``: only include values below first bin into the first bin
        - ``"last"``: only include values above the last bin into that last bin
        - ``"both"``: include values into the first or last bins
    cumulative
        Pass ``True`` to draw a cumulative histogram, or set it to ``"reverse"`` to draw
        a reverse cumulative histogram instead.
    stairs
        Draw a stairs-step diagram which does not include the internal bars of the
        default histogram.
    horizontal
        Plot the histogram horizontally from x = 0 [Default is vertically from y = 0].
        The plot dimensions remain the same, but the two axes are flipped, i.e., the
        x-axis is plotted vertically and the y-axis is plotted horizontally.
    series : int, str, or list
        [*min*\ /*max*\ /]\ *inc*\ [**+n**\ ].
        Set the interval for the width of each bar in the histogram.
    $projection
    $region
    $frame
    $verbose
    $binary
    $panel
    $nodata
    $find
    $header
    $incols
    $label
    $perspective
    $transparency
    $wrap

    Examples
    --------

    >>> import numpy as np
    >>> import pygmt
    >>> # Generate random data from a normal distribution
    >>> rng = np.random.default_rng(seed=100)
    >>> data = rng.normal(loc=100, scale=25, size=1024)
    >>> fig = pygmt.Figure()
    >>> fig.histogram(data=data, frame=True, series=5, fill="red3", pen="1p")
    >>> fig.show()
    """
    if bar_offset is not None and bar_width is None:
        raise GMTParameterError(
            required="bar_width", reason="Required when 'bar_offset' is set."
        )

    aliasdict = AliasSystem(
        A=Alias(horizontal, name="horizontal"),
        C=Alias(cmap, name="cmap"),
        E=[
            Alias(bar_width, name="bar_width"),
            Alias(bar_offset, name="bar_offset", prefix="+o"),
        ],
        F=Alias(center, name="center"),
        G=Alias(fill, name="fill"),
        L=Alias(
            out_range,
            name="out_range",
            mapping={"first": "l", "last": "h", "both": "b"},
        ),
        Q=Alias(cumulative, name="cumulative", mapping={"reverse": "r"}),
        S=Alias(stairs, name="stairs"),
        W=Alias(pen, name="pen"),
        Z=Alias(
            histtype,
            name="histtype",
            mapping={
                "count": "0",
                "percent": "1",
                "log_count": "2",
                "log_percent": "3",
                "log10_count": "4",
                "log10_percent": "5",
            },
        ),
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

    self._activate_figure()
    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
            lib.call_module(
                module="histogram", args=build_arg_list(aliasdict, infile=vintbl)
            )
