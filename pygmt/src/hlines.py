"""
hlines - Plot horizontal lines.
"""

from collections.abc import Sequence

import numpy as np
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import is_nonstr_iter


def hlines(
    self,
    y: int | float | Sequence[int | float],
    xmin=None,
    xmax=None,
    pen=None,
    label=None,
    transparency=None,
    no_clip: bool = False,
    perspective=None,
):
    """
    Plot one or multiple horizontal line(s) at specified y-coordinates.

    This method is a high-level wrapper around :meth:`pygmt.Figure.plot`, to plot one or
    multiple horizontal lines at specified y-coordinates. By default, the lines are
    plotted between the x-limits of the current plot, but this can be overridden by
    specifying the ``xmin`` and ``xmax`` parameters to set the x-coordinates of the
    start and end points of the lines.

    ``y`` can be a single value or a sequence of values. If a single value, the line is
    plotted between ``xmin`` and ``xmax``. Similarly, ``xmin`` and ``xmax`` can be a
    single value or a sequence of values. If a sequence, the length of ``xmin`` and
    ``xmax`` must match the length of ``y``.

    Parameters
    ----------
    y
        Y-coordinates to plot the lines. It can be a single value or a sequence of
        values.
    xmin
        X-coordinates of the start point of the line(s). If ``None``, defaults to the
        minimum x-value of the current plot.
    xmax
        X-coordinates of the end point of the line(s). If ``None``, defaults to the
        maximum x-value of the current plot.
    pen
        Pen attributes for the line(s).
    label
        Label for the line(s), to be displayed in the legend.
    transparency
        Transparency level for the lines, in [0-100] percent range. Defaults to 0, i.e.,
        opaque. Only visible when saving figures in PDF or raster formats.
    no_clip
        If ``True``, do not clip the lines outside the plot region.
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

    # Determine the x limits.
    if xmin is None and xmax is None:
        _xmin, _xmax = self.region[0:2]  # Get x limits from current plot region
        if xmin is None:
            xmin = _xmin
        if xmax is None:
            xmax = _xmax

    _y = np.atleast_1d(y)
    nlines = len(_y)  # Number of lines to plot.
    # Repeat xmin and xmax to match the length of y if they are scalars.
    _xmin = np.atleast_1d(xmin) if is_nonstr_iter(xmin) else np.repeat(xmin, nlines)
    _xmax = np.atleast_1d(xmax) if is_nonstr_iter(xmax) else np.repeat(xmax, nlines)

    # Validate the xmin and xmax arguments.
    if _xmin.size != nlines or _xmax.size != nlines:
        msg = f"'xmin' and 'xmax' are expected to be scalars or have a length of {nlines}."
        raise GMTInvalidInput(msg)

    # Loop over horizontal lines
    for i in range(nlines):
        _label = label if i == 0 else None
        self.plot(
            x=[_xmin[i], _xmax[i]],
            y=[_y[i], _y[i]],
            pen=pen,
            label=_label,
            transparency=transparency,
            no_clip=no_clip,
            perspective=perspective,
        )
