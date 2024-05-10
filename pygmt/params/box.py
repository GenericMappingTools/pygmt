"""
The box parameter.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

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
    ...         shading=("5p", "5p", "lightred"),
    ...     )
    ... )
    '+c0.2+pblue+r10p+s5p/5p/lightred'
    >>> str(Box(clearance=0.2, innerborder=("2p", "1p,red"), pen="blue"))
    '+c0.2+i2p/1p,red+pblue'
    """

    clearance: float | str | Sequence[float | str] | None = None
    fill: str | None = None
    innerborder: str | Sequence | None = None
    pen: str | None = None
    radius: float | bool | None = False
    shading: str | Sequence | None = None

    _aliases: ClassVar = [
        Alias("clearance", prefix="+c", separator="/"),
        Alias("fill", prefix="+g"),
        Alias("innerborder", prefix="+i", separator="/"),
        Alias("pen", prefix="+p"),
        Alias("radius", prefix="+r"),
        Alias("shading", prefix="+s", separator="/"),
    ]
