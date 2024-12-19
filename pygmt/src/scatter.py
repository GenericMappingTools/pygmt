"""
scatter - Plot scatter points.
"""

from collections.abc import Sequence

from pygmt.helpers import fmt_docstring, is_nonstr_iter


def _parse_symbol_size(
    symbol: str | Sequence[str], size: float | str | Sequence[float | str]
) -> str:
    """
    Parse the 'symbol' and 'size' parameter into GMT's style string.

    Examples
    --------
    >>> _parse_symbol_size("c", 0.2)
    'c0.2'
    >>> _parse_symbol_size("c", "0.2c")
    'c0.2c'
    >>> _parse_symbol_size("c", [0.2, 0.3])
    'c'
    >>> _parse_symbol_size(["c", "t"], "0.2c")
    '0.2c'
    >>> _parse_symbol_size(["c", "t"], [0.2, 0.3])
    ''
    """
    return "".join(f"{arg}" for arg in [symbol, size] if not is_nonstr_iter(arg))


@fmt_docstring
def scatter(  # noqa: PLR0913
    self,
    x,
    y,
    symbol: str | Sequence[str],
    size: float | str | Sequence[float | str],
    fill: str | Sequence[float] | None = None,
    intensity: float | Sequence[float] | None = None,
    transparency: float | Sequence[float] | None = None,
    cmap: str | None = None,
    pen: str | float | None = None,
    no_clip: bool = False,
    perspective=None,
):
    """
    Plot scatter points.

    It can plot data points with constant or varying symbols, sizes, colors,
    transparencies, and intensities. The parameters ``symbol``, ``size``, ``fill``,
    ``intensity``, and ``transparency`` can be a single scalar value or a sequence of
    values with the same length as the number of data points. If a single value is
    given, it is used for all data points. If a sequence is given, different values are
    used for different data points.

    Parameters
    ----------
    x, y
        The data coordinates.
    symbol
        The symbol(s) to use. Valid symbols are:

        - ``-``: X-dash (-)
        - ``+``: Plus
        - ``a``: Star
        - ``c``: Circle
        - ``d``: Diamond
        - ``g``: Octagon
        - ``h``: Hexagon
        - ``i``: Inverted triangle
        - ``n``: Pentagon
        - ``p``: Point
        - ``s``: Square
        - ``t``: Triangle
        - ``x``: Cross
        - ``y``: Y-dash (|)
    size
        The size(s) of the points.
    fill
        Set color or pattern for filling symbols [Default is no fill]. If ``cmap`` is
        used, ``fill`` must be a sequence of values.
    intensity
        The intensity(ies) of the points.
    transparency
        The transparency(ies) of the points.
    cmap
        The colormap to map scalar values in ``fill`` to colors. In this case, ``fill``
        must be a sequence of values.
    pen
        The pen property of the symbol outline.
    no_clip
        If True, do not clip the points that fall outside the frame boundaries.
    {perspective}

    Examples
    --------

    Plot three points with the same symbol and size.

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 3, 0, 3], projection="X10c/5c", frame=True)
    >>> fig.scatter(x=[0, 1, 2], y=[0, 1, 2], symbol="c", size=0.3, fill="red")
    >>> fig.show()

    Plot three points with different sizes and transparencies.

    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 3, 0, 3], projection="X10c/5c", frame=True)
    >>> fig.scatter(
    ...     x=[0, 1, 2],
    ...     y=[0, 1, 2],
    ...     symbol="c",
    ...     size=[0.5, 0.3, 0.2],
    ...     fill="blue",
    ...     transparency=[50, 70, 90],
    ... )
    >>> fig.show()
    """
    self._preprocess()

    # Create GMT plot's "style" from "symbol" and "size".
    _style = _parse_symbol_size(symbol, size)
    # Set "symbol" and "size" to None if they're not sequences.
    _symbol = symbol if is_nonstr_iter(symbol) else None
    _size = size if is_nonstr_iter(size) else None

    # Set "cmap" to True if "fill" is a sequence of values.
    if is_nonstr_iter(fill) and cmap is None:
        cmap = True

    self.plot(
        x=x,
        y=y,
        style=_style,
        symbol=_symbol,
        size=_size,
        fill=fill,
        intensity=intensity,
        transparency=transparency,
        cmap=cmap,
        pen=pen,
        no_clip=no_clip,
        perspective=perspective,
    )
