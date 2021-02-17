"""
hlines - Plot horizontal lines.
"""
import numpy as np
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    D="offset",
    J="projection",
    N="no_clip",
    R="region",
    U="timestamp",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    Z="zvalue",
    l="label",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", p="sequence")
def hlines(self, y=None, xmin=None, xmax=None, pen=None, label=None, **kwargs):
    """
    " Plot one or a collection of horizontal lines.

    Takes a single y value or a list of individual y values and optionally
    lower and upper x value limits as input.

    Must provide *y*.

    If y values are given without x limits then the current map boundaries are
    used as lower and upper limits. If only a single set of x limits is given
    then all lines will have the same length, otherwise give x limits for each
    individual line. If only a single label is given then all lines are grouped
    under this label in the legend (if shown). If each line should appear as a
    single entry in the legend, give corresponding labels for all lines
    (same for **pen**).

    Parameters
    ----------
    y : float or 1d array
        The y coordinates or an array of y coordinates of the
        horizontal lines to plot.
    {J}
    {R}
    {B}
    {CPT}
    offset : str
        ``dx/dy``.
        Offset the line locations by the given amounts
        *dx/dy* [Default is no offset]. If *dy* is not given it is set
        equal to *dx*.
    no_clip : bool or str
        ``'[c|r]'``.
        Do NOT clip lines that fall outside map border [Default plots
        lines whose coordinates are strictly inside the map border only].
        The option does not apply to lines which are always
        clipped to the map region. For periodic (360-longitude) maps we
        must plot all lines twice in case they are clipped by the
        repeating boundary. ``no_clip=True`` will turn off clipping and not
        plot repeating lines. Use ``no_clip="r"`` to turn off clipping
        but retain the plotting of such repeating lines, or use
        ``no_clip="c"`` to retain clipping but turn off plotting of
        repeating lines.
    {W}
    {U}
    {V}
    {XY}
    zvalue : str or float
        ``value``.
        Instead of specifying a line color via **pen**, give it a *value*
        via **zvalue** and a color lookup table via **cmap**. Requires
        appending **+z** to **pen** (e.g. ``pen = "5p,+z"``,
        ``zvalue = 0.8``, ``cmap = "viridis"``).
    label : str
        Add a legend entry for the line being plotted.
    {p}
    {t}
        *transparency* can also be a 1d array to set varying transparency
        for lines.
    """

    kwargs = self._preprocess(**kwargs)

    list_length = len(np.atleast_1d(y))

    # prepare x vals
    if xmin is None and xmax is None:
        # get limits from current map boundings if not given via xmin, xmax
        with Session() as lib:
            mapbnds = lib.extract_region()
            x = np.array([[mapbnds[0]], [mapbnds[1]]])
            x = np.repeat(x, list_length, axis=1)
    elif xmin is None or xmax is None:
        raise GMTInvalidInput(
            "Must provide both, xmin and xmax if limits are not set automatically."
        )

    else:
        # if only a single xmin and xmax without [], repeat to fit size of y
        if isinstance(xmin, int) or isinstance(xmin, float):
            x = np.array([[xmin], [xmax]])
            x = np.repeat(x, list_length, axis=1)
        else:
            if len(xmin) != len(xmax):
                GMTInvalidInput("Must provide same length for xmin and xmax.")
            else:
                x = np.array([xmin, xmax])

    # prepare labels
    if "l" in kwargs:
        # if several lines belong to the same label, first take the label,
        # then set all to None and reset the first entry to the given label
        if not isinstance(kwargs["l"], list):
            label2use = kwargs["l"]
            kwargs["l"] = np.repeat(None, list_length)
            kwargs["l"][0] = label2use
    else:
        kwargs["l"] = np.repeat(None, list_length)

    # prepare pens
    if "W" in kwargs:
        # select pen, no series
        if not isinstance(kwargs["W"], list):
            pen2use = kwargs["W"]
            kwargs["W"] = np.repeat(pen2use, list_length)
    else:  # use as default if no pen is given (neither single nor series)
        kwargs["W"] = np.repeat("1p,black", list_length)

    # loop over entries
    kwargs_copy = kwargs.copy()

    for index in range(list_length):
        y2plt = [np.atleast_1d(y)[index], np.atleast_1d(y)[index]]
        x2plt = [np.atleast_1d(x)[0][index], np.atleast_1d(x)[1][index]]
        kind = data_kind(None, x2plt, y2plt)

        with Session() as lib:
            if kind == "vectors":
                file_context = lib.virtualfile_from_vectors(
                    np.atleast_1d(x2plt), np.atleast_1d(y2plt)
                )
            else:
                raise GMTInvalidInput("Unrecognized data type.")

            kwargs["l"] = kwargs_copy["l"][index]
            kwargs["W"] = kwargs_copy["W"][index]

            with file_context as fname:
                arg_str = " ".join([fname, build_arg_string(kwargs)])
                lib.call_module("plot", arg_str)
