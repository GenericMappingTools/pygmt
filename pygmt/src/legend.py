"""
legend - Plot a legend.
"""

import io
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


@fmt_docstring
@use_alias(
    R="region",
    D="position",
    F="box",
    V="verbose",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def legend(  # noqa: PLR0913
    self,
    spec: PathLike | io.StringIO | None = None,
    projection=None,
    position=None,
    position_type: Literal[
        "mapcoords", "boxcoords", "plotcoords", "inside", "outside"
    ] = "mapcoords",
    width=None,
    height=None,
    justify=None,
    spacing=None,
    anchor_offset=None,
    box="+gwhite+p1p",
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
    position/position_type
        Location of the map scale bar. The actual meaning of this parameter depends
        on the ``position_type`` parameter.
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

    _dimension = (width, height) if height is not None else width

    aliasdict = AliasSystem(
        J=Alias(projection, name="projection"),
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
            Alias(position, name="position", sep="/", size=2),
            Alias(_dimension, name="width/height", prefix="+w"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(spacing, name="spacing", prefix="+l"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
        ],
    ).merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(data=spec, required=False) as vintbl:
            lib.call_module(
                module="legend", args=build_arg_list(aliasdict, infile=vintbl)
            )
