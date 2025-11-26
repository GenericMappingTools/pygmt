"""
scalebar - Add a scale bar.
"""

from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInputError
from pygmt.helpers import build_arg_list
from pygmt.params import Box, Position


def scalebar(  # noqa: PLR0913
    self,
    position: Position,
    length: float | str | None = None,
    label_alignment: Literal["left", "right", "top", "bottom"] | None = None,
    scale_position: float | tuple[float, float] | bool = False,
    label: str | bool = False,
    fancy: bool = False,
    unit: bool = False,
    vertical: bool = False,
    box: Box | bool = False,
    perspective: str | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    transparency: float | None = None,
):
    """
    Add a scale bar on the map.

    The scale bar is plotted at the location defined by the reference point (specified
    by the **position** and *position_type** parameters) and anchor point (specified by
    the **anchor** and **anchor_offset** parameters). Refer to
    :doc:`/techref/reference_anchor_points` for details about the positioning.

    Parameters
    ----------
    position
        Specify the location of the scale bar. See :class:`pygmt.params.Position` for
        more details.
    length
        Length of the scale bar in km. You can append different units to the length,
        which are:
        - **e**: meters
        - **f**: feet
        - **k**: kilometers
        - **M**: statute mile
        - **n**: nautical miles
        - **u**: US Survey foot
    scale_position
        Specify the location where on a geographic map the scale applies. It can be:

        - *slat*: Map scale is calculated for latitude *slat*
        - (*slon*, *slat*): Map scale is calculated for latitude *slat* and longitude
          *slon*, which is useful for oblique projections.
        - ``True``: Map scale is calculated for the middle of the map.
        - ``False``: Default to the location of the reference point.
    label
        Text string to use as the scale bar label. If ``False``, no label is drawn. If
        ``True``, the distance unit provided in the **length** parameter (default is km)
        is used as the label. The parameter requires ``fancy=True``.
    label_alignment
        Alignment of the scale bar label. Choose from "left", "right", "top", or
        "bottom". [Default is "top"].
    fancy
        If ``True``, draw a “fancy” scale bar. A fancy scale bar is a segmented bar with
        alternating black and white rectangles. If ``False``, draw a plain scale bar.
    unit
        If ``True``, append the unit to all distance annotations along the scale. For a
        plain scale, this will instead select the unit to be appended to the distance
        length. The unit is determined from the suffix in the **length** or defaults to
        km.
    vertical
        If ``True``, plot a vertical rather than a horizontal Cartesian scale.
    box
        Draw a background box behind the directional rose. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    $perspective
    $verbose
    $transparency

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Box, Position
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 80, -30, 30], projection="M10c", frame=True)
    >>> fig.scalebar(
    ...     position=Position((10, 10)),
    ...     length=1000,
    ...     fancy=True,
    ...     label="Scale",
    ...     unit=True,
    ... )
    >>> fig.show()
    """
    self._preprocess()

    if position is None:
        msg = "Parameter 'position' must be specified."
        raise GMTInvalidInputError(msg)
    if length is None:
        msg = "Parameter 'length' must be specified."
        raise GMTInvalidInputError(msg)

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
        L=[
            Alias(position, name="position"),
            Alias(length, name="length", prefix="+w"),
            Alias(
                label_alignment,
                name="label_alignment",
                prefix="+a",
                mapping={"left": "l", "right": "r", "top": "t", "bottom": "b"},
            ),
            Alias(scale_position, name="scale_position", prefix="+c", sep="/", size=2),
            Alias(fancy, name="fancy", prefix="+f"),
            Alias(label, name="label", prefix="+l"),
            Alias(unit, name="unit", prefix="+u"),
            Alias(vertical, name="vertical", prefix="+v"),
        ],
        p=Alias(perspective, name="perspective"),
    ).add_common(
        V=verbose,
        t=transparency,
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
