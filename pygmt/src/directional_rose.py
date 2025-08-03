"""
directional_rose - Add a map directional rose.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def directional_rose(  # noqa: PLR0913
    self,
    position,
    position_type: Literal[
        "mapcoords", "inside", "outside", "boxcoords", "plotcoords"
    ] = "mapcoords",
    width: float | str | None = None,
    justify: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    label: Sequence[str] | bool = False,
    fancy: Literal[1, 2, 3] | bool = False,
    box=None,
    perspective=None,
    verbose=None,
    transparency=None,
):
    r"""
    Add a directional rose to the map.

    Parameters
    ----------
    position/position_type
        Location of the rose. The actual meaning of this parameter depends on the
        ``position_type`` parameter.

        - ``position_type="mapcoords"``: *position* is given as (x, y) in user
          coordinates.
        - ``position_type="boxcoords"``: *position* is given as (nx, ny) in normalized
          coordinates, where (0, 0) is the lower-left corner and (1, 1) is the
          upper-right corner of the map.
        - ``position_type="plotcoords"``: *position* is given as (x, y) in plot
          coordinates.
        - ``position_type="inside"``: *position* is given as a two-character
          justification code, meaning the anchor point of the rose is inside the map
          bounding box.
        - ``position_type="outside"``: *position* is given as a two-character
          justification code, but the rose is outside the map bounding box.
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
    anchor_offset
        *offset* or (*offset_x*, *offset_y*).
        Offset the anchor point by *offset_x* and *offset_y*. If a single value *offset*
        is given, *offset_y* = *offset_x* = *offset*.
    justify
        Set the anchor point. Specify a two-character (order independent) code. Choose
        from vertical **T**\(op), **M**\(iddle), or **B**\(ottom) and horizontal
        **L**\(eft), **C**\(entre), or **R**\(ight).

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 80, -30, 30], projection="M10c", frame=True)
    >>> fig.directional_rose(position=(10, 10), position_type="user")
    >>> fig.show()
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
        Td=[
            Alias(
                position_type,
                name="position_type",
                mapping={
                    "mapcoords": "g",
                    "inside": "j",
                    "outside": "J",
                    "boxcoords": "n",
                    "plotcoords": "x",
                },
            ),
            Alias(position, name="position", sep="/"),
            Alias(width, name="width", prefix="+w"),
            Alias(fancy, name="fancy", prefix="+f"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(label, name="label", prefix="+l", sep=",", size=4),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
        ],
        V=Alias(verbose, name="verbose"),
        p=Alias(perspective, name="perspective"),
        t=Alias(transparency, name="transparency"),
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
