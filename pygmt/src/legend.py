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
from pygmt.helpers import build_arg_list, data_kind, fmt_docstring, is_nonstr_iter
from pygmt.params import Box, Position


@fmt_docstring
def legend(  # noqa: PLR0913
    self,
    spec: PathLike | io.StringIO | None = None,
    position: Position | None = None,
    width: float | str | None = None,
    height: float | str | None = None,
    spacing: float | None = None,
    box: Box | bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    transparency: float | None = None,
    perspective: float | Sequence[float] | str | bool = False,
    **kwargs,
):
    r"""
    Plot a legend.

    Makes legends that can be overlaid on plots. It reads specific legend-related
    information from an input file, a :class:`io.StringIO` object, or automatically
    creates legend entries from plotted symbols that have labels. Unless otherwise
    noted, annotations will be made using the primary annotation font and size in effect
    (i.e., :gmt-term:`FONT_ANNOT_PRIMARY`).

    Full GMT docs at :gmt-docs:`legend.html`.

    **Aliases:**

    .. hlist::
       :columns: 3

       - D = position, **+w**: width/height, **+l**: spacing
       - F = box
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - p = perspective
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
    position
        Specify the position of the legend on the plot. By default, the anchor point on
        the legend is assumed to be the bottom left corner (``"BL"``). See
        :class:`pygmt.enums.Position` for details.
    width
    height
        Specify the width and height of the legend box in plot coordinates (inches, cm,
        etc.). If unit is ``%`` (percentage) then width as computed as that fraction of
        the plot width. If height is given as percentage then then height is recomputed
        as that fraction of the legend width (not plot height).

        **Note:** If ``width`` is not given, the width defaults to be computed within
        the Postscript code. Currently, this is only possible if just legend codes
        **D**, **H**, **L**, **S**, or **V** are used and that the number of symbol
        columns (**N**) is 1. If ``height`` is zero or not given then we estimate height
        based the expected vertical extent of the items to be placed.
    spacing
        Specify the line-spacing factor in units of the current font size [Default is
        1.1].
    box
        Draw a background box behind the legend. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    $projection
    $region
    $verbose
    $panel
    $perspective
    $transparency
    """
    self._activate_figure()

    # Set default position if not specified.
    if kwargs.get("D", position) is None:
        position = Position("TR", anchor="TR", offset=0.2)
        if kwargs.get("F", box) is None:
            box = Box(pen="1p", fill="white")  # Default box

    kind = data_kind(spec)
    if kind not in {"empty", "file", "stringio"}:
        raise GMTTypeError(type(spec))
    if kind == "file" and is_nonstr_iter(spec):
        raise GMTTypeError(
            type(spec), reason="Only one legend specification file is allowed."
        )

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position"),
            Alias(width, name="width", prefix="+w"),  # +wwidth/height
            Alias(height, name="height", prefix="/"),
            Alias(spacing, name="spacing", prefix="+l"),
        ],
        F=Alias(box, name="box"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(data=spec, required=False) as vintbl:
            lib.call_module(
                module="legend", args=build_arg_list(aliasdict, infile=vintbl)
            )
