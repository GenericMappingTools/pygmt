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
@use_alias(R="region", D="position", F="box", S="style")
@kwargs_to_strings(R="sequence", p="sequence")
def logo(  # noqa: PLR0913
    self,
    position: Sequence[str | float] | AnchorCode,
    position_type: Literal[
        "mapcoords", "boxcoords", "plotcoords", "inside", "outside"
    ] = "plotcoords",
    anchor: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    height: float | str | None = None,
    width: float | str | None = None,
    projection=None,
    box=False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
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
       - J = projection
       - V = verbose
       - c = panel
       - t = transparency

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
          upper-right corner of the plot.
        - ``position_type="plotcoords"``: *position* is given as (x, y) in plot
          coordinates, i.e., the distances in inches, centimeters, or points from the
          lower left plot origin.
        - ``position_type="inside"``: *position* is given as a two-character
          justification code, meaning the anchor point of the rose is inside the plot
          bounding box.
        - ``position_type="outside"``: *position* is given as a two-character
          justification code, but the rose is outside the plot bounding box.
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
                    "boxcoords": "n",
                    "plotcoords": "x",
                    "inside": "j",
                    "outside": "J",
                },
            ),
            Alias(position, name="position", sep="/"),
            Alias(anchor, name="justify", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
            Alias(height, name="height", prefix="+h"),
            Alias(width, name="width", prefix="+w"),
        ]
    ).merge(kwargs)

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
    ).add_common(
        J=projection,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
