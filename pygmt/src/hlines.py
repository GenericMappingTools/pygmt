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
    N="no_clip",
    V="verbose",
    W="pen",
    l="label",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(p="sequence")
def hlines(self, y=None, xmin=None, xmax=None, **kwargs):
    """
    Plot one or a collection of horizontal lines.
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
    {V}
    label : str
        Add a legend entry for the line being plotted.
    {p}
    {t}
        *transparency* can also be a 1d array to set varying transparency
        for lines.

    """
    kwargs = self._preprocess(**kwargs)

    y = np.atleast_1d(y)
    list_length = len(y)

    # prepare x values
    def prep_data(xmin, xmax, list_length):
        if xmin is None and xmax is None:
            # get limits from current map boundings if not given via xmin, xmax
            xmin, xmax = self.region[0:2]
            x = np.repeat([[xmin], [xmax]], list_length, axis=1)
        elif xmin is None or xmax is None:
            raise GMTInvalidInput(
                "Must provide both, xmin and xmax if limits are not set automatically."
            )

        # if only a single xmin and xmax without [], repeat to fit
        # size of y
        elif isinstance(xmin, int | float):
            x = np.array([[xmin], [xmax]])
            x = np.repeat(x, list_length, axis=1)
        elif len(xmin) != len(xmax):
            GMTInvalidInput("Must provide same length for xmin and xmax.")
        else:
            x = np.array([xmin, xmax])

        return np.atleast_1d(x)

    def prep_style(kwargs, list_length):
        # prepare labels
        if "l" in kwargs:
            # if several lines belong to the same label, first set all to None
            # then replace first entry by the label given via "l"
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
                kwargs["W"] = np.repeat(kwargs["W"], list_length)
        else:  # use as default if no pen is given (neither single nor series)
            kwargs["W"] = np.repeat("1p,black", list_length)

        return kwargs

    # loop over entries
    x = prep_data(xmin, xmax, list_length)
    kwargs = prep_style(kwargs, list_length)
    kwargs_copy = kwargs.copy()

    for index in range(list_length):
        with Session() as lib:
            if (
                data_kind(None, [x[0][index], x[1][index]], [y[index], y[index]])
                == "vectors"
            ):
                file_context = lib.virtualfile_from_vectors(
                    np.atleast_1d([x[0][index], x[1][index]]), [y[index], y[index]]
                )
            else:
                raise GMTInvalidInput("Unrecognized data type.")

            kwargs["l"] = kwargs_copy["l"][index]
            kwargs["W"] = kwargs_copy["W"][index]

            with file_context as fname:
                lib.call_module("plot", " ".join([fname, build_arg_string(kwargs)]))
