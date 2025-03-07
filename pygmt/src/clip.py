"""
clip - Create a polygonal clip path.
"""

import contextlib

from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@contextlib.contextmanager
@use_alias(
    A="straight_line",
    B="frame",
    J="projection",
    N="invert",
    R="region",
    W="pen",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def clip(self, data=None, x=None, y=None, **kwargs):
    r"""
    Create a polygonal clip path.

    This function sets a clip path for the figure. The clip path is applied
    to plotting functions that are called within the context manager.

    Full option list at :gmt-docs:`clip.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in either a file name to an ASCII data table, a 2D {table-classes}.
    x/y : 1d arrays
        The x and y coordinates of the clip path.
    {B}
    {J}
    {R}
    straight_line : bool or str
        [**m**\|\ **p**\|\ **x**\|\ **y**\|\ **r**\|\ **t**].
        By default, geographic line segments are connected as great circle
        arcs. To connect them as straight lines, use ``straight_line``.
        Alternatively, add **m** to connect the line by first following a
        meridian, then a parallel. Or append **p** to start following a
        parallel, then a meridian. (This can be practical to connect a line
        along parallels, for example). For Cartesian data, points are
        simply connected, unless you append **x** or **y** to draw
        stair-case curves that whose first move is along *x* or *y*,
        respectively. For polar projection, append **r** or **t** to connect
        staircase curves whose first move is along *r* or *theta*,
        respectively.
    invert : bool
        Invert the sense of what is inside and outside. For example, when
        using a single clip path, use ``invert=True`` to only plot points
        outside to path. Cannot be used with ``frame``.
    {V}
    pen : str
        Draw the output of the clip path using the pen attributes before
        clipping is initiated [Default is no outline].


    Examples
    --------
    >>> import pygmt
    >>>
    >>> # Create x,y data for the clip path
    >>> x = [-60, 60, 60, -60]
    >>> y = [-30, -30, 30, 30]
    >>>
    >>> # Load the 1 degree global earth relief
    >>> grid = pygmt.datasets.load_earth_relief()
    >>>
    >>> # Create a figure and draw the map frame
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region="d", projection="W15c", frame=True)
    >>>
    >>> # Use a "with" statement to initialize the clip context manager
    >>> with fig.clip(x=x, y=y):
    ...     # Map elements under the "with" statement are clipped
    ...     fig.grdimage(grid=grid)
    >>> fig.show()  # doctest: +SKIP
    <IPython.core.display.Image object>
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        try:
            with lib.virtualfile_in(check_kind="vector", data=data, x=x, y=y) as vintbl:
                lib.call_module(
                    module="clip", args=build_arg_list(kwargs, infile=vintbl)
                )
            yield
        finally:
            # End the top most clipping path
            lib.call_module(module="clip", args="-C1")
