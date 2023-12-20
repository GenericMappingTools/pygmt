from __future__ import annotations

from typing import TYPE_CHECKING

from dataclass import dataclass
from pygmt.params.base import Alias, BaseParams

if TYPE_CHECKING:
    from collections.abc import Sequence


@dataclass(repr=False)
class Box(BaseParams):
    clearance: float | str | Sequence[float | str] | None = None
    fill: str | None = None
    innerborder: str | Sequence | None = None
    pen: str | None = None
    radius: float | bool | None = False
    shading: str | Sequence | None = None

    aliases = [
        Alias("clearance", "+c", "/"),
        Alias("fill", "+g"),
        Alias("innerborder", "+i", "/"),
        Alias("pen", "+p"),
        Alias("radius", "+r"),
        Alias("shading", "+s", "/"),
    ]
