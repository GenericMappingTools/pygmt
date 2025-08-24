"""
directional_rose - Add a map directional rose.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def directional_rose(
    self,
    position: Sequence[str | float] | AnchorCode,
    position_type: Literal[
        "mapcoords",
        "boxcoords",
        "plotcoords",
        "inside",
        "outside",
    ] = "plotcoords",
    width: float | str | None = None,
    anchor: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    label: Sequence[str] | bool = False,
    fancy: Literal[1, 2, 3] | bool = False,
):
    r"""
    Add a directional rose on the map.

    The directional rose is plotted at the location defined by the reference point
    (specified by the **position** and *position_type** parameters) and anchor point
    (set by the **anchor** and **anchor_offset** parameters).

    Parameters
    ----------
    position/position_type
        Reference point on the map for the directional rose. The meaning of the
        **position** parameter depends on the **position_type** parameter:

        - ``"mapcoords"``: **position** is given as (x, y) in user coordinates.
        - ``"boxcoords"``: **position** is given as (nx, ny) in normalized coordinates,
          where (0, 0) is the lower-left corner and (1, 1) is the upper-right corner of
          the plot bounding box.
        - ``"plotcoords"``: **position** is given as (x, y) in plot coordinates, i.e.,
          the distances in inches, centimeters, or points from the lower left plot
          origin.
        - ``"inside"`` or ``"outside"``: **position** is the justification code, meaning
          the anchor point of the rose is inside or outside the plot bounding box.
    anchor
        The anchor point of the rose, set by a 2-character justification code.
        The default value depends on the **position_type** parameter.

        - ``position_type="inside"``, **anchor** defaults to the same as **position**.
        - ``position_type="outside"``, **anchor** defaults to the mirror opposite of
          **position**.
        - Otherwise, **anchor** defaults to ``"MC"`` (middle center).
    anchor_offset
        *offset* or (*offset_x*, *offset_y*).
        Offset the anchor point by *offset_x* and *offset_y*. If a single value *offset*
        is given, *offset_y* = *offset_x* = *offset*.
    width
        Width of the rose in plot coordinates (append **i** (inch),
        **cm** (centimeters), or **p** (points)), or append % for a size in percentage
        of map width [Default is 10 %].
    label
        A sequence of four strings to label the cardinal points W,E,S,N. Use an empty
        string to skip a specific label. If set to ``True``, use the default labels
        ``["W", "E", "S", "N"]``.
    fancy
        Get a fancy rose. The fanciness level can be set to 1, 2, or 3:

        - Level 1 draws the two principal E-W, N-S orientations
        - Level 2 adds the two intermediate NW-SE and NE-SW orientations
        - Level 3 adds the four minor orientations WNW-ESE, NNW-SSE, NNE-SSW, and
          ENE-WSW

        If set to ``True``, it defaults to level 1.
    {perspective}
    {verbose}
    {transparency}

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 80, -30, 30], projection="M10c", frame=True)
    >>> fig.directional_rose(position=(10, 10), position_type="mapcoords")
    >>> fig.show()
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        Td=[
            Alias(
                position_type,
                name="position_type",
                mapping={
                    "mapcoords": "g",
                    "boxcoords": "n",
                    "plotcoords": "x",
                    "inside": "j",
                    "outside": "J",
                },
            ),
            Alias(position, name="position", sep="/", size=2),
            Alias(fancy, name="fancy", prefix="+f"),  # +F is not supported yet.
            Alias(anchor, name="anchor", prefix="+j"),
            Alias(label, name="label", prefix="+l", sep=",", size=4),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
            Alias(width, name="width", prefix="+w"),
        ],
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
