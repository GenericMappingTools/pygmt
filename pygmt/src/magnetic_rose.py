"""
magnetic_rose - Add a map magnetic rose.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list
from pygmt.params import Box


def magnetic_rose(  # noqa: PLR0913
    self,
    position: Sequence[float | str] | AnchorCode | None = None,
    position_type: Literal[
        "mapcoords", "boxcoords", "plotcoords", "inside", "outside"
    ] = "plotcoords",
    anchor: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    width: float | str | None = None,
    labels: Sequence[str] | bool = False,
    outer_pen: str | bool = False,
    inner_pen: str | bool = False,
    declination: float | None = None,
    declination_label: str | None = None,
    intervals: Sequence[float] | None = None,
    box: Box | bool = False,
    perspective: str | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    transparency: float | None = None,
):
    """
    Add a magnetic rose to the map.

    The magnetic rose is plotted at the location defined by the reference point
    (specified by the **position** and *position_type** parameters) and anchor point
    (specified by the **anchor** and **anchor_offset** parameters). Refer to
    :doc:`/techref/reference_anchor_points` for details about the positioning.

    Parameters
    ----------
    position/position_type
        Specify the reference point on the map for the magnetic rose. The reference
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
        Anchor point of the magnetic rose, specified by one of the
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
    width
        Width of the rose in plot coordinates (append **i** (inch), **cm**
        (centimeters), or **p** (points)), or append % for a size in percentage of map
        width [Default is 15 %].
    labels
        A sequence of four strings to label the cardinal points W,E,S,N. Use an empty
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
        **declination**. To bypass the label, set to ``"-"``.
    intervals
        Specify the annotation and tick intervals for the geographic and magnetic
        directions. It can be a seqeunce of three or six values. If three values are
        given, they are used for both geographic and magnetic directions. If six values
        are given, the first three are used for geographic directions and the last three
        for magnetic directions. Default is ``(30, 5, 1)``. **Note**: If
        :gmt-term:`MAP_EMBELLISHMENT_MODE` is ``"auto"`` and the compass size is smaller
        than 2.5 cm then the interval defaults are reset to ``(90,30, 3, 45, 15, 3)``.

    Examples
    --------
    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[-10, 10, -10, 10], projection="M15c", frame=True)
    >>> fig.magnetic_rose(
    ...     position=(-5, -5),
    ...     position_type="mapcoords",
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

    if declination_label is not None and declination is None:
        msg = "Parameter 'declination' must be set when 'declination_label' is set."
        raise GMTInvalidInput(msg)
    _dec = (
        (declination, declination_label)
        if declination_label is not None
        else declination
    )

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
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
            Alias(anchor, name="anchor", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
            Alias(width, name="width", prefix="+w"),
            Alias(labels, name="labels", prefix="+l", sep=",", size=4),
            Alias(outer_pen, name="outer_pen", prefix="+p"),
            Alias(inner_pen, name="inner_pen", prefix="+i"),
            Alias(
                _dec, name="declination/declination_label", prefix="+d", sep="/", size=2
            ),
            Alias(intervals, name="intervals", prefix="+t", sep="/", size=(3, 6)),
        ],
        p=Alias(perspective, name="perspective"),
    ).add_common(
        V=verbose,
        t=transparency,
    )

    with Session() as lib:
        lib.call_module(module="basemap", args=build_arg_list(aliasdict))
