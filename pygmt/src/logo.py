"""
logo - Plot the GMT logo.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.params import Box


@fmt_docstring
@use_alias(D="position")
@kwargs_to_strings(p="sequence")
def logo(
    self,
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

    By default, the GMT logo is 2 inches wide and 1 inch high and
    will be positioned relative to the current plot origin.
    Use various options to change this and to place a transparent or
    opaque rectangular map panel behind the GMT logo.

    Full GMT docs at :gmt-docs:`gmtlogo.html`.

    {aliases}
       - F = box
       - J = projection
       - R = region
       - S = style
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    {projection}
    {region}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *width*\ [**+j**\ *justify*]\ [**+o**\ *dx*\ [/*dy*]].
        Set reference point on the map for the image.
    box
        Draw a background box behind the logo. If set to ``True``, a simple rectangular
        box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box appearance,
        pass a :class:`pygmt.params.Box` object to control style, fill, pen, and other
        box properties.
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

    aliasdict = AliasSystem(
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
