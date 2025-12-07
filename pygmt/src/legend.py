"""
legend - Plot a legend.
"""

import io
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput, GMTTypeError
from pygmt.helpers import build_arg_list, data_kind, fmt_docstring, is_nonstr_iter
from pygmt.params import Box, Position


@fmt_docstring
def legend(  # noqa: PLR0913
    self,
    spec: PathLike | io.StringIO | None = None,
    position: Position | None = None,
    width: float | str | None = None,
    height: float | str | None = None,
    line_spacing: float | None = None,
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
    """
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

       - D = position, **+w**: width/height, **+l**: line_spacing
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
        Specify the position of the legend on the plot. If not specified, defaults to
        the top right corner inside the plot with a 0.2-cm offset. See
        :class:`pygmt.enums.Position` for details.
    width
    height
        Specify the width and height of the legend box in plot coordinates (inches, cm,
        etc.). If not given, the width and height are computed automatically based on
        the contents of the legend specification.

        If unit is ``%`` (percentage) then width is computed as that fraction of the
        plot width. If height is given as percentage then height is recomputed as that
        fraction of the legend width (not plot height).

        **Note:** Currently, the automatic height calculation only works when legend
        codes **D**, **H**, **L**, **S**, or **V** are used and that the number of
        symbol columns (**N**) is 1.
    line_spacing
        Specify the line-spacing factor between legend entries in units of the current
        font size [Default is 1.1].
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

    # Prior PyGMT v0.17.0, 'position' can accept a raw GMT CLI string. Check for
    # conflicts with other parameters.
    if isinstance(position, str) and any(
        v is not None for v in (width, height, line_spacing)
    ):
        msg = (
            "Parameter 'position' is given with a raw GMT command string, and conflicts "
            "with parameters 'width', 'height', and 'line_spacing'. "
        )
        raise GMTInvalidInput(msg)

    # Set default position if not specified.
    if kwargs.get("D", position) is None:
        position = Position("TR", anchor="TR", offset=0.2)
        if kwargs.get("F", box) is False:
            box = Box(pen="1p", fill="white")  # Default box

    # Set default width to 0 if height is given but width is not.
    if height is not None and width is None:
        width = 0

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
            Alias(line_spacing, name="line_spacing", prefix="+l"),
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
