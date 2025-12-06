"""
logo - Plot the GMT logo.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Box, Position


@fmt_docstring
def logo(  # noqa: PLR0913
    self,
    position: Position | None = None,
    height: float | str | None = None,
    width: float | str | None = None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    style: Literal["standard", "url", "no_label"] = "standard",
    box: Box | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    transparency: float | None = None,
    perspective: float | Sequence[float] | str | bool = False,
    **kwargs,
):
    r"""
    Plot the GMT logo.

    .. figure:: https://docs.generic-mapping-tools.org/6.6/_images/GMT_coverlogo.png
       :alt: GMT logo
       :align: center
       :width: 300px

    By default, the GMT logo is 2 inches wide and 1 inch high and will be positioned
    relative to the current plot origin. The position can be changed by specifying the
    reference point (via ``position_type`` and ``position``) and anchor point (via
    ``anchor`` and ``anchor_offset``). Refer to :doc:`/techref/reference_anchor_points`
    for details about the positioning.

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
        Specify the position of the GMT logo. See the :class:`pygmt.params.Position`
        class for details.
    width
    height
        Width or height of the GMT logo. Since the aspect ratio is fixed, only one of
        the two can be specified.
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
    $transparency
    $perspective
    """
    self._activate_figure()

    # Prior PyGMT v0.17.0, 'position' can accept a raw GMT CLI string. Check for
    # conflicts with other parameters.
    if isinstance(position, str) and (height is not None or width is not None):
        msg = (
            "Parameter 'position' is given with a raw GMT command string, and conflicts "
            "with parameters 'height', and 'width'. "
        )
        raise GMTInvalidInput(msg)

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
