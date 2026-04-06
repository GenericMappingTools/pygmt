"""
magnetic_rose - Add a map magnetic rose.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position

__doctest_skip__ = ["magnetic_rose"]


@fmt_docstring
def magnetic_rose(  # noqa: PLR0913
    self,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    width: float | str | None = None,
    labels: Sequence[str] | bool = False,
    outer_pen: str | bool = False,
    inner_pen: str | bool = False,
    declination: float | None = None,
    declination_label: str | None = None,
    intervals: Sequence[float] | None = None,
    box: Box | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: str | bool = False,
    transparency: float | None = None,
):
    """
    Add a magnetic rose to the map.

    Parameters
    ----------
    position
        Position of the magnetic rose on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x- and y-coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the Bottom Left corner of the plot (position
        ``(0, 0)`` with anchor ``"BL"``).
    width
        Width of the rose in plot coordinates, or append unit ``%`` for a size in
        percentage of plot width [Default is 15%].
    labels
        A sequence of four strings to label the cardinal points W, E, S, N. Use an empty
        string to skip a specific label. If the north label is ``"*"``, then a north
        star is plotted instead of the north label. If set to ``True``, use the default
        labels ``["W", "E", "S", "N"]``.
    outer_pen
        Draw the outer circle of the magnetic rose, using the given pen attributes.
    inner_pen
        Draw the inner circle of the magnetic rose, using the given pen attributes.
    declination
        Magnetic declination in degrees. By default, only a geographic north is plotted.
        With this parameter set, a magnetic north is also plotted. A magnetic compass
        needle is drawn inside the rose to indicate the direction to magnetic north.
    declination_label
        Label for the magnetic compass needle. Default is to format a label based on
        ``declination``. To bypass the label, set to ``"-"``.
    intervals
        Specify the annotation and tick intervals for the geographic and magnetic
        directions. It can be a sequence of three or six values. If three values are
        given, they are used for both geographic and magnetic directions. If six values
        are given, the first three are used for geographic directions and the last three
        for magnetic directions. [Default is ``(30, 5, 1)``].
        **Note**: If :gmt-term:`MAP_EMBELLISHMENT_MODE` is ``"auto"`` and the compass
        size is smaller than 2.5 cm then the interval defaults are reset to
        ``(90,30, 3, 45, 15, 3)``.
    box
        Draw a background box behind the magnetic rose. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    $perspective
    $verbose
    $transparency

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Position
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[-10, 10, -10, 10], projection="M15c", frame=True)
    >>> fig.magnetic_rose(
    ...     position=Position((-5, -5), cstype="mapcoords"),
    ...     width="4c",
    ...     labels=["W", "E", "S", "*"],
    ...     intervals=(45, 15, 3, 60, 20, 4),
    ...     outer_pen="1p,red",
    ...     inner_pen="1p,blue",
    ...     declination=11.5,
    ...     declination_label="11.5°E",
    ... )
    >>> fig.show()
    """
    self._activate_figure()

    position = _parse_position(position, default=Position("BL", cstype="inside"))

    if declination_label is not None:
        if declination is None:
            raise GMTParameterError(
                required="declination",
                reason="Required when 'declination_label' is set.",
            )
        # Upstream issue that declination label with spaces is not properly handled.
        if " " in declination_label:
            declination_label = declination_label.replace(" ", "\\040")

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
        Tm=[
            Alias(position, name="position"),
            Alias(width, name="width", prefix="+w"),
            Alias(labels, name="labels", prefix="+l", sep=",", size=4),
            Alias(outer_pen, name="outer_pen", prefix="+p"),
            Alias(inner_pen, name="inner_pen", prefix="+i"),
            Alias(declination, name="declination", prefix="+d"),
            Alias(declination_label, name="declination_label", prefix="/"),
            Alias(intervals, name="intervals", prefix="+t", sep="/", size=(3, 6)),
        ],
    ).add_common(
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
