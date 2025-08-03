"""
The Box class for specifying the box around GMT embellishments.
"""

import dataclasses
from collections.abc import Sequence

from pygmt.alias import Alias
from pygmt.exceptions import GMTValueError
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Box(BaseParam):
    """
    Class for specifying the box around GMT embellishments.

    Attributes
    ----------
    clearance
        Set clearances between the embellishment and the box border. It can be either a
        scalar value or a sequence of two/four values.

        - a scalar value means a uniform clearance in all four directions.
        - a sequence of two values means separate clearances in x- and y-directions.
        - a sequence of four values means separate clearances for left/right/bottom/top.
    fill
        Fill for the box. Default is no fill.
    pen
        Pen attributes for the box outline.
    radius
        Draw a rounded rectangular border instead of sharp. Passing a value with unit
        to control the corner radius [Default is ``"6p"``].
    inner_gap
        Gap between the outer and inner borders. Default is ``"2p"``.
    inner_pen
        Pen attributes for the inner border. Default to :gmt-term:`MAP_DEFAULT_PEN`.
    shading_offset
        Place an offset background shaded region behind the box. A sequence of two
        values (dx, dy) indicates the shift relative to the foreground frame. Default is
        ``("4p", "-4p")``.
    shading_fill
        Fill for the shading region. Default is ``"gray50"``.

    Examples
    --------
    >>> from pygmt.params import Box
    >>> str(Box(fill="red@20"))
    '+gred@20'
    >>> str(Box(clearance=(0.2, 0.2), fill="red@20", pen="blue"))
    '+c0.2/0.2+gred@20+pblue'
    >>> str(Box(clearance=(0.2, 0.2), pen="blue", radius=True))
    '+c0.2/0.2+pblue+r'
    >>> str(Box(clearance=(0.1, 0.2, 0.3, 0.4), pen="blue", radius="10p"))
    '+c0.1/0.2/0.3/0.4+pblue+r10p'
    >>> str(
    ...     Box(
    ...         clearance=0.2,
    ...         pen="blue",
    ...         radius="10p",
    ...         shading_offset=("5p", "5p"),
    ...         shading_fill="lightred",
    ...     )
    ... )
    '+c0.2+pblue+r10p+s5p/5p/lightred'
    >>> str(Box(clearance=0.2, inner_gap="2p", inner_pen="1p,red", pen="blue"))
    '+c0.2+i2p/1p,red+pblue'
    >>> str(Box(clearance=0.2, shading_offset=("5p", "5p"), shading_fill="lightred"))
    '+c0.2+s5p/5p/lightred'
    """

    clearance: float | str | Sequence[float | str] | None = None
    fill: str | None = None
    inner_gap: float | str | None = None
    inner_pen: str | None = None
    pen: str | None = None
    radius: str | bool = False
    shading_offset: Sequence[float | str] | None = None
    shading_fill: str | None = None

    def _validate(self):
        """
        Validate the parameters.
        """
        # shading_offset must be a sequence of two values or None.
        if self.shading_offset and (
            not isinstance(self.shading_offset, Sequence)
            or len(self.shading_offset) != 2
        ):
            raise GMTValueError(
                self.shading_offset,
                description="value for parameter 'shading_offset'",
                reason="Must be a sequence of two values (dx, dy) or None.",
            )

    @property
    def _innerborder(self) -> list[str | float] | None:
        """
        Inner border of the box, formatted as a list of 1-2 values, or None.
        """
        return [v for v in (self.inner_gap, self.inner_pen) if v is not None] or None

    @property
    def _shading(self) -> list[str | float] | None:
        """
        Shading for the box, formatted as a list of 1-3 values, or None.
        """
        _shading_offset = self.shading_offset or []
        return [
            v for v in (*_shading_offset, self.shading_fill) if v is not None
        ] or None

    @property
    def _aliases(self):
        """
        Aliases for the parameter.
        """
        return [
            Alias(self.clearance, prefix="+c", separator="/", size=(2, 4)),
            Alias(self.fill, prefix="+g"),
            Alias(self._innerborder, prefix="+i", separator="/", size=(1, 2)),
            Alias(self.pen, prefix="+p"),
            Alias(self.radius, prefix="+r"),
            Alias(self._shading, prefix="+s", separator="/", size=(1, 2, 3)),
        ]
