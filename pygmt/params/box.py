"""
The box parameter.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from pygmt.alias import Alias
from pygmt.params.base import BaseParam


@dataclass(repr=False)
class Box(BaseParam):
    """
    Class for the box around GMT embellishments.

    Attributes
    ----------
    clearance
        Set clearances between the embellishment and the box border. Can be either a
        scalar value or a list of two/four values.

        - a scalar value means a uniform clearance in all four directions.
        - a list of two values means separate clearances in x- and y- directions.
        - a list of four values means separate clearances for left/right/bottom/top.
    fill
        Fill for the box. None means no fill.

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

    """
    The GMT syntax:

    [+c<clearance(s)>]
    [+g<fill>]
    [+i[[<gap>/]<pen>]]
    [+p[<pen>]]
    [+r[<radius>]]
    [+s[<dx>/<dy>/][<fill>]]
    """
    clearance: float | str | Sequence[float | str] | None = None
    fill: str | None = None
    inner_gap: float | str | None = None
    inner_pen: str | None = None
    pen: str | None = None
    radius: float | bool | None = False
    shading_offset: Sequence[float | str] | None = None
    shading_fill: str | None = None

    @property
    def innerborder(self) -> str | None:
        """
        innerborder="{inner_gap}/{inner_pen}"
        """
        return [v for v in (self.inner_gap, self.inner_pen) if v is not None] or None

    @property
    def shading(self) -> str | None:
        """
        shading="{shading_offset}/{shading_fill}"
        """
        args = (
            [*self.shading_offset, self.shading_fill]
            if self.shading_offset
            else [self.shading_fill]
        )
        return [v for v in args if v is not None] or None

    @property
    def _aliases(self):
        return [
            Alias(self.clearance, prefix="+c", separator="/"),
            Alias(self.fill, prefix="+g"),
            Alias(self.innerborder, prefix="+i", separator="/"),
            Alias(self.pen, prefix="+p"),
            Alias(self.radius, prefix="+r"),
            Alias(self.shading, prefix="+s", separator="/"),
        ]
