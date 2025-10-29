"""
Histogram - Calculate and plot histograms.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    A="horizontal",
    B="frame",
    C="cmap",
    D="annotate",
    E="barwidth",
    F="center",
    G="fill",
    L="extreme",
    N="distribution",
    Q="cumulative",
    S="stairs",
    T="series",
    W="pen",
    Z="histtype",
    b="binary",
    d="nodata",
    e="find",
    h="header",
    i="incols",
    l="label",
    p="perspective",
    w="wrap",
)
@kwargs_to_strings(T="sequence", i="sequence_comma", p="sequence")
def histogram(
    self,
    data: PathLike | TableLike,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Calculate and plot histograms.

    Full GMT docs at :gmt-docs:`histogram.html`.

    {aliases}
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a Python list, a 2-D
        {table-classes}.
    {projection}
    {region}
    {frame}
    {cmap}
    fill : str
         Set color or pattern for filling bars [Default is no fill].
    {pen}
    {panel}
    annotate : bool or str
        [**+b**][**+f**\ *font*][**+o**\ *off*][**+r**].
        Annotate each bar with the count it represents. Append any of the
        following modifiers: Use **+b** to place the labels beneath the bars
        instead of above; use **+f** to change to another font than the default
        annotation font; use **+o** to change the offset between bar and
        label [Default is ``"6p"``]; use **+r** to rotate the labels from
        horizontal to vertical.
    barwidth : float or str
        *width*\ [**+o**\ *offset*].
        Use an alternative histogram bar width than the default set via
        ``series``, and optionally shift all bars by an *offset*. Here
        *width* is either an alternative width in data units, or the user may
        append a valid plot dimension unit (**c**\|\ **i**\|\ **p**) for a
        fixed dimension instead. Optionally, all bins may be shifted along the
        axis by *offset*. As for *width*, it may be given in data units of
        plot dimension units by appending the relevant unit.
    center : bool
        Center bin on each value. [Default is left edge].
    distribution : bool, float, or str
        [*mode*][**+p**\ *pen*].
        Draw the equivalent normal distribution; append desired
        *pen* [Default is ``"0.25p,black,solid"``].
        The *mode* selects which central location and scale to use:

        * 0 = mean and standard deviation [Default];
        * 1 = median and L1 scale (1.4826 \* median absolute deviation; MAD);
        * 2 = LMS (least median of squares) mode and scale.
    cumulative : bool or str
        [**r**].
        Draw a cumulative histogram by passing ``True``. Use **r** to display
        a reverse cumulative histogram.
    extreme : str
        **l**\|\ **h**\|\ **b**.
        The modifiers specify the handling of extreme values that fall outside
        the range set by ``series``. By default, these values are ignored.
        Append **b** to let these values be included in the first or last
        bins. To only include extreme values below first bin into the first
        bin, use **l**, and to only include extreme values above the last bin
        into that last bin, use **h**.
    stairs : bool
        Draw a stairs-step diagram which does not include the internal bars
        of the default histogram.
    horizontal : bool
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
    {verbose}
    {binary}
    {nodata}
    {find}
    {header}
    {incols}
    {label}
    {perspective}
    {transparency}
    {wrap}
    """
    self._activate_figure()

    aliasdict = AliasSystem().add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
            lib.call_module(
                module="histogram", args=build_arg_list(aliasdict, infile=vintbl)
            )
