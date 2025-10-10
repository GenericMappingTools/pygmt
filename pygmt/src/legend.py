"""
legend - Plot a legend.
"""

import io
from collections.abc import Sequence
from typing import Literal

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
from pygmt.params import Box


@fmt_docstring
@use_alias(D="position", p="perspective")
@kwargs_to_strings(p="sequence")
def legend(
    self,
    spec: PathLike | io.StringIO | None = None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    position="JTR+jTR+o0.2c",
    box: Box | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
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
       - F = box
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

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
    box
        Draw a background box behind the legend. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    self._activate_figure()

    # Default position and box when not specified.
    if kwargs.get("D") is None:
        kwargs["D"] = position
        if box is False and kwargs.get("F") is None:
            box = Box(pen="1p", fill="white")  # Default box

    kind = data_kind(spec)
    if kind not in {"empty", "file", "stringio"}:
        raise GMTTypeError(type(spec))
    if kind == "file" and is_nonstr_iter(spec):
        raise GMTTypeError(
            type(spec), reason="Only one legend specification file is allowed."
        )

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(data=spec, required=False) as vintbl:
            lib.call_module(
                module="legend", args=build_arg_list(aliasdict, infile=vintbl)
            )
