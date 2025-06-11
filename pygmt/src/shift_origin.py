"""
shift_origin - Shift plot origin in x- and/or y-directions.
"""

import contextlib

from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def shift_origin(
    self, xshift: float | str | None = None, yshift: float | str | None = None
):
    r"""
    Shift the plot origin in x- and/or y-directions.

    The shifts can be permanent or temporary. If used as a standalone method, the shifts
    are permanent and apply to all subsequent plots. If used as a context manager, the
    shifts are temporary and only apply to the block of code within the context manager.

    1.  Use as a standalone method to shift the plot origin permanently:

        .. code-block:: python

            fig.shift_origin(...)
            ...  # Other plot commands

    2.  Use as a context manager to shift the plot origin temporarily:

        .. code-block:: python

            with fig.shift_origin(...):
                ...  # Other plot commands
                ...

    The shifts *xshift* and *yshift* in x- and y-directions are relative to the current
    plot origin. The default unit for shifts is centimeters (**c**) but can be changed
    to other units via :gmt-term:`PROJ_LENGTH_UNIT`. Optionally, append the length unit
    (**c** for centimeters, **i** for inches, or **p** for points) to the shifts.

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
        Shift plot origin in x-direction.
    yshift
        Shift plot origin in y-direction.

    Examples
    --------

    Shifting the plot origin permanently:

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 5, 0, 5], projection="X5c/5c", frame=True)
    >>> # Shift the plot origin in x-direction by 6 cm
    >>> fig.shift_origin(xshift=6)
    <contextlib._GeneratorContextManager object at ...>
    >>> fig.basemap(region=[0, 7, 0, 5], projection="X7c/5c", frame=True)
    >>> # Shift the plot origin in x-direction based on the previous plot width.
    >>> # Here, the width is 7 cm, and xshift is 8 cm.
    >>> fig.shift_origin(xshift="w+1c")
    <contextlib._GeneratorContextManager object at ...>
    >>> fig.basemap(region=[0, 10, 0, 5], projection="X10c/5c", frame=True)
    >>> fig.show()

    Shifting the plot origin temporarily:

    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 5, 0, 5], projection="X5c/5c", frame=True)
    >>> # Shift the plot origin in x-direction by 6 cm temporarily. The plot origin will
    >>> # revert back to the original plot origin after the block of code is executed.
    >>> with fig.shift_origin(xshift=6):
    ...     fig.basemap(region=[0, 5, 0, 5], projection="X5c/5c", frame=True)
    >>> # Shift the plot origin in y-direction by 6 cm temporarily.
    >>> with fig.shift_origin(yshift=6):
    ...     fig.basemap(region=[0, 5, 0, 5], projection="X5c/5c", frame=True)
    >>> # Shift the plot origin in x- and y-directions by 6 cm temporarily.
    >>> with fig.shift_origin(xshift=6, yshift=6):
    ...     fig.basemap(region=[0, 5, 0, 5], projection="X5c/5c", frame=True)
    >>> fig.show()
    """
    self._activate_figure()
    kwdict = {"T": True, "X": xshift, "Y": yshift}

    with Session() as lib:
        lib.call_module(module="plot", args=build_arg_list(kwdict))
        _xshift = lib.get_common("X")  # False or xshift in inches
        _yshift = lib.get_common("Y")  # False or yshift in inches

    @contextlib.contextmanager
    def _shift_origin_context():
        """
        An internal context manager to shift the plot origin temporarily.
        """
        try:
            yield
        finally:
            # Revert the plot origin to the original plot origin by shifting it by
            # -xshift and -yshift in inches.
            kwdict = {
                "T": True,
                "X": f"{-1.0 * _xshift}i" if _xshift else None,
                "Y": f"{-1.0 * _yshift}i" if _yshift else None,
            }
            with Session() as lib:
                lib.call_module(module="plot", args=build_arg_list(kwdict))

    return _shift_origin_context()
