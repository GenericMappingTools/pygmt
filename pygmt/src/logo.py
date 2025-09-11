"""
logo - Plot the GMT logo.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(R="region", F="box", S="style")
@kwargs_to_strings(R="sequence", p="sequence")
def logo(  # noqa: PLR0913
    self,
    position: Sequence[str | float] | AnchorCode | None = None,
    position_type: Literal[
        "mapcoords", "boxcoords", "plotcoords", "inside", "outside"
    ] = "plotcoords",
    anchor: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    height: float | str | None = None,
    width: float | str | None = None,
    projection=None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot the GMT logo.

    .. figure:: https://docs.generic-mapping-tools.org/6.5/_images/GMT_coverlogo.png
       :alt: GMT logo
       :align: center
       :width: 300px

    By default, the GMT logo is 2 inches wide and 1 inch high and will be positioned
    relative to the current plot origin. The position can be changed by specifying the
    reference point (via ``position_type`` and ``position``) and anchor point (via
    ``anchor`` and ``anchor_offset``). Refer to :doc:`/techref/reference_anchor_points`
    for details about the positioning.

    Full GMT docs at :gmt-docs:`gmtlogo.html`.

    {aliases}
       - D = position/position_type/anchor/anchor_offset/width/height
       - J = projection
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    {projection}
    {region}
    position/position_type
        Specify the reference point on the plot for the GMT logo. The reference point
        can be specified in five different ways, which is selected by the
        **position_type** parameter. The actual reference point is then given by the
        coordinates or code specified by the **position** parameter.

        The **position_type** parameter can be one of the following:

        - ``"mapcoords"``: **position** is given as (*longitude*, *latitude*) in map
          coordinates. For example, (120, -45) means placing the reference point at
          120°E and 45°S in map coordinates.
        - ``"boxcoords"``: **position** is given as (*nx*, *ny*) in normalized
          coordinates, i.e., fractional coordinates between 0 and 1 in both the x and y
          directions. For example, (0, 0) is the lower-left corner and (1, 1) is the
          upper-right corner of the plot bounding box.
        - ``"plotcoords"``: **position** is given as (x, y) in plot coordinates, i.e.,
          the distances in inches, centimeters, or points from the lower left plot
          origin. For example, ("1c", "2c") means placing the reference point 1 cm to
          the right and 2 cm above the lower left plot origin.
        - ``"inside"`` or ``"outside"``: **position** is one of the nine
          :doc:`2-character justification codes </techref/justification_codes>`, meaning
          placing the reference point at specific locations, either inside or outside
          the plot bounding box. E.g., ``"TL"`` means placing the reference point at the
          top left corner of the plot bounding box, either inside or outside the box.
    anchor
        Anchor point of the GMT logo, specified by one of the
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
        Width or height of the GMT logo. Since the aspect ratio is fixed, only one of
        the two can be specified.
    box : bool or str
        If set to ``True``, draw a rectangular border around the
        GMT logo.
    style : str
        [**l**\|\ **n**\|\ **u**].
        Control what is written beneath the map portion of the logo.

        - **l** to plot the text label "The Generic Mapping Tools"
          [Default]
        - **n** to skip the label placement
        - **u** to place the URL to the GMT site
    {verbose}
    {panel}
    {transparency}
    """
    self._activate_figure()

    # width and height are mutually exclusive.
    if width is not None and height is not None:
        msg = "Cannot specify both width and height."
        raise GMTInvalidInput(msg)

    # Mapping position_type to GMT shorthand.
    _position_type = {
        "mapcoords": "g",
        "boxcoords": "n",
        "plotcoords": "x",
        "inside": "j",
        "outside": "J",
    }[position_type]

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position", sep="/", size=2, prefix=_position_type),
            Alias(anchor, name="anchor", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
            Alias(height, name="height", prefix="+h"),
            Alias(width, name="width", prefix="+w"),
        ]
    ).add_common(
        J=projection,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
