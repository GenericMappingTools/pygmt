"""
logo - Plot the GMT logo.
"""

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.params import Box


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    D="position",
    S="style",
    V="verbose",
    c="panel",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def logo(
    self,
    position=None,
    position_type=None,
    length=None,
    height=None,
    offset=None,
    box: Box | str | None = None,
    **kwargs,
):
    r"""
    Plot the GMT logo.

    By default, the GMT logo is 2 inches wide and 1 inch high and
    will be positioned relative to the current plot origin.
    Use various options to change this and to place a transparent or
    opaque rectangular map panel behind the GMT logo.

    Full option list at :gmt-docs:`gmtlogo.html`.

    {aliases}

    Parameters
    ----------
    {projection}
    {region}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *width*\ [**+j**\ *justify*]\ [**+o**\ *dx*\ [/*dy*]].
        Set reference point on the map for the image.
    box
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
    kwargs = self._preprocess(**kwargs)

    kwdict = (
        AliasSystem(
            D=[
                Alias(position, separator="/", prefix=position_type),
                Alias(length, prefix="+w"),
                Alias(height, prefix="+h"),
                Alias(offset, prefix="+o", separator="/"),
            ],
            F=Alias(box),
        ).kwdict
        | kwargs
    )

    with Session() as lib:
        lib.call_module(module="logo", args=build_arg_list(kwdict))
