"""
The Position class for positioning GMT embellishments.
"""

import dataclasses
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias
from pygmt.exceptions import GMTValueError
from pygmt.helpers import is_nonstr_iter
from pygmt.params.base import BaseParam


@dataclasses.dataclass(repr=False)
class Position(BaseParam):
    """
    Class for positioning embellishments on a plot.

    .. figure:: https://docs.generic-mapping-tools.org/6.6/_images/GMT_anchor.png
       :width: 600 px
       :align: center

       The placement of a GMT embellishment (represented by a green rectangle) in
       relation to the underlying plot (represented by a bisque rectangle).

    This class provides flexible positioning for GMT embellishments (e.g., logo, scale,
    rose) by defining a *reference point* on the plot and an *anchor point* on the
    embellishment. The embellishment is positioned so these two points overlap.

    **Conceptual Model**

    Think of it like dropping an anchor from a boat:

    1. The boat navigates to the *reference point* (a location on the plot)
    2. The *anchor point* (a specific point on the embellishment) is aligned with the
       *reference point*
    3. The embellishment is "dropped" at that position

    **Reference Point**

    The *reference point* can be specified in five different ways using the ``cstype``
    and ``refpoint`` attributes:

    ``cstype="mapcoords"`` Map Coordinates
        Use data/geographic coordinates. Specify ``refpoint`` as
        (*longitude*, *latitude*). Useful when tying the embellishment to a specific
        geographic location.

        **Example:** ``refpoint=(135, 20), cstype="mapcoords"``

    ``cstype="plotcoords"`` Plot Coordinates
        Use plot coordinates as distances from the lower-left plot origin. Specify
        ``refpoint`` as (*x*, *y*) with units (e.g., inches, centimeters, points).
        Useful for precise layout control.

        **Example:** ``refpoint=("2c", "2.5c"), cstype="plotcoords"``

    ``cstype="boxcoords"`` Normalized Coordinates
        Use normalized coordinates where (0, 0) is the lower-left corner and (1, 1) is
        the upper-right corner of the bounding box of the current plot. Specify
        ``refpoint`` as (*nx*, *ny*). Useful for positioning relative to plot dimensions
        without units.

        **Example:** ``refpoint=(0.2, 0.1), cstype="boxcoords"``

    ``cstype="inside"`` Inside Plot
        Select one of the nine :doc:`justification codes </techref/justification_codes>`
        as the *reference point*. The *anchor point* defaults to be the same as the
        *reference point*, so the embellishment is placed inside the plot.

        **Example:** ``refpoint="TL", cstype="inside"``

    ``cstype="outside"`` Outside Plot
        Similar to ``cstype="inside"``, but the *anchor point* defaults to the mirror
        opposite of the *reference point*. Useful for placing embellishments outside
        the plot boundaries (e.g., color bars).

        **Example:** ``refpoint="TL", cstype="outside"``

    **Anchor Point**

    The *anchor point* determines which part of the embellishment aligns with the
    *reference point*. It uses one of nine
    :doc:`justification codes </techref/justification_codes>`.

    Set ``anchor`` explicitly to override these defaults. If not set, the default
    *anchor* behaviors are:

    - ``cstype="inside"``: Same as the *reference point* justification code
    - ``cstype="outside"``: Mirror opposite of the *reference point* justification code
    - Other cstypes: ``"MC"`` (middle center) for map rose and scale, ``"BL"``
      (bottom-left) for other embellishments

    **Offset**

    The ``offset`` parameter shifts the *anchor point* from its default position.
    Offsets are applied to the projected plot coordinates, with positive values moving
    in the direction indicated by the *anchor point*'s justification code. It should be
    a single value (applied to both x and y) or as (*offset_x*, *offset_y*).

    Examples
    --------
    Position the GMT logo at map coordinates (3, 3) with the logo's middle-left point as
    the anchor, offset by (0.2, 0.2):

    >>> import pygmt
    >>> from pygmt.params import Position
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c", frame=True)
    >>> fig.logo(
    ...     position=Position(
    ...         (3, 3), cstype="mapcoords", anchor="ML", offset=(0.2, 0.2)
    ...     ),
    ...     box=True,
    ... )
    >>> fig.show()

    Position the GMT logo at the top-left corner inside the plot:

    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c", frame=True)
    >>> fig.logo(position=Position("TL", cstype="inside", offset="0.2c"), box=True)
    >>> fig.show()
    """

    #: Location of the reference point on the plot. The format depends on ``cstype``:
    #:
    #: - ``cstype="mapcoords"``: (*longitude*, *latitude*)
    #: - ``cstype="plotcoords"``: (*x*, *y*) with plot units
    #: - ``cstype="boxcoords"``: (*nx*, *ny*)
    #: - ``cstype="inside"`` or ``"outside"``:
    #:   :doc:`2-character justification codes </techref/justification_codes>`
    refpoint: Sequence[float | str] | AnchorCode

    #: cstype of the reference point. Valid values are:
    #:
    #: - ``"mapcoords"``: Map/Data coordinates
    #: - ``"plotcoords"``: Plot coordinates
    #: - ``"boxcoords"``: Normalized coordinates
    #: - ``"inside"`` or ``"outside"``: Justification codes
    #:
    #: If not specified, defaults to ``"inside"`` if ``refpoint`` is a justification
    #: code; otherwise defaults to ``"plotcoords"``.
    cstype: (
        Literal["mapcoords", "inside", "outside", "boxcoords", "plotcoords"] | None
    ) = None

    #: Anchor point on the embellishment using a
    #: :doc:`2-character justification code </techref/justification_codes>`.
    #: If ``None``, defaults are applied based on ``cstype`` (see above).
    anchor: AnchorCode | None = None

    #: Offset for the anchor point as a single value or (*offset_x*, *offset_y*).
    #: If a single value is given, the offset is applied to both x and y directions.
    offset: float | str | Sequence[float | str] | None = None

    def _validate(self):
        """
        Validate the parameters.
        """
        _valid_anchors = {f"{h}{v}" for v in "TMB" for h in "LCR"} | {
            f"{v}{h}" for v in "TMB" for h in "LCR"
        }

        # Default to "inside" if cstype is not specified and location is an anchor code.
        if self.cstype is None:
            self.cstype = "inside" if isinstance(self.refpoint, str) else "plotcoords"

        # Validate the location based on cstype.
        match self.cstype:
            case "mapcoords" | "plotcoords" | "boxcoords":
                if not is_nonstr_iter(self.refpoint) or len(self.refpoint) != 2:
                    raise GMTValueError(
                        self.refpoint,
                        description="reference point",
                        reason="Expect a sequence of two values.",
                    )
            case "inside" | "outside":
                if self.refpoint not in _valid_anchors:
                    raise GMTValueError(
                        self.refpoint,
                        description="reference point",
                        reason="Expect a valid 2-character justification code.",
                    )
        # Validate the anchor if specified.
        if self.anchor is not None and self.anchor not in _valid_anchors:
            raise GMTValueError(
                self.anchor,
                description="anchor point",
                reason="Expect a valid 2-character justification code.",
            )

    @property
    def _aliases(self):
        return [
            Alias(
                self.cstype,
                name="cstype",
                mapping={
                    "mapcoords": "g",
                    "boxcoords": "n",
                    "plotcoords": "x",
                    "inside": "j",
                    "outside": "J",
                },
            ),
            Alias(self.refpoint, name="refpoint", sep="/", size=2),
            Alias(self.anchor, name="anchor", prefix="+j"),
            Alias(self.offset, name="offset", prefix="+o", sep="/", size=2),
        ]
