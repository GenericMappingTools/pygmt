"""
logo - Plot the GMT logo.
"""

from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    R="region",
    D="position",
    F="box",
    S="style",
    t="transparency",
)
@kwargs_to_strings(R="sequence", p="sequence")
def logo(
    self,
    projection=None,
    verbose: Literal[
        "quiet",
        "error",
        "warning",
        "timing",
        "information",
        "compatibility",
        "debug",
    ]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
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

    aliasdict = AliasSystem(
        J=Alias(projection, name="projection"),
    ).add_common(
        V=verbose,
        c=panel,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
