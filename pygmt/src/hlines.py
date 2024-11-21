"""
hlines - Plot horizontal lines.
"""

from collections.abc import Sequence

import numpy as np
from pygmt.exceptions import GMTInvalidInput

__doctest_skip__ = ["hlines"]


def hlines(
    self,
    y: float | Sequence[float],
    xmin: float | Sequence[float] | None = None,
    xmax: float | Sequence[float] | None = None,
    pen: str | None = None,
    label: str | None = None,
    transparency: float | None = None,
    no_clip: bool = False,
    perspective: str | bool | None = None,
):
    """
    Plot one or multiple horizontal line(s).

    This method is a high-level wrapper around :meth:`pygmt.Figure.plot`, focusing on
    plotting horizontal lines at Y-coordinates specified by the ``y`` parameter. The
    ``y`` parameter can be a single value (for a single horizontal line) or a sequence
    of values (for multiple horizontal lines).

    By default, the X-coordinates of the start and end points of the lines are set to
    be the X-limits of the current plot, but this can be overridden by specifying the
    ``xmin`` and ``xmax`` parameters. ``xmin`` and ``xmax`` can either be a single
    value or a sequence of values. If a single value is provided, it is applied to all
    lines. If a sequence is provided, the length of ``xmin`` and ``xmax`` must match
    the length of ``y``.

    Currently, it only works for Cartesian coordinate system.

    Parameters
    ----------
    y
        Y-coordinates to plot the lines. It can be a single value (for a single line)
        or a sequence of values (for multiple lines).
    xmin
        X-coordinates of the start point of the line(s). If ``None``, defaults to the
        minimum X-limit of the current plot.
    xmax
        X-coordinates of the end point of the line(s). If ``None``, defaults to the
        maximum X-limit of the current plot.
    pen
        Pen attributes for the line(s), in the format of *width,color,style*.
    label
        Label for the line(s), to be displayed in the legend.
    transparency
        Transparency level for the lines, in [0-100] percent range. Defaults to 0, i.e.,
        opaque. Only visible when saving figures in PDF or raster formats.
    no_clip
        If ``True``, do not clip lines outside the plot region.
    perspective
        Select perspective view and set the azimuth and elevation angle of the
        viewpoint. Refer to :method:`pygmt.Figure.plot` for details.

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    >>> fig.hlines(y=1, pen="1p,black", label="Line 1")
    >>> fig.hlines(y=2, xmin=2, xmax=8, pen="1p,red,-", label="Line 2")
    >>> fig.hlines(y=[3, 4], xmin=3, xmax=7, pen="1p,black,.", label="Line 3")
    >>> fig.hlines(y=[5, 6], xmin=4, xmax=9, pen="1p,red", label="Line 4")
    >>> fig.hlines(y=[7, 8], xmin=[0, 1], xmax=[7, 8], pen="1p,blue", label="Line 5")
    >>> fig.legend()
    >>> fig.show()
    """
    self._preprocess()

    # Ensure y is a 1D array.
    _y = np.atleast_1d(y)
    nlines = len(_y)  # Number of lines to plot.

    # Ensure xmin and xmax are 1D arrays.
    # First, determine the x limits if not specified.
    if xmin is None or xmax is None:
        xlimits = self.region[:2]  # Get x limits from current plot region
    _xmin = np.full(nlines, xlimits[0]) if xmin is None else np.atleast_1d(xmin)
    _xmax = np.full(nlines, xlimits[1]) if xmax is None else np.atleast_1d(xmax)

    # Check if xmin/xmax are scalars or have the same length.
    if _xmin.size != _xmax.size:
        msg = "'xmin' and 'xmax' are expected to be scalars or have the same length."
        raise GMTInvalidInput(msg)

    # Ensure _xmin/_xmax match the _y length if they're scalars or have length 1.
    if _xmin.size == 1 and _xmax.size == 1:
        _xmin = np.repeat(_xmin, nlines)
        _xmax = np.repeat(_xmax, nlines)

    # Check if _xmin/_xmax match the _y length.
    if _xmin.size != nlines or _xmax.size != nlines:
        msg = (
            f"'xmin' and 'xmax' are expected to have length '{nlines}' but "
            f"have length '{_xmin.size}' and '{_xmax.size}'."
        )
        raise GMTInvalidInput(msg)

    # Call the plot method to plot the lines.
    for i in range(nlines):
        # Special handling for label.
        # 1. Only specify label when plotting the first line.
        # 2. The -l option can accept comma-separated labels for labeling multiple lines
        #    with auto-coloring enabled. We don't need this feature here, so we need to
        #    replace comma with \054 if the label contains commas.
        _label = label.replace(",", "\\054") if label and i == 0 else None

        # By default, points are connected as great circle arcs in geographic coordinate
        # system and straight lines in Cartesian coordinate system (including polar
        # projection). To plot "horizontal" lines along constant latitude (in geographic
        # coordinate system) or constant radius (in polar projection), we need to
        # resample the line to at least 4 points.
        npoints = 4  # 2 for Cartesian, 4 for geographic and polar projections.
        self.plot(
            x=np.linspace(_xmin[i], _xmax[i], npoints),
            y=[_y[i]] * npoints,
            pen=pen,
            label=_label,
            transparency=transparency,
            no_clip=no_clip,
            perspective=perspective,
            straight_line="m",  # Any one of "m", "p", "r", "t", "x", and "y" works.
        )
