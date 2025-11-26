"""
The Position class for positioning GMT embellishments.
"""

import dataclasses
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias
from pygmt.exceptions import GMTValueError
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Position(BaseParam):
    """
    Class for positioning embellishments on a plot.

    .. figure:: https://docs.generic-mapping-tools.org/dev/_images/GMT_anchor.png
       :width: 600 px
       :align: center

       Positioning of GMT embellishment.

    This class provides flexible positioning for GMT embellishments (e.g., logo, scale,
    rose) by defining a *reference point* on the plot and an *anchor point* on the
    embellishment. The embellishment is positioned so these two points overlap.

    **Conceptual Model**

    Think of it like dropping an anchor from a boat:

    1. The boat navigates to the *reference point* (a location on the plot)
    2. The *anchor point* (a specific point on the embellishment) is aligned with the
       *reference point*
    3. The embellishment is "dropped" at that position

    **Reference Point Types**

    The reference point can be specified in five different ways using the ``type`` and
    ``location`` attributes:

    **type="mapcoords"** (Map Coordinates)
        Use data/geographic coordinates. Set ``location`` as (*longitude*, *latitude*).
        Useful when tying the embellishment to a specific geographic location.

        Example: ``location=(135, 20), type="mapcoords"``.

    **type="plotcoords"** (Plot Coordinates)
        Use plot coordinates as distances from the lower-left plot origin. Specify
        ``location`` as (*x*, *y*) with units (e.g., inches, centimeters, points).
        Useful for precise layout control.

        Example: ``location=("2c", "2.5c"), type="plotcoords"``

    **type="boxcoords"** (Normalized Coordinates)
        Use normalized coordinates where (0, 0) is the lower-left corner and (1, 1) is
        the upper-right corner. Set ``location`` as (*nx*, *ny*) with values between
        0 and 1. Useful for positioning relative to plot dimensions without units.

        Example: ``location=(0.2, 0.1), type="boxcoords"``

    **type="inside"** (Inside Plot)
        Use a :doc:`justification code </techref/justification_codes>` (e.g., ``"TL"``)
        to place the embellishment inside the plot. Set ``location`` to one of the nine
        2-character codes.

        Example: ``location="TL", type="inside"``

    **type="outside"** (Outside Plot)
        Similar to ``type="inside"``, but the anchor point defaults to the mirror
        opposite of the justification code. Useful for placing embellishments outside
        the plot boundaries (e.g., color bars).

        Example: ``location="TL", type="outside"``

    **Anchor Point**

    The anchor point determines which part of the embellishment aligns with the
    reference point. It uses one of nine
    :doc:`justification codes </techref/justification_codes>`.

    Set ``anchor`` explicitly to override these defaults. If not set, the default
    anchor behaviors are:

    - For ``type="inside"``: Same as the reference point justification
    - For ``type="outside"``: Mirror opposite of the reference point justification
    - For other types: ``"MC"`` (middle center) for map rose and scale, ``"BL"``
      (bottom-left) for other embellishments

    Example: ``anchor="TR"`` selects the top-right point of the embellishment.

    **Offset**

    The ``offset`` parameter shifts the anchor point from its default position. Offsets
    are applied to the projected plot coordinates, with positive values moving in the
    direction indicated by the anchor point's justification code.

    Specify as a single value (applied to both x and y) or as (*offset_x*, *offset_y*).

    Examples
    --------
    Position a logo at map coordinates (3, 3) with the logo's middle-left point as the
    anchor, offset by (0.2, 0.2):

    >>> import pygmt
    >>> from pygmt.params import Position
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c", frame=True)
    >>> fig.logo(
    ...     position=Position((3, 3), type="mapcoords", anchor="ML", offset=(0.2, 0.2)),
    ...     box=True,
    ... )
    >>> fig.show()

    Position an embellishment at the top-left corner inside the plot:

    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c", frame=True)
    >>> fig.logo(position=Position("TL", type="inside", offset="0.2c"), box=True)
    >>> fig.show()
    """

    #: Location of the reference point on the plot. The format depends on ``type``:
    #:
    #: - ``type="mapcoords"``: (*longitude*, *latitude*)
    #: - ``type="plotcoords"``: (*x*, *y*) with units (e.g., ``"2c"``)
    #: - ``type="boxcoords"``: (*nx*, *ny*) with values between 0 and 1
    #: - ``type="inside"`` or ``"outside"``: 2-character justification code
    location: Sequence[float | str] | AnchorCode

    #: Coordinate system for the reference point. Valid values are:
    #:
    #: - ``"mapcoords"``: Map/Data coordinates
    #: - ``"plotcoords"``: Plot coordinates
    #: - ``"boxcoords"``: Normalized coordinates
    #: - ``"inside"`` or ``"outside"``: Justification codes
    #:
    #: If not specified, defaults to ``"inside"`` if ``location`` is a justification
    #: code; otherwise defaults to ``"plotcoords"``.
    type: (
        Literal["mapcoords", "inside", "outside", "boxcoords", "plotcoords"] | None
    ) = None

    #: Anchor point on the embellishment using a
    #: :doc:`2-character justification codes </techref/justification_codes>`.
    #: If ``None``, defaults are applied based on ``type`` (see above).
    anchor: AnchorCode | None = None

    #: Offset for the anchor point as a single value or (*offset_x*, *offset_y*).
    #: If a single value is given, the offset is applied to both x and y directions.
    offset: Sequence[float | str] | None = None

    def _validate(self):
        """
        Validate the parameters.
        """
        _valid_anchors = {f"{h}{v}" for v in "TMB" for h in "LCR"} | {
            f"{v}{h}" for v in "TMB" for h in "LCR"
        }

        # Default to "inside" if type is not specified and location is an anchor code.
        if self.type is None:
            self.type = "inside" if isinstance(self.location, str) else "plotcoords"

        # Validate the location based on type.
        match self.type:
            case "mapcoords" | "plotcoords" | "boxcoords":
                if not isinstance(self.location, Sequence) or len(self.location) != 2:
                    raise GMTValueError(
                        self.location,
                        description="reference point",
                        reason="Expect a sequence of two values.",
                    )
            case "inside" | "outside":
                if self.location not in _valid_anchors:
                    raise GMTValueError(
                        self.location,
                        description="reference point",
                        reason="Expect a valid 2-character justification code.",
                    )

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
