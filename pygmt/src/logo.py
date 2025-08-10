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
@use_alias(
    R="region",
    J="projection",
    F="box",
    S="style",
    V="verbose",
    c="panel",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def logo(
    self,
    position: Sequence[str | float] | AnchorCode,
    position_type: Literal[
        "mapcoords", "inside", "outside", "boxcoords", "plotcoords"
    ] = "mapcoords",
    height=None,
    width=None,
    justify=None,
    anchor_offset=None,
    **kwargs,
):
    r"""
    Plot the GMT logo.

    By default, the GMT logo is 2 inches wide and 1 inch high and
    will be positioned relative to the current plot origin.
    Use various options to change this and to place a transparent or
    opaque rectangular map panel behind the GMT logo.

    Full GMT docs at :gmt-docs:`gmtlogo.html`.

    {aliases}

    Parameters
    ----------
    {projection}
    {region}
    position/position_type
        Location of the GMT logo. The actual meaning of this parameter depends on the
        ``position_type`` parameter.
        - ``position_type="mapcoords"``: *position* is given as (x, y) in user
          coordinates.
        - ``position_type="boxcoords"``: *position* is given as (nx, ny) in normalized
          coordinates, where (0, 0) is the lower-left corner and (1, 1) is the
          upper-right corner of the map.
        - ``position_type="plotcoords"``: *position* is given as (x, y) in plot
          coordinates.
        - ``position_type="inside"``: *position* is given as a two-character
          justification code, meaning the anchor point of the rose is inside the map
          bounding box.
        - ``position_type="outside"``: *position* is given as a two-character
          justification code, but the rose is outside the map bounding box.
    width/height
        Width or height of the GMT logo.
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
    if width is not None and height is not None:
        msg = "Cannot specify both width and height."
        raise GMTInvalidInput(msg)

    aliasdict = AliasSystem(
        D=[
            Alias(
                position_type,
                name="position_type",
                mapping={
                    "mapcoords": "g",
                    "inside": "j",
                    "outside": "J",
                    "boxcoords": "n",
                    "plotcoords": "x",
                },
            ),
            Alias(position, name="position", sep="/"),
            Alias(height, name="height", prefix="+h"),
            Alias(width, name="width", prefix="+w"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
        ]
    ).merge(kwargs)

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
