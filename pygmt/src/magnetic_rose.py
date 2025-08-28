"""
magnetic_rose - Add a map magnetic rose.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list


def magnetic_rose(  # noqa: PLR0913
    self,
    position: Sequence[str | float] | AnchorCode,
    position_type: Literal[
        "mapcoords",
        "boxcoords",
        "plotcoords",
        "inside",
        "outside",
    ] = "mapcoords",
    width: float | str | None = None,
    justify: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    labels: Sequence[str] | bool = False,
    outer_pen=None,
    inner_pen=None,
    declination=None,
    declination_label=None,
    intervals=None,
):
    """
    Add a magnetic rose to the map.
    """
    self._activate_figure()

    _dec = (
        (declination, declination_label)
        if declination_label is not None
        else declination
    )

    # [+tints]
    aliasdict = AliasSystem(
        Tm=[
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
            Alias(width, name="width", prefix="+w"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
            Alias(labels, name="labels", prefix="+l", sep=",", size=4),
            Alias(outer_pen, name="outer_pen", prefix="+p"),
            Alias(inner_pen, name="inner_pen", prefix="+i"),
            Alias(
                _dec, name="declination/declination_label", prefix="+d", sep="/", size=2
            ),
            Alias(intervals, name="intervals", prefix="+t", sep="/", size=(3, 6)),
        ],
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
