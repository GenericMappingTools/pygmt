"""
logo - Plot the GMT logo.
"""

from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(R="region", D="position", F="box")
@kwargs_to_strings(R="sequence", p="sequence")
def logo(
    self,
    projection=None,
    style: Literal["standard", "url", "no_label"] = "standard",
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
    box : bool or str
        If set to ``True``, draw a rectangular border around the
        GMT logo.
    style
        Control what is written beneath the map portion of the logo.

        - ``"standard"``: The text label "The Generic Mapping Tools".
        - ``"url"``: The URL to the GMT website.
        - ``"no_label"``: Skip the text label.
    {verbose}
    {panel}
    {transparency}
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        S=Alias(
            style, name="style", mapping={"standard": "l", "url": "u", "no_label": "n"}
        ),
    ).add_common(
        J=projection,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
