"""
The Position class for positioning GMT embellishments.
"""

import dataclasses
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Position(BaseParam):
    """
    The class for positioning GMT embellishments.
    """

    location: str | tuple[float | str, float | str]
    type: Literal["mapcoords", "inside", "outside", "boxcoords", "plotcoords"]
    anchor: AnchorCode
    offset: Sequence[float | str]

    @property
    def _aliases(self):
        return [
            Alias(
                self.type,
                name="type",
                mapping={
                    "mapcoords": "g",
                    "boxcoords": "n",
                    "plotcoords": "x",
                    "inside": "j",
                    "outside": "J",
                },
            ),
            Alias(self.location, name="location", sep="/", size=2),
            Alias(self.anchor, name="anchor"),
            Alias(self.offset, name="offset", sep="/", size=2),
        ]
