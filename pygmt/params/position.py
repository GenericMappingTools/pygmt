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

    .. figure:: https://github.com/user-attachments/assets/0f3e9b39-7d64-4628-8acb-58fe74ff6fa5
       :width: 400 px

       Positioning of GMT embellishment using the :class:`pygmt.params.Position` class.

    Placing an embellishment on the plot means selecting a *reference point* somewhere
    on the plot, an *anchor point* somewhere on the embellishment, and then positioning
    the embellishment so that the two points overlap. It may be helpful to consider the
    analog of a boat dropping an anchor: The boat navigates to the *reference point* and
    then, depending on where on the boat the *anchor* is located, moves so that the
    *anchor* connection point overlies the *reference point*, then drops the *anchor*.

    There are five different ways to specify the *reference point* on a map, controlled
    by the ``type`` and ``location`` attributes of this class, for complete freedom to
    select any location inside or outside the map.

    ``type="mapcoords"``
        Specify the *reference point* using data coordinates. ``location`` is given as
        (*longitude*, *latitude*). This mechanism is useful when you want to tie the
        location of the embellishment to an actual point best described by data
        coordinates. Example: ``location=(135, 20), type="mapcoords"``.
    ``type="plotcoords"``
        Specify the *reference point* using plot coordinates, i.e., the distances in
        inches, centimeters, or points from the lower left plot origin. This mechanism
        is preferred when you wish to lay out an embellishment using familiar
        measurements of distance from origins. Example:
        ``location=("2c", "2.5c"), type="plotcoords"``.
    ``type="boxcoords"``
        Specify the *reference point* using normalized coordinates, i.e., fractional
        coordinates between 0 and 1 in both the x and y directions. This mechanism
        avoids units and is useful if you want to always place embellishments at
        locations best referenced as fractions of the plot dimensions. Example:
        ``location=(0.2, 0.1), type="boxcoords"``.
    ``type="inside"``
        Specify the *reference point* using one of the nine justification codes. This
        mechanism is preferred when you just want to place the embellishment inside the
        basemap at one of the corners or centered at one of the sides (or even smack in
        the middle). Example: ``location="TL", type="inside"``. When used, the anchor
        point on the map embellishments will default to the same justification, i.e.,
        ``"TL"`` in this example.
    ``type="outside"``
        Same ``type="inside"`` except it implies that the default anchor point is the
        mirror opposite of the justification code. Thus, when using
        ``location="TL", type="outside"``, the anchor point on the map embellishment
        will default to ``"BR"``. This is practical for embellishments that are drawn
        outside of the basemap (like color bars often are).

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
