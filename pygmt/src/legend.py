"""
legend - Plot a legend.
"""

import io

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTTypeError
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    D="position",
    F="box",
    V="verbose",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", p="sequence")
def legend(
    self,
    spec: PathLike | io.StringIO | None = None,
    projection=None,
    position="JTR+jTR+o0.2c",
    box="+gwhite+p1p",
    panel: int | tuple[int, int] | bool = False,
    **kwargs,
):
    r"""
    Plot a legend.

    Makes legends that can be overlaid on maps. Reads specific
    legend-related information from an input file, or automatically creates
    legend entries from plotted symbols that have labels. Unless otherwise
    noted, annotations will be made using the primary annotation font and
    size in effect (i.e., :gmt-term:`FONT_ANNOT_PRIMARY`).

    Full GMT docs at :gmt-docs:`legend.html`.

    {aliases}
       - J = projection
       - c = panel

    Parameters
    ----------
    spec
        The legend specification. It can be:

        - ``None`` which means using the automatically generated legend specification
          file
        - Path to the legend specification file
        - A :class:`io.StringIO` object containing the legend specification

        See :gmt-docs:`legend.html` for the definition of the legend specification.
    {projection}
    {region}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *width*\ [/*height*]\ [**+j**\ *justify*]\ [**+l**\ *spacing*]\
        [**+o**\ *dx*\ [/*dy*]].
        Define the reference point on the map for the
        legend. By default, uses **JTR**\ **+jTR**\ **+o**\ 0.2c which
        places the legend at the top-right corner inside the map frame, with a
        0.2 cm offset.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draw a rectangular border around the legend
        using :gmt-term:`MAP_FRAME_PEN`. By default, uses
        **+g**\ white\ **+p**\ 1p which draws a box around the legend using a
        1p black pen and adds a white background.
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    self._activate_figure()

    if kwargs.get("D") is None:
        kwargs["D"] = position
        if kwargs.get("F") is None:
            kwargs["F"] = box

    kind = data_kind(spec)
    if kind not in {"empty", "file", "stringio"}:
        raise GMTTypeError(type(spec))
    if kind == "file" and is_nonstr_iter(spec):
        raise GMTTypeError(
            type(spec), reason="Only one legend specification file is allowed."
        )

    aliasdict = AliasSystem(
        J=Alias(projection, name="projection"),
    ).add_common(
        c=panel,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(data=spec, required=False) as vintbl:
            lib.call_module(
                module="legend", args=build_arg_list(aliasdict, infile=vintbl)
            )
