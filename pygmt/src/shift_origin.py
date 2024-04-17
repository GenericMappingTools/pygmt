"""
shift_origin - Shift plot origin in x and/or y directions.
"""

from __future__ import annotations

from pygmt import Figure
from pygmt.clib import Session
from pygmt.helpers import build_arg_string


class shift_origin(Figure):  # noqa: N801
    r"""
    Shift plot origin in x and/or y directions.

    This method shifts the plot origin relative to the current origin by *xshift* and
    *yshift* in x and y directions, respectively. Optionally, append the length unit
    (**c** for centimeters, **i** for inches, or **p** for points) to the shifts.
    Default unit if not explicitly given is **c**, but can be changed to other units via
    :gmt-term:`PROJ_LENGTH_UNIT`.

    For *xshift*, a special character **w** can also be used, which represents the
    bounding box **width** of the previous plot. The full syntax is
    [[±][*f*]\ **w**\ [/\ *d*\ ]±]\ *xoff*, where optional signs, factor *f* and divisor
    *d* can be used to compute an offset that may be adjusted further by ±\ *xoff*.
    Assuming that the previous plot has a width of 10 centimeters, here are some example
    values for *xshift*:

    - ``"w"``: x-shift is 10 cm
    - ``"w+2c"``: x-shift is 10+2=12 cm
    - ``"2w+3c"``: x-shift is 2*10+3=23 cm
    - ``"w/2-2c"``: x-shift is 10/2-2=3 cm

    Similarly, for *yshift*, a special character **h** can also be used, which is the
    bounding box **height** of the previous plot.

    **Note**: The previous plot bounding box refers to the last object plotted, which
    may be a basemap, image, logo, legend, colorbar, etc.

    Parameters
    ----------
    xshift
        Shift plot origin in x direction.
    yshift
        Shift plot origin in y direction.

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    >>> # Shift the plot origin in x direction by 12 cm
    >>> fig.shift_origin(xshift=12)
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X14c/10c", frame=True)
    >>> # Shift the plot origin in x direction based on the previous plot width
    >>> # Here, the width is 14 cm, and xshift is 16 cm
    >>> fig.shift_origin(xshift="w+2c")
    >>> fig.show()
    """

    def __init__(
        self, xshift: float | str | None = None, yshift: float | str | None = None
    ):
        # self._preprocess()  # pylint: disable=protected-access

        kwargs = {"T": True}
        if xshift:
            kwargs["X"] = xshift
        if yshift:
            kwargs["Y"] = yshift
        with Session() as lib:
            lib.call_module(module="plot", args=build_arg_string(kwargs))
            self.saved_xshift = lib.get_common("X")  # False or xshift in inches
            self.saved_yshift = lib.get_common("Y")  # False or yshift in inches

    def __enter__(self):
        """
        Enter the context manager.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        """
        kwargs = {"T": True}
        if self.saved_xshift:
            kwargs["X"] = f"{-1.0 * self.saved_xshift}i"
        if self.saved_yshift:
            kwargs["Y"] = f"{-1.0 * self.saved_yshift}i"
        with Session() as lib:
            lib.call_module(module="plot", args=build_arg_string(kwargs))
