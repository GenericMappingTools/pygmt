"""
logo - Plot the GMT logo.
"""

from typing import Literal

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
    position_type: Literal[
        "user", "justify", "mirror", "normalize", "plot", None
    ] = None,
    position=None,
    height=None,
    width=None,
    justify=None,
    offset=None,
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
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *width*\ [**+j**\ *justify*]\ [**+o**\ *dx*\ [/*dy*]].
        Set reference point on the map for the image.
    positon_type
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
                    "user": "g",
                    "justify": "j",
                    "mirror": "J",
                    "normalize": "n",
                    "plot": "x",
                },
            ),
            Alias(position, name="position", separator="/"),
            Alias(height, name="height", prefix="+h"),
            Alias(width, name="width", prefix="+w"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(offset, name="offset", prefix="+o", separator="/", size=2),
        ]
    ).merge(kwargs)

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
