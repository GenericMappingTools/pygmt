"""
directional_rose - Add a map directional rose.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position

__doctest_skip__ = ["directional_rose"]


@fmt_docstring
def directional_rose(
    self,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    width: float | str | None = None,
    fancy: Literal[1, 2, 3] | bool = False,
    labels: Sequence[str] | bool = False,
    box: Box | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: str | bool = False,
    transparency: float | None = None,
):
    """
    Add a directional rose on the map.

    Parameters
    ----------
    position
        Position of the directional rose on the plot. It can be specified in multiple
        ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x and y coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the bottom-left corner of the plot.
    width
        Width of the rose in plot coordinates, or append unit ``%`` for a size in
        percentage of plot width [Default is 10%].
    fancy
        Get a fancy rose. The fanciness level can be set to 1, 2, or 3:

        - Level 1 draws the two principal E-W, N-S orientations
        - Level 2 adds the two intermediate NW-SE and NE-SW orientations
        - Level 3 adds the four minor orientations WNW-ESE, NNW-SSE, NNE-SSW, and
          ENE-WSW

        If set to ``True``, defaults to level 1.
    labels
        A sequence of four strings to label the cardinal points W, E, S, N. Use an empty
        string to skip a specific label. If set to ``True``, default labels are used
        (``["W", "E", "S", "N"]`` for a fancy rose and ``["", "", "", "N"]`` for a
        simple rose).
    box
        Draw a background box behind the directional rose. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    $verbose
    $panel
    $perspective
    $transparency

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 80, 0, 30], projection="M10c", frame=True)
    >>> fig.directional_rose()
    >>> fig.show()
    """
    self._activate_figure()

    position = _parse_position(
        position,
        kwdict={"width": width, "fancy": fancy, "labels": labels},
        default=Position("BL", cstype="inside"),  # Default to BL.
    )

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
        Td=[
            Alias(position, name="position"),
            Alias(width, name="width", prefix="+w"),
            Alias(fancy, name="fancy", prefix="+f"),
            Alias(labels, name="labels", prefix="+l", sep=",", size=4),
        ],
    ).add_common(
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
