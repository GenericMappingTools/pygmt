"""
legend - Plot a legend.
"""

import io
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode, PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput, GMTTypeError
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(R="region", D="position", F="box", p="perspective")
@kwargs_to_strings(R="sequence", p="sequence")
def legend(  # noqa: PLR0913
    self,
    spec: PathLike | io.StringIO | None = None,
    projection=None,
    position: Sequence[float | str] | AnchorCode | None = None,
    position_type: Literal[
        "mapcoords", "boxcoords", "plotcoords", "inside", "outside"
    ] = "plotcoords",
    anchor: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    width=None,
    height=None,
    spacing=None,
    box="+gwhite+p1p",
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot a legend.

    Makes legends that can be overlaid on maps. Reads specific
    legend-related information from an input file, or automatically creates
    legend entries from plotted symbols that have labels. Unless otherwise
    noted, annotations will be made using the primary annotation font and
    size in effect (i.e., :gmt-term:`FONT_ANNOT_PRIMARY`).

    Full GMT docs at :gmt-docs:`legend.html`.

    {aliases}
       - J = projection
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    spec
        The legend specification. It can be:

        - ``None`` which means using the automatically generated legend specification
          file
        - Path to the legend specification file
        - A :class:`io.StringIO` object containing the legend specification

        See :gmt-docs:`legend.html` for the definition of the legend specification.
    {projection}
    {region}
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
    width/height
        Width and height of the legend box in plot coordinates (inches, cm, etc.). If
        unit is % (percentage) then width as computed as that fraction of the map width.
        If height is given as percentage then then height is recomputed as that fraction
        of the legend width (not map height). Note: If **width** is not given then the
        width is computed within the Postscript code. Currently, this is only possible
        if just legend codes D, H, L, S, or V are used and that the number of symbol
        columns (N) is 1. If **height** is zero or not given then we estimate height
        based the expected vertical extent of the items to be placed.
    spacing
        Line spacing factor in units of the current font size [Default is 1.1].
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draw a rectangular border around the legend
        using :gmt-term:`MAP_FRAME_PEN`. By default, uses
        **+g**\ white\ **+p**\ 1p which draws a box around the legend using a
        1p black pen and adds a white background.
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    self._activate_figure()

    if kwargs.get("D") is None:
        kwargs["D"] = position
        if kwargs.get("F") is None:
            kwargs["F"] = box

    kind = data_kind(spec)
    if kind not in {"empty", "file", "stringio"}:
        raise GMTTypeError(type(spec))
    if kind == "file" and is_nonstr_iter(spec):
        raise GMTTypeError(
            type(spec), reason="Only one legend specification file is allowed."
        )

    if height is not None and width is None:
        msg = "Parameter 'width' must be given if 'height' is specified."
        raise GMTInvalidInput(msg)

    _dimension = (width, height) if height is not None else width
    aliasdict = AliasSystem(
        D=[
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
            Alias(_dimension, name="width/height", prefix="+w"),
            Alias(spacing, name="spacing", prefix="+l"),
        ],
    ).add_common(
        J=projection,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(data=spec, required=False) as vintbl:
            lib.call_module(
                module="legend", args=build_arg_list(aliasdict, infile=vintbl)
            )
