"""
vlines - Plot vertical lines.
"""

from collections.abc import Sequence

import numpy as np
from pygmt.exceptions import GMTValueError

__doctest_skip__ = ["vlines"]


def vlines(
    self,
    x: float | Sequence[float],
    ymin: float | Sequence[float] | None = None,
    ymax: float | Sequence[float] | None = None,
    pen: str | None = None,
    label: str | None = None,
    no_clip: bool = False,
    perspective: str | bool | None = None,
):
    """
    Plot one or multiple vertical line(s).

    This method is a high-level wrapper around :meth:`pygmt.Figure.plot` that focuses on
    plotting vertical lines at X-coordinates specified by the ``x`` parameter. The ``x``
    parameter can be a single value (for a single vertical line) or a sequence of values
    (for multiple vertical lines).

    By default, the Y-coordinates of the start and end points of the lines are set to be
    the Y-limits of the current plot, but this can be overridden by specifying the
    ``ymin`` and ``ymax`` parameters. ``ymin`` and ``ymax`` can be either a single value
    or a sequence of values. If a single value is provided, it is applied to all lines.
    If a sequence is provided, the length of ``ymin`` and ``ymax`` must match the length
    of ``x``.

    The term "vertical" lines can be interpreted differently in different coordinate
    systems:

    - **Cartesian**: lines are plotted as straight lines.
    - **Polar**: lines are plotted as straight lines along a constant azimuth.
    - **Geographic**: lines are plotted as arcs along meridians (i.e., constant
      longitude).

    Parameters
    ----------
    x
        X-coordinates to plot the lines. It can be a single value (for a single line)
        or a sequence of values (for multiple lines).
    ymin/ymax
        Y-coordinates of the start/end point(s) of the line(s). If ``None``, defaults to
        the Y-limits of the current plot. ``ymin`` and ``ymax`` can either be a single
        value or a sequence of values. If a single value is provided, it is applied to
        all lines. If a sequence is provided, the length of ``ymin`` and ``ymax`` must
        match the length of ``x``.
    pen
        Pen attributes for the line(s), in the format of *width,color,style*.
    label
        Label for the line(s), to be displayed in the legend.
    no_clip
        Do **not** clip lines outside the plot region. Only makes sense in the Cartesian
        coordinate system. [Default is ``False`` to clip lines at the plot region.]
    perspective
        Select perspective view and set the azimuth and elevation angle of the
        viewpoint. Refer to :meth:`pygmt.Figure.plot` for details.

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    >>> fig.vlines(x=1, pen="1p,black", label="Line at x=1")
    >>> fig.vlines(x=2, ymin=2, ymax=8, pen="1p,red,-", label="Line at x=2")
    >>> fig.vlines(x=[3, 4], ymin=3, ymax=7, pen="1p,black,.", label="Lines at x=3,4")
    >>> fig.vlines(x=[5, 6], ymin=4, ymax=9, pen="1p,red", label="Lines at x=5,6")
    >>> fig.vlines(
    ...     x=[7, 8], ymin=[0, 1], ymax=[7, 8], pen="1p,blue", label="Lines at x=7,8"
    ... )
    >>> fig.legend()
    >>> fig.show()
    """
    self._activate_figure()

    # Determine the y limits from the current plot region if not specified.
    if ymin is None or ymax is None:
        ylimits = self.region[2:]
        if ymin is None:
            ymin = ylimits[0]
        if ymax is None:
            ymax = ylimits[1]

    # Ensure x/ymin/ymax are 1-D arrays.
    _x = np.atleast_1d(x)
    _ymin = np.atleast_1d(ymin)
    _ymax = np.atleast_1d(ymax)

    nlines = len(_x)  # Number of lines to plot.

    # Check if ymin/ymax are scalars or have the expected length.
    if _ymin.size not in {1, nlines} or _ymax.size not in {1, nlines}:
        _value = f"{_ymin.size}, {_ymax.size}"
        raise GMTValueError(
            _value,
            description="size for 'ymin'/'ymax'",
            reason=f"'ymin'/'ymax' are expected to be scalars or have lengths {nlines!r}.",
        )

    # Repeat ymin/ymax to match the length of x if they are scalars.
    if nlines != 1:
        if _ymin.size == 1:
            _ymin = np.repeat(_ymin, nlines)
        if _ymax.size == 1:
            _ymax = np.repeat(_ymax, nlines)

    # Call the Figure.plot method to plot the lines.
    for i in range(nlines):
        # Special handling for label.
        # 1. Only specify a label when plotting the first line.
        # 2. The -l option can accept comma-separated labels for labeling multiple lines
        #    with auto-coloring enabled. We don't need this feature here, so we need to
        #    replace comma with \054 if the label contains commas.
        _label = label.replace(",", "\\054") if label and i == 0 else None

        self.plot(
            x=[_x[i], _x[i]],
            y=[_ymin[i], _ymax[i]],
            pen=pen,
            label=_label,
            no_clip=no_clip,
            perspective=perspective,
            straight_line="y",
        )
