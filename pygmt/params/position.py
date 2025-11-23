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

    #: Specify the reference point on the plot. The method of defining the reference
    #: point is controlled by ``type``, and the exact location is set by ``position``.
    location: Sequence[float | str] | AnchorCode

    #: Specify the type of coordinates used to define the reference point. It can be
    #: one of the following values:
    #:
    #: - ``"mapcoords"``: ``position`` is specified as (*longitude*, *latitude*) in map
    #:   coordinates.
    #: - ``"boxcoords"``: ``position`` is specified as (*nx*, *ny*) in normalized
    #:   coordinates, i.e., fractional values between 0 and 1 along the x- and y-axes.
    #: - ``"plotcoords"``: ``position`` is specified as (*x*, *y*) in plot coordinates,
    #:   i.e., distances from the lower-left plot origin given in inches, centimeters,
    #:   or points.
    #: - ``"inside"`` or ``"outside"``: ``position`` is one of the nine
    #:   :doc:`two-character justification codes </techref/justification_codes>`,
    #:   indicating a specific location relative to the plot bounding box.
    #:
    type: Literal["mapcoords", "inside", "outside", "boxcoords", "plotcoords"]

    #: Specify the anchor point of the GMT logo, using one of the
    #: :doc:`2-character justification codes </techref/justification_codes>`. The
    #: default value depends on ``position_type``.
    #:
    #: - ``position_type="inside"``: ``anchor`` defaults to the same as ``position``.
    #: - ``position_type="outside"``: ``anchor`` defaults to the mirror opposite of
    #:   ``position``.
    #: - Otherwise, ``anchor`` defaults to ``"MC"`` (middle center).
    anchor: AnchorCode | None = None

    #: Specifies an offset for the anchor point as *offset* or (*offset_x*, *offset_y*).
    #: If a single value *offset* is given, both *offset_x* and *offset_y* are set to
    #: *offset*.
    offset: Sequence[float | str] | None = None

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
            Alias(self.anchor, name="anchor", prefix="+j"),
            Alias(self.offset, name="offset", prefix="+o", sep="/", size=2),
        ]
