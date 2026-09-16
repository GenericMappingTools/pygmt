"""
Histogram - Calculate and plot histograms.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem, _to_string
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)
from pygmt.params import Axis, Frame


def _alias_option_N(  # ruff: ignore[invalid-function-name]
    distribution=None, distribution_pen=None
):
    """
    Helper function to create the alias for the -N option.

    The ``-N`` option may be repeated to draw several distribution curves, so
    ``distribution`` also accepts a sequence of modes. ``distribution_pen`` is either a
    single pen, used for every curve, or one pen per curve.

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return build_arg_list(AliasSystem(N=_alias_option_N(**kwargs)))
    >>> parse()
    []
    >>> # A single curve
    >>> parse(distribution="mean")
    ['-N0']
    >>> parse(distribution="median", distribution_pen="1p,blue")
    ['-N1+p1p,blue']

    >>> # Multiple curves
    >>> parse(distribution=["mean", "lms"])
    ['-N0', '-N2']

    >>> # A single pen is used for every curve
    >>> parse(distribution=["mean", "lms"], distribution_pen="1p,red")
    ['-N0+p1p,red', '-N2+p1p,red']

    >>> # Several curves, each with its own pen
    >>> parse(
    ...     distribution=["mean", "median", "lms"],
    ...     distribution_pen=["1p,red", "1p,blue", "1p,green"],
    ... )
    ['-N0+p1p,red', '-N1+p1p,blue', '-N2+p1p,green']

    >>> # A pen alone without distribution is ignored.
    >>> parse(distribution_pen="1p,red")
    []

    >>> # Backward compatibility: the legacy syntax combines the mode and the pen into
    >>> # a single string, and is passed through as is.
    >>> parse(distribution="0+p1p,blue")
    ['-N0+p1p,blue']
    >>> parse(distribution=["0+p1p,blue", "1+p1p,red"])
    ['-N0+p1p,blue', '-N1+p1p,red']
    >>> parse(distribution="+p1p,blue")
    ['-N+p1p,blue']
    >>> parse(distribution="1")
    ['-N1']
    >>> parse(distribution=True)
    ['-N']

    >>> # But the legacy syntax cannot be mixed with 'distribution_pen'.
    >>> parse(distribution="0+p1p,blue", distribution_pen="1p,red")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTParameterError: Conflicting parameters: 'distribution_pen' ...

    >>> parse(distribution="invalid")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTValueError: Invalid value for parameter 'distribution': ...

    >>> parse(distribution=["mean", "lms"], distribution_pen=["1p,red"])
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTParameterError: 'distribution_pen' must be a single pen or ...
    """
    # Do nothing if distribution is not specified. Ignoring distribution_pen.
    if distribution is None:
        return Alias(None, name="distribution")

    modes = distribution if is_nonstr_iter(distribution) else [distribution]
    # The legacy syntax gives the mode and the pen as a single string (e.g., "1+p1p,red"
    # or "+p1p,red"), or the mode as a string (e.g. "1"). Pass it as is.
    if any(isinstance(mode, str) and ("+" in mode or mode.isdigit()) for mode in modes):
        if distribution_pen is not None:
            raise GMTParameterError(
                conflicts_with=("distribution_pen", ["distribution"]),
                reason="'distribution' is using the legacy syntax.",
            )
        return Alias(distribution, name="distribution")

    pens = (
        distribution_pen
        if is_nonstr_iter(distribution_pen)
        else [distribution_pen] * len(modes)
    )
    if len(pens) != len(modes):
        raise GMTParameterError(
            reason=(
                "'distribution_pen' must be a single pen or one pen per curve, but "
                f"got {len(pens)} pen(s) for {len(modes)} curve(s)."
            )
        )

    values = []
    for mode, pen in zip(modes, pens, strict=True):
        _mode = _to_string(
            mode, mapping={"mean": 0, "median": 1, "lms": 2}, name="distribution"
        )
        _pen = _to_string(pen, prefix="+p", name="distribution_pen")
        if _mode is None:  # e.g. distribution=False means no curve at all.
            continue
        values.append(_mode if _pen is None else f"{_mode}{_pen}")
    return Alias(values, name="distribution")


@fmt_docstring
# TODO(PyGMT>=0.22.0): Remove the deprecated "extreme" parameter.
@deprecate_parameter("extreme", "out_range", "0.20.0", remove_version="0.22.0")
@use_alias(
    D="annotate",
    F="center",
    T="series",
    Z="histtype",
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
    bar_width: float | str | None = None,
    bar_offset: float | str | None = None,
    cmap: str | bool = False,
    pen: str | None = None,
    fill: str | None = None,
    horizontal: bool = False,
    distribution: Literal["mean", "median", "lms"]
    | Sequence[Literal["mean", "median", "lms"]]
    | None = None,
    distribution_pen: str | Sequence[str] | None = None,
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
       - N = distribution, **+p**: distribution_pen
       - Q = cumulative
       - R = region
       - S = stairs
       - V = verbose
       - W = pen
       - c = panel
       - i = incols
       - p = perspective
       - t = transparency

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a Python list, a 2-D
        $table_classes.
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
        of plot dimension units by appending the relevant unit.
    center : bool
        Center bin on each value. [Default is left edge].
    distribution
        Draw the equivalent normal distribution. Select which central location and scale
        to use:

        - ``"mean"``: mean and standard deviation
        - ``"median"``: median and L1 scale (1.4826 \* median absolute deviation)
        - ``"lms"``: least median of squares (LMS) mode and scale

        Pass a sequence of modes to draw several curves at once, e.g.,
        ``["mean", "lms"]``.

        **Note**: If ``wrap`` is used, only ``"mean"`` is available and the circular
        von Mises distribution is determined instead.
    distribution_pen
        Pen used to draw the distribution curve [Default is ``"0.25p,black,solid"``].
        Pass a sequence of pens to use a different pen for each curve; a single pen is
        used for all of them. If ``distribution`` is not set, this parameter is ignored.
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
    histtype : int or str
        [*type*][**+w**].
        Choose between 6 types of histograms:

        * 0 = counts [Default]
        * 1 = frequency_percent
        * 2 = log (1.0 + count)
        * 3 = log (1.0 + frequency_percent)
        * 4 = log10 (1.0 + count)
        * 5 = log10 (1.0 + frequency_percent).

        To use weights provided as a second data column instead of pure counts,
        append **+w**.
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
        G=Alias(fill, name="fill"),
        L=Alias(
            out_range,
            name="out_range",
            mapping={"first": "l", "last": "h", "both": "b"},
        ),
        N=_alias_option_N(distribution, distribution_pen),
        Q=Alias(cumulative, name="cumulative", mapping={"reverse": "r"}),
        S=Alias(stairs, name="stairs"),
        W=Alias(pen, name="pen"),
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
