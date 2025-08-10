"""
scalebar - Add a scale bar.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def scalebar(  # noqa: PLR0913
    self,
    position,
    length,
    position_type: Literal[
        "mapcoords",
        "boxcoords",
        "plotcoords",
        "inside",
        "outside",
    ] = "mapcoords",
    label_alignment: Literal["left", "right", "top", "bottom"] | None = None,
    scale_position=None,
    justify: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    label: str | bool = False,
    fancy: bool = False,
    unit: bool = False,
    vertical: bool = False,
    box=None,
):
    """
    Add a scale bar.

    Parameters
    ----------
    position/position_type
        Location of the map scale bar. The actual meaning of this parameter depends
        on the ``position_type`` parameter.
        - ``position_type="mapcoords"``: *position* is given as (x, y) in user
          coordinates.
        - ``position_type="boxcoords"``: *position* is given as (nx, ny) in normalized
          coordinates, where (0, 0) is the lower-left corner and (1, 1) is the
          upper-right corner of the plot.
        - ``position_type="plotcoords"``: *position* is given as (x, y) in plot
          coordinates, i.e., the distances in inches, centimeters, or points from the
          lower left plot origin.
        - ``position_type="inside"``: *position* is given as a two-character
          justification code, meaning the anchor point of the rose is inside the plot
          bounding box.
        - ``position_type="outside"``: *position* is given as a two-character
          justification code, but the rose is outside the plot bounding box.

    Parameters
    ----------
    TODO

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Box
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 80, -30, 30], projection="M10c", frame=True)
    >>> fig.scalebar(
    ...     position=(10, 10),
    ...     position_type="mapcoords",
    ...     length=1000,
    ...     fancy=True,
    ...     label="Scale",
    ...     unit=True,
    ... )
    >>> fig.show()
    """
    self._preprocess()

    aliasdict = AliasSystem(
        L=[
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
            Alias(length, name="length", prefix="+w"),
            Alias(
                label_alignment,
                name="label_alignment",
                prefix="+a",
                mapping={"left": "l", "right": "r", "top": "t", "bottom": "b"},
            ),
            Alias(scale_position, name="scale_position", prefix="+c", sep="/"),
            Alias(fancy, name="fancy", prefix="+f"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(label, name="label", prefix="+l"),
            Alias(
                anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=[1, 2]
            ),
            Alias(unit, name="unit", prefix="+u"),
            Alias(vertical, name="vertical", prefix="+v"),
        ],
        F=Alias(box, name="box"),
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
