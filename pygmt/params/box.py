"""
The Box class for specifying the box around GMT embellishments.
"""

import dataclasses
from collections.abc import Sequence

from pygmt.alias import Alias
from pygmt.exceptions import GMTInvalidInput, GMTValueError
from pygmt.helpers import is_nonstr_iter
from pygmt.params.base import BaseParam

__doctest_skip__ = ["Box"]


@dataclasses.dataclass(repr=False)
class Box(BaseParam):
    """
    Class for specifying the box around GMT embellishments.

    Parameters
    ----------
    clearance
        Set clearances between the embellishment and the box border. It can be either a
        scalar value or a sequence of two/four values.

        - a scalar value means a uniform clearance in all four directions.
        - a sequence of two values means separate clearances in x- and y-directions.
        - a sequence of four values means separate clearances for left/right/bottom/top.
    fill
        Fill for the box [Default is no fill].
    inner_gap
        Gap between the outer and inner borders [Default is ``"2p"``].
    inner_pen
        Pen attributes for the inner border [Default to :gmt-term:`MAP_DEFAULT_PEN`].
    pen
        Pen attributes for the box outline.
    radius
        Draw a rounded rectangular border instead of sharp. Passing a value with unit
        to control the corner radius [Default is ``"6p"``].
    shade_offset
        Place an offset background shaded region behind the box. A sequence of two
        values (dx, dy) indicates the shift relative to the foreground frame [Default is
        ``("4p", "-4p")``].
    shade_fill
        Fill for the shaded region [Default is ``"gray50"``].

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Box
    >>> fig = pygmt.Figure()
    >>> fig.logo(box=Box(pen="1p", radius="5p", shade_offset=("5p", "5p")))
    >>> fig.show()
    """

    clearance: float | str | Sequence[float | str] | None = None
    fill: str | None = None
    inner_gap: float | str | None = None
    inner_pen: str | None = None
    pen: str | None = None
    radius: str | bool = False
    shade_offset: Sequence[float | str] | None = None
    shade_fill: str | None = None

    def _validate(self):
        """
        Validate the parameters.
        """
        # inner_pen is required when inner_gap is set.
        if self.inner_gap is not None and self.inner_pen is None:
            msg = "Parameter 'inner_pen' is required when 'inner_gap' is set."
            raise GMTInvalidInput(msg)

        # shade_offset must be a sequence of two values or None.
        if self.shade_offset and not (
            is_nonstr_iter(self.shade_offset) and len(self.shade_offset) == 2
        ):
            raise GMTValueError(
                self.shade_offset,
                description="value for parameter 'shade_offset'",
                reason="Must be a sequence of two values (dx, dy) or None.",
            )

    @property
    def _innerborder(self) -> list[str | float] | None:
        """
        Inner border of the box, formatted as a list of 1-2 values, or None.
        """
        return [v for v in (self.inner_gap, self.inner_pen) if v is not None] or None

    @property
    def _shade(self) -> list[str | float] | None:
        """
        Shading for the box, formatted as a list of 1-3 values, or None.
        """
        _shade_offset = self.shade_offset or []
        return [v for v in (*_shade_offset, self.shade_fill) if v is not None] or None

    @property
    def _aliases(self):
        """
        Aliases for the parameter.
        """
        return [
            Alias(self.clearance, name="clearance", prefix="+c", sep="/", size=(2, 4)),
            Alias(self.fill, name="fill", prefix="+g"),
            Alias(self._innerborder, name="inner_gap/inner_pen", prefix="+i", sep="/"),
            Alias(self.pen, name="pen", prefix="+p"),
            Alias(self.radius, name="radius", prefix="+r"),
            Alias(self._shade, name="shade_offset/shade_fill", prefix="+s", sep="/"),
        ]
