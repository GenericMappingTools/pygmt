"""
scalebar - Add a scale bar.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInputError
from pygmt.helpers import build_arg_list
from pygmt.params import Box


def scalebar(  # noqa: PLR0913
    self,
    position: Sequence[float | str] | AnchorCode | None = None,
    position_type: Literal[
        "mapcoords", "boxcoords", "plotcoords", "inside", "outside"
    ] = "plotcoords",
    anchor: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
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
    position/position_type
        Specify the reference point on the map for the directional rose. The reference
        point can be specified in five different ways, which is selected by the
        **position_type** parameter. The actual reference point is then given by the
        coordinates or code specified by the **position** parameter.

        The **position_type** parameter can be one of the following:

        - ``"mapcoords"``: **position** is given as (*longitude*, *latitude*) in map
          coordinates.
        - ``"boxcoords"``: **position** is given as (*nx*, *ny*) in normalized
          coordinates, i.e., fractional coordinates between 0 and 1 in both the x and y
          directions. For example, (0, 0) is the lower-left corner and (1, 1) is the
          upper-right corner of the plot bounding box.
        - ``"plotcoords"``: **position** is given as (x, y) in plot coordinates, i.e.,
          the distances in inches, centimeters, or points from the lower left plot
          origin.
        - ``"inside"`` or ``"outside"``: **position** is one of the nine
          :doc:`2-character justification codes </techref/justification_codes>`, meaning
          placing the reference point at specific locations, either inside or outside
          the plot bounding box.
    anchor
        Anchor point of the directional rose, specified by one of the
        :doc:`2-character justification codes </techref/justification_codes>`.
        The default value depends on the **position_type** parameter.

        - ``position_type="inside"``: **anchor** defaults to the same as **position**.
        - ``position_type="outside"``: **anchor** defaults to the mirror opposite of
          **position**.
        - Otherwise, **anchor** defaults to ``"MC"`` (middle center).
    anchor_offset
        *offset* or (*offset_x*, *offset_y*).
        Offset the anchor point by *offset_x* and *offset_y*. If a single value *offset*
        is given, *offset_y* = *offset_x* = *offset*.
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
    {perspective}
    {verbose}
    {transparency}

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

    if position is None:
        msg = "Parameter 'position' must be specified."
        raise GMTInvalidInputError(msg)
    if length is None:
        msg = "Parameter 'length' must be specified."
        raise GMTInvalidInputError(msg)

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
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
            Alias(anchor, name="justify", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
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
