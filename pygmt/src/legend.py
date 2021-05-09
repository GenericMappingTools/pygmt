"""
legend - Plot a legend.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    D="position",
    F="box",
    V="verbose",
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def legend(self, spec=None, position="JTR+jTR+o0.2c", box="+gwhite+p1p", **kwargs):
    r"""
    Plot legends on maps.

    Makes legends that can be overlaid on maps. Reads specific
    legend-related information from an input file, or automatically creates
    legend entries from plotted symbols that have labels. Unless otherwise
    noted, annotations will be made using the primary annotation font and
    size in effect (i.e., FONT_ANNOT_PRIMARY).

    Full option list at :gmt-docs:`legend.html`

    {aliases}

    Parameters
    ----------
    spec : None or str
        Either ``None`` [default] for using the automatically generated legend
        specification file, or a *filename* pointing to the legend
        specification file.
    {J}
    {R}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *width*\ [/*height*]\ [**+j**\ *justify*]\ [**+l**\ *spacing*]\
        [**+o**\ *dx*\ [/*dy*]].
        Defines the reference point on the map for the
        legend. By default, uses **JTR**\ +\ **jTR**\ +\ **o**\ *0.2c* which
        places the legend at the top-right corner inside the map frame, with a
        0.2 cm offset.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        Without further arguments, draws a rectangular border around the legend
        using :gmt-term:`MAP_FRAME_PEN`. By default, uses
        **+g**\ white\ **+p**\ 1p which draws a box around the legend using a
        1p black pen and adds a white background.
    {V}
    {XY}
    {c}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    if "D" not in kwargs:
        kwargs["D"] = position

        if "F" not in kwargs:
            kwargs["F"] = box

    with Session() as lib:
        if spec is None:
            specfile = ""
        elif data_kind(spec) == "file":
            specfile = spec
        else:
            raise GMTInvalidInput("Unrecognized data type: {}".format(type(spec)))
        arg_str = " ".join([specfile, build_arg_string(kwargs)])
        lib.call_module("legend", arg_str)
