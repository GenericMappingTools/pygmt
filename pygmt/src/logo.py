"""
logo - Plot the GMT logo.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position


@fmt_docstring
def logo(  # noqa: PLR0913
    self,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    width: float | str | None = None,
    height: float | str | None = None,
    box: Box | bool = False,
    style: Literal["standard", "url", "no_label"] = "standard",
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    """
    Plot the GMT logo.

    .. figure:: https://docs.generic-mapping-tools.org/6.6/_images/GMT_coverlogo.png
       :alt: GMT logo
       :align: center
       :width: 300px

    By default, the GMT logo is 2 inches wide and 1 inch high and will be positioned
    relative to the current plot origin.

    Full GMT docs at :gmt-docs:`gmtlogo.html`.

    **Aliases:**

    .. hlist::
       :columns: 3

       - D = position, **+w**: width, **+h**: height
       - F = box
       - J = projection
       - R = region
       - S = style
       - V = verbose
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    position
        Position of the GMT logo on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x and y coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the lower-left corner of the plot (position
        ``(0, 0)`` with anchor ``"BL"``).
    width
    height
        Width or height of the GMT logo. Since the aspect ratio is fixed, only one of
        the two can be specified. [Default is 2 inches wide and 1 inch high.]
    box
        Draw a background box behind the logo. If set to ``True``, a simple rectangular
        box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box appearance,
        pass a :class:`pygmt.params.Box` object to control style, fill, pen, and other
        box properties.
    style
        Control what is written beneath the map portion of the logo.

        - ``"standard"``: The text label "The Generic Mapping Tools".
        - ``"no_label"``: Skip the text label.
        - ``"url"``: The URL to the GMT website.
    $projection
    $region
    $verbose
    $panel
    $perspective
    $transparency
    """
    self._activate_figure()

    position = _parse_position(
        position,
        default=Position((0, 0), cstype="plotcoords"),  # Default to (0,0) in plotcoords
        kwdict={"width": width, "height": height},
    )

    # width and height are mutually exclusive.
    if width is not None and height is not None:
        msg = "Cannot specify both 'width' and 'height'."
        raise GMTInvalidInput(msg)

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position"),
            Alias(height, name="height", prefix="+h"),
            Alias(width, name="width", prefix="+w"),
        ],
        F=Alias(box, name="box"),
        S=Alias(
            style, name="style", mapping={"standard": "l", "url": "u", "no_label": "n"}
        ),
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
        lib.call_module(module="logo", args=build_arg_list(aliasdict))
