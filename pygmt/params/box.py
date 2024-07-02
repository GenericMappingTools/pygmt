"""
Class for the box around GMT embellishments.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

from pygmt.params.base import Alias, BaseParams


@dataclass(repr=False)
class Box(BaseParams):
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

    """

    clearance: float | str | Sequence[float | str] | None = None
    fill: str | None = None
    innerborder: str | Sequence | None = None
    pen: str | None = None
    radius: float | bool | None = False
    shading: str | Sequence | None = None

    __aliases__: ClassVar = [
        Alias("clearance", "+c", "/"),
        Alias("fill", "+g"),
        Alias("innerborder", "+i", "/"),
        Alias("pen", "+p"),
        Alias("radius", "+r"),
        Alias("shading", "+s", "/"),
    ]
