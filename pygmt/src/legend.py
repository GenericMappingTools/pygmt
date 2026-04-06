"""
legend - Plot a legend.
"""

import io
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode, PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTTypeError
from pygmt.helpers import build_arg_list, data_kind, fmt_docstring, is_nonstr_iter
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position


@fmt_docstring
def legend(  # noqa: PLR0913
    self,
    spec: PathLike | io.StringIO | None = None,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    width: float | str | None = None,
    height: float | str | None = None,
    line_spacing: float | None = None,
    box: Box | bool = False,
    scale: float | None = None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: str | Sequence[str] | Literal["none"] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
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
       - B = frame
       - F = box
       - J = projection
       - R = region
       - S = scale
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
        Position of the legend on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x- and y-coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the Top Right corner inside the plot with a 0.2-cm
        offset.
    width
    height
        Width and height of the legend box. If not given, the width and height are
        computed automatically based on the contents of the legend specification. If
        unit is ``%`` (percentage) then width is computed as that fraction of the plot
        width. If height is given as percentage then height is recomputed as that
        fraction of the legend width (not plot height).

        **Note:** Currently, the automatic height calculation only works when legend
        codes **D**, **H**, **L**, **S**, or **V** are used and that the number of
        symbol columns (**N**) is 1.
    line_spacing
        The line-spacing factor between legend entries in units of the current font size
        [Default is 1.1].
    box
        Draw a background box behind the legend. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    scale
        Scale all symbol sizes by a common scale [Default is 1.0, i.e., no scaling].
    $projection
    $region
    $frame
    $verbose
    $panel
    $perspective
    $transparency
    """
    self._activate_figure()

    # Set default box if both position and box are not given.
    # The default position will be set later in _parse_position().
    if kwargs.get("D", position) is None and kwargs.get("F", box) is False:
        box = Box(pen="1p", fill="white")

    position = _parse_position(
        position,
        default=Position("TR", offset=0.2),  # Default to TR with 0.2-cm offset.
        kwdict={"width": width, "height": height, "line_spacing": line_spacing},
    )

    # Set width to 0 (auto calculated) if height is given but width is not.
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
        S=Alias(scale, name="scale"),
    ).add_common(
        B=frame,
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
