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
    {frame}
    {projection}
    {region}
    straight_line
        By default, line segments are drawn as straight lines in the Cartesian and polar
        coordinate systems, and as great circle arcs (by resampling coarse input data
        along such arcs) in the geographic coordinate system. The ``straight_line``
        parameter can control the drawing of line segments. Valid values are:

        - ``True``: Draw line segments as straight lines in geographic coordinate
          systems.
        - ``"x"``: Draw line segments by first along *x*, then along *y*.
        - ``"y"``: Draw line segments by first along *y*, then along *x*.

        Here, *x* and *y* have different meanings depending on the coordinate system:

        - **Cartesian** coordinate system: *x* and *y* are the X- and Y-axes.
        - **Polar** coordinate system: *x* and *y* are theta and radius.
        - **Geographic** coordinate system: *x* and *y* are parallels and meridians.

        .. attention::

            There exits a bug in GMT<=6.5.0 that, in geographic coordinate systems, the
            meaning of *x* and *y* is reversed, i.e., *x* means meridians and *y* means
            parallels. The bug is fixed by upstream
            `PR #8648 <https://github.com/GenericMappingTools/gmt/pull/8648>`__.
    invert : bool
        Invert the sense of what is inside and outside. For example, when using a single
        path, ``invert=True`` means only plot points outside that path will be shown.
        Cannot be used together with ``frame``.
    {verbose}
    pen : str
        Draw outline of clip path using given pen attributes before clipping is
        initiated [Default is no outline].

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
