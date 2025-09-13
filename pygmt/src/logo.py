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
    position/position_type
        Specify the reference point on the plot for the GMT logo. The method of
        defining the the reference point is controlled by **position_type**, and the
        exact location is set by **position**.

        The **position_type** parameter can take one of the following values:

        - ``"mapcoords"``: **position** is specified as (*longitude*, *latitude*) in map
          coordinates. Example: (120, -45) places the reference point at 120°E, 45°S.
        - ``"boxcoords"``: **position** is specified as (*nx*, *ny*) in normalized
          coordinates, i.e., fractional values between 0 and 1 along the x- and y-axes.
          Example: (0, 0) corresponds to the lower-left corner, and (1, 1) to the
          upper-right corner of the plot bounding box.
        - ``"plotcoords"``: **position** is specified as (*x*, *y*) in plot coordinates,
          i.e., distances from the lower-left plot origin given in inches, centimeters,
          or points. Example: ("1c", "2c") places the reference point 1 cm to the right
          and 2 cm above the plot origin.
        - ``"inside"`` or ``"outside"``: **position** is one of the nine
          :doc:two-character justification codes </techref/justification_codes>,
          indicating a specific location relative to the plot bounding box. Example:
          ``"TL"`` places the reference point at the top-left corner, either inside or
          outside the bounding box.
    anchor
        Specify the anchor point of the GMT logo, using one of the
        :doc:`2-character justification codes </techref/justification_codes>`.
        The default value depends on **position_type**.

        - ``position_type="inside"``: **anchor** defaults to the same as **position**.
        - ``position_type="outside"``: **anchor** defaults to the mirror opposite of
          **position**.
        - Otherwise, **anchor** defaults to ``"MC"`` (middle center).
    anchor_offset
        Specifies an offset for the anchor point as *offset* or
        (*offset_x*, *offset_y*). If a single value *offset* is given, both *offset_x*
        and *offset_y* are set to *offset*.
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
    {projection}
    {region}
    {verbose}
    {panel}
    {transparency}
    """
    self._activate_figure()

    # width and height are mutually exclusive.
    if width is not None and height is not None:
        msg = "Cannot specify both width and height."
        raise GMTInvalidInput(msg)

    # Mapping position_type to GMT single-letter code.
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
