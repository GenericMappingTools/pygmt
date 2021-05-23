"""
logo - Plot the GMT logo
"""

from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    D="position",
    F="box",
    S="style",
    U="timestamp",
    V="verbose",
    X="xshift",
    Y="yshift",
    c="panel",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def logo(self, **kwargs):
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
    {J}
    {R}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *width*\ [**+j**\ *justify*]\ [**+o**\ *dx*\ [/*dy*]].
        Sets reference point on the map for the image.
    box : bool or str
        Without further arguments, draws a rectangular border around the
        GMT logo.
    style : str
        [**l**\|\ **n**\|\ **u**].
        Control what is written beneath the map portion of the logo.

        - **l** to plot the text label "The Generic Mapping Tools"
          [Default]
        - **n** to skip the label placement
        - **u** to place the URL to the GMT site
    {U}
    {V}
    {XY}
    {c}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        lib.call_module("logo", build_arg_string(kwargs))
