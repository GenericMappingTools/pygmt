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

    Example
    -------
    >>> import pygmt
    >>> from pygmt.params import Position
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c", frame=True)
    >>> fig.logo(
    ...     position=Position((3, 3), type="mapcoords", anchor="ML", offset=(0.2, 0.2)),
    ...     box=True,
    ... )
    >>> fig.show()
    """

    #: Location of the reference point on the plot. Its meaning depends on the value of
    #: ``type``.
    location: Sequence[float | str] | AnchorCode

    #: The coordinates used to define the reference point. Valid values and meanings for
    #: corresponding ``location`` are:
    #:
    #: - ``"mapcoords"``: ``location`` is specified as (*longitude*, *latitude*) in map
    #:   coordinates.
    #: - ``"boxcoords"``: ``location`` is specified as (*nx*, *ny*) in normalized
    #:   coordinates, i.e., fractional values between 0 and 1 along the x- and y-axes.
    #: - ``"plotcoords"``: ``location`` is specified as (*x*, *y*) in plot coordinates,
    #:   i.e., distances from the lower-left plot origin given in inches, centimeters,
    #:   or points.
    #: - ``"inside"`` or ``"outside"``: ``location`` is one of the nine
    #:   :doc:`two-character justification codes </techref/justification_codes>`,
    #:   indicating a specific location relative to the plot bounding box.
    #:
    #: The default value is ``"plotcoords"``.
    type: Literal["mapcoords", "inside", "outside", "boxcoords", "plotcoords"] = (
        "plotcoords"
    )

    #: Anchor point of the embellishment, using one of the
    #: :doc:`2-character justification codes </techref/justification_codes>`. The
    #: default value depends on ``type``.
    #:
    #: - ``type="inside"``: ``anchor`` defaults to the same as ``location``.
    #: - ``type="outside"``: ``anchor`` defaults to the mirror opposite of ``location``.
    #: - Otherwise, ``anchor`` defaults to ``"MC"`` (middle center).
    anchor: AnchorCode | None = None

    #: Offset for the anchor point. It can be either a single value *offset* or a pair
    #: (*offset_x*, *offset_y*), where *offset_x* and *offset_y* are the offsets in the
    #: x- and y-directions, respectively. If a single value *offset* is given, both
    #: *offset_x* and *offset_y* are set to *offset*.
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
