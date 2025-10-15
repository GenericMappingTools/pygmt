"""
logo - Plot the GMT logo.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings
from pygmt.params import Box


@fmt_docstring
@kwargs_to_strings(p="sequence")
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
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    style: Literal["standard", "url", "no_label"] = "standard",
    box: Box | bool = False,
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
       - F = box
       - J = projection
       - R = region
       - S = style
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    position
        Specify the reference point on the plot for the GMT logo. The method of defining
        the reference point is controlled by **position_type**, and the exact location
        is set by **position**.
    position_type
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
    box
        Draw a background box behind the logo. If set to ``True``, a simple rectangular
        box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box appearance,
        pass a :class:`pygmt.params.Box` object to control style, fill, pen, and other
        box properties.
    {projection}
    {region}
    style
        Control what is written beneath the map portion of the logo.

        - ``"standard"``: The text label "The Generic Mapping Tools".
        - ``"no_label"``: Skip the text label.
        - ``"url"``: The URL to the GMT website.
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

    # Prior PyGMT v0.17.0, 'position' was aliased to the -D option.
    # For backward compatibility, we need to check if users pass a string with the GMT
    # CLI syntax to 'position', i.e., a string starting with one of the leading
    # single-letter or contains modifiers with "+".
    if isinstance(position, str) and (position[0] in "gnxjJ" or "+" in position):
        if any(v is not None for v in (anchor, anchor_offset, height, width)):
            msg = (
                "Parameter 'position' is given with a raw GMT CLI syntax, and conflicts "
                "with other parameters (anchor, anchor_offset, height, width). "
                "Please refer to the documentation for the recommended usage."
            )
            raise GMTInvalidInput(msg)
        _position_type = ""  # Unset _position_type to an empty string.

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position", sep="/", size=2, prefix=_position_type),
            Alias(anchor, name="anchor", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
            Alias(height, name="height", prefix="+h"),
            Alias(width, name="width", prefix="+w"),
        ],
        F=Alias(box, name="box"),
        S=Alias(
            style, name="style", mapping={"standard": "l", "url": "u", "no_label": "n"}
        ),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
