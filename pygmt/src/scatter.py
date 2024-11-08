"""
scatter - Scatter plot.
"""

from pygmt.helpers import is_nonstr_iter


def _parse_symbol_size(symbol, size):
    """
    Parse the symbol and size into a style string.

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


def scatter(self, x, y, symbol, size, **kwargs):
    """
    Plot scatter points on a map.

    Parameters
    ----------
    x, y : array-like
        The coordinates of the points to plot.
    symbol : str or sequence
        The symbol to use for the points.
    size : float or sequence
        The size of the points.
    """
    kwargs = self._preprocess(**kwargs)

    # style is a combination of symbol and size, but only if they are string-like
    style = _parse_symbol_size(symbol, size)
    if not is_nonstr_iter(symbol):
        symbol = None
    if not is_nonstr_iter(size):
        size = None

    self.plot(x=x, y=y, style=style, symbol=symbol, size=size, **kwargs)
