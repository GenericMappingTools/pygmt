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
    position,
    position_type: Literal["user", "justify", "mirror", "normalize", "plot"]
    | None = None,
    width: float | str | None = None,
    justify: AnchorCode | None = None,
    offset: Sequence[float | str] | None = None,
    label: Sequence[str] | bool = False,
    fancy: Literal[1, 2, 3] | bool = False,
):
    """
    Add a directional rose to the map.

    Parameters
    ----------
    position
    position_type

    width
        Width of the rose in plot coordinates (append **i** (inch),
        **cm** (centimeters), or **p** (points)), or append % for a size in percentage
        of map width [default is 10%].
    label
        A sequence of four strings to label the cardinal points W,E,S,N. Use a empty
        string to skip a specific label. If set to ``True``, use the default labels
        ``["W", "E", "S", "N"]``.
    fancy
        Get a fancy rose. The fanciness level can be set to 1, 2, or 3:

        - Level 1 draws the two principal E-W, N-S orientations
        - Level 2 adds the two intermediate NW-SE and NE-SW orientations
        - Level 3 adds the eight minor orientations WNW-ESE, NNW-SSE, NNE-SSW, and
          ENE-WSW

        If set to ``True``, it defaults to level 1.
    offset
    justify

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
        Td=[
            Alias(
                position_type,
                name="position_type",
                mapping={
                    "user": "g",
                    "justify": "j",
                    "mirror": "J",
                    "normalize": "n",
                    "plot": "x",
                },
            ),
            Alias(position, name="position", separator="/"),
            Alias(width, name="width", prefix="+w"),
            Alias(fancy, name="fancy", prefix="+f"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(label, name="label", prefix="+l", separator=",", size=4),
            Alias(offset, name="offset", prefix="+o", separator="/", size=[1, 2]),
        ]
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
