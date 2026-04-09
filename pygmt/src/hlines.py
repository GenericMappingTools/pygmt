"""
hlines - Plot horizontal lines.
"""

from collections.abc import Sequence

import numpy as np
from pygmt.exceptions import GMTValueError

__doctest_skip__ = ["hlines"]


def hlines(
    self,
    y: float | Sequence[float],
    xmin: float | Sequence[float] | None = None,
    xmax: float | Sequence[float] | None = None,
    pen: str | None = None,
    label: str | None = None,
    no_clip: bool = False,
    perspective: str | bool | None = None,
):
    """
    Plot one or multiple horizontal line(s).

    This method is a high-level wrapper around :meth:`pygmt.Figure.plot` that focuses on
    plotting horizontal lines at Y-coordinates specified by the ``y`` parameter. The
    ``y`` parameter can be a single value (for a single horizontal line) or a sequence
    of values (for multiple horizontal lines).

    By default, the X-coordinates of the start and end points of the lines are set to
    be the X-limits of the current plot, but this can be overridden by specifying the
    ``xmin`` and ``xmax`` parameters. ``xmin`` and ``xmax`` can be either a single
    value or a sequence of values. If a single value is provided, it is applied to all
    lines. If a sequence is provided, the length of ``xmin`` and ``xmax`` must match
    the length of ``y``.

    The term "horizontal" lines can be interpreted differently in different coordinate
    systems:

    - **Cartesian**: lines are plotted as straight lines.
    - **Polar**: lines are plotted as arcs along a constant radius.
    - **Geographic**: lines are plotted as arcs along parallels (i.e., constant
      latitude).

    Parameters
    ----------
    y
        Y-coordinates to plot the lines. It can be a single value (for a single line)
        or a sequence of values (for multiple lines).
    xmin/xmax
        X-coordinates of the start/end point(s) of the line(s). If ``None``, defaults to
        the X-limits of the current plot. ``xmin`` and ``xmax`` can be either a single
        value or a sequence of values. If a single value is provided, it is applied to
        all lines. If a sequence is provided, the length of ``xmin`` and ``xmax`` must
        match the length of ``y``.
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
    >>> fig.hlines(y=1, pen="1p,black", label="Line at y=1")
    >>> fig.hlines(y=2, xmin=2, xmax=8, pen="1p,red,-", label="Line at y=2")
    >>> fig.hlines(y=[3, 4], xmin=3, xmax=7, pen="1p,black,.", label="Lines at y=3,4")
    >>> fig.hlines(y=[5, 6], xmin=4, xmax=9, pen="1p,red", label="Lines at y=5,6")
    >>> fig.hlines(
    ...     y=[7, 8], xmin=[0, 1], xmax=[7, 8], pen="1p,blue", label="Lines at y=7,8"
    ... )
    >>> fig.legend()
    >>> fig.show()
    """
    self._activate_figure()

    # Determine the x limits from the current plot region if not specified.
    if xmin is None or xmax is None:
        xlimits = self.region[:2]
        if xmin is None:
            xmin = xlimits[0]
        if xmax is None:
            xmax = xlimits[1]

    # Ensure y/xmin/xmax are 1-D arrays.
    _y = np.atleast_1d(y)
    _xmin = np.atleast_1d(xmin)
    _xmax = np.atleast_1d(xmax)

    nlines = len(_y)  # Number of lines to plot.

    # Check if xmin/xmax are scalars or have the expected length.
    if _xmin.size not in {1, nlines} or _xmax.size not in {1, nlines}:
        _value = f"{_xmin.size}, {_xmax.size}"
        raise GMTValueError(
            _value,
            description="size for 'xmin'/'xmax'",
            reason=f"'xmin'/'xmax' are expected to be scalars or have lengths {nlines!r}.",
        )

    # Repeat xmin/xmax to match the length of y if they are scalars.
    if nlines != 1:
        if _xmin.size == 1:
            _xmin = np.repeat(_xmin, nlines)
        if _xmax.size == 1:
            _xmax = np.repeat(_xmax, nlines)

    # Call the Figure.plot method to plot the lines.
    for i in range(nlines):
        # Special handling for label.
        # 1. Only specify a label when plotting the first line.
        # 2. The -l option can accept comma-separated labels for labeling multiple lines
        #    with auto-coloring enabled. We don't need this feature here, so we need to
        #    replace comma with \054 if the label contains commas.
        _label = label.replace(",", "\\054") if label and i == 0 else None

        # By default, points are connected as great circle arcs in geographic coordinate
        # systems and straight lines in Cartesian coordinate systems (including polar
        # projection). To plot "horizontal" lines along constant latitude (in geographic
        # coordinate systems) or constant radius (in polar projection), we need to
        # resample the line to at least 4 points.
        npoints = 4  # 2 for Cartesian, at least 4 for geographic and polar projections.
        self.plot(
            x=np.linspace(_xmin[i], _xmax[i], npoints),
            y=[_y[i]] * npoints,
            pen=pen,
            label=_label,
            no_clip=no_clip,
            perspective=perspective,
            straight_line="x",
        )
