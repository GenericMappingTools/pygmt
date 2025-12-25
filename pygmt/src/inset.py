"""
inset - Manage figure inset setup and completion.
"""

import contextlib
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position

__doctest_skip__ = ["inset"]


@fmt_docstring
@deprecate_parameter("margin", "clearance", "v0.18.0", remove_version="v0.20.0")
@use_alias(C="clearance")
@kwargs_to_strings(C="sequence")
@contextlib.contextmanager
def inset(
    self,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    width: float | str | None = None,
    height: float | str | None = None,
    box: Box | bool = False,
    no_clip: bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
):
    r"""
    Manage figure inset setup and completion.


    This method carves out a sub-region of the current plot canvas and restrict further
    plotting to that section of the canvas. Plotting methods that are called within the
    context manager are added to the inset figure.

    Full GMT docs at :gmt-docs:`inset.html`.

    $aliases
       - D = position, **+w**: width/height
       - F = box
       - J = projection
       - N = no_clip
       - R = region
       - V = verbose

    Parameters
    ----------
    position
        Position of the inset on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x- and y-coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the Bottom Left corner of the plot.
    width
    height
        Width and height of the inset. Width must be specified and height is set to be
        equal to width if not specified.
    box
        Draw a background box behind the inset. If set to ``True``, a simple rectangular
        box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box appearance,
        pass a :class:`pygmt.params.Box` object to control style, fill, pen, and other
        box properties.
    clearance : float, str, or list
        This is clearance that is added around the inside of the inset.
        Plotting will take place within the inner region only. The margins
        can be a single value, a pair of values separated (for setting
        separate horizontal and vertical margins), or the full set of four
        margins (for setting separate left, right, bottom, and top
        margins). When passing multiple values, it can be either a list or
        a string with the values separated by forward
        slashes [Default is no margins].
    no_clip
        Do **not** clip features extruding outside the inset frame boundaries [Default
        is ``False``].

    $projection
    $region
    $verbose

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Box, Position
    >>>
    >>> fig = pygmt.Figure()
    >>> fig.coast(region="MG+r2", water="lightblue", shorelines="thin")
    >>> # Use a "with" statement to initialize the inset context manager.
    >>> # Setting the position to Top Left and a width of 3.5 centimeters
    >>> with fig.inset(
    ...     position=Position("TL", offset=0.2),
    ...     width="3.5c",
    ...     clearance=0,
    ...     box=Box(pen="green"),
    ... ):  # Map elements under the "with" statement are plotted in the inset
    ...     fig.coast(
    ...         region="g",
    ...         projection="G47/-20/?",
    ...         land="gray",
    ...         water="white",
    ...         dcw="MG+gred",
    ...     )
    >>> # Map elements outside the "with" statement are plotted in the main figure
    >>> fig.logo(position=Position("BR", offset=0.2), width="3c")
    >>> fig.show()
    """
    self._activate_figure()

    position = _parse_position(
        position,
        kwdict={"width": width, "height": height},
        default=Position((0, 0), cstype="plotcoords"),  # Default to (0,0) in plotcoords
    )

    # width is mandatory.
    if width is None and not isinstance(position, str):
        msg = "Parameter 'width' must be specified."
        raise GMTInvalidInput(msg)

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position"),
            Alias(width, name="width", prefix="+w"),  # +wwidth/height
            Alias(height, name="height", prefix="/"),
        ],
        F=Alias(box, name="box"),
        N=Alias(no_clip, name="no_clip"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        try:
            lib.call_module(module="inset", args=["begin", *build_arg_list(aliasdict)])
            yield
        finally:
            lib.call_module(
                module="inset", args=["end", *build_arg_list({"V": aliasdict.get("V")})]
            )
