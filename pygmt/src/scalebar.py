"""
scalebar - Add a scale bar.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position

__doctest_skip__ = ["scalebar"]


@fmt_docstring
def scalebar(  # noqa: PLR0913
    self,
    length: float | str,
    height: float | str | None = None,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    scale_at: float | Sequence[float] | bool = False,
    label: str | bool = False,
    label_alignment: Literal["left", "right", "top", "bottom"] | None = None,
    unit: bool = False,
    fancy: bool = False,
    vertical: bool = False,
    box: Box | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
):
    """
    Add a scale bar on the plot.

    Parameters
    ----------
    length
        Length of the scale bar in kilometers. Append a suffix to specify another unit. Valid
        units are: **e**: meters; **f**: feet; **k**: kilometers; **M**: statute miles;
        **n**: nautical miles; **u**: US survey feet.
    height
        Height of the scale bar. Only works when ``fancy=True``. [Default is ``"5p"``].
    position
        Position of the scale bar on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x- and y-coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the Bottom Left corner of the plot with a 0.2-cm
        and 0.4-cm offset in the x- and y-directions, respectively.
    scale_at
        Specify the location where the map scale is calculated. It can be:

        - *slat*: Map scale is calculated for latitude *slat*.
        - (*slon*, *slat*): Map scale is calculated for latitude *slat* and longitude
          *slon*, which is useful for oblique projections.
        - ``True``: Map scale is calculated for the middle of the map.
        - ``False``: Default to the location of the reference point.
    label
        Text string to use as the scale bar label. If ``False``, no label is drawn. If
        ``True``, the distance unit provided in the ``length`` parameter (default is km)
        is used as the label. This parameter requires ``fancy=True``.
    label_alignment
        Alignment of the scale bar label. Choose from ``"left"``, ``"right"``,
        ``"top"``, or ``"bottom"``. [Default is ``"top"``].
    fancy
        If ``True``, draw a "fancy" scale bar, which is a segmented bar with alternating
        black and white rectangles. If ``False``, draw a plain scale bar.
    unit
        If ``True``, append the unit to all distance annotations along the scale. For a
        plain scale, this will instead select the unit to be appended to the distance
        length. The unit is determined from the suffix in the ``length`` or defaults to
        ``"km"``.
    vertical
        If ``True``, plot a vertical rather than a horizontal Cartesian scale.
    box
        Draw a background box behind the scale bar. If set to ``True``, a simple
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
    >>> from pygmt.params import Position
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 80, -30, 30], projection="M10c", frame=True)
    >>> fig.scalebar(
    ...     length=1000,
    ...     position=Position((10, 10), cstype="mapcoords"),
    ...     fancy=True,
    ...     label="Scale",
    ...     unit=True,
    ... )
    >>> fig.show()
    """
    self._activate_figure()
    position = _parse_position(
        position,
        kwdict={},  # No need to check conflicts since it's a new function.
        default=Position("BL", offset=(0.2, 0.4)),  # Default to "BL" with offset.
    )

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
            Alias(scale_at, name="scale_at", prefix="+c", sep="/", size=2),
            Alias(fancy, name="fancy", prefix="+f"),
            Alias(label, name="label", prefix="+l"),
            Alias(unit, name="unit", prefix="+u"),
            Alias(vertical, name="vertical", prefix="+v"),
        ],
    ).add_common(
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )

    confdict = {}
    if height is not None:
        confdict["MAP_SCALE_HEIGHT"] = height

    with Session() as lib:
        lib.call_module(
            module="basemap", args=build_arg_list(aliasdict, confdict=confdict)
        )
