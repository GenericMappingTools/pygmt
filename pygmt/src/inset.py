"""
inset - Manage figure inset setup and completion.
"""

import contextlib
from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.params import Box, Position

__doctest_skip__ = ["inset"]


@fmt_docstring
@contextlib.contextmanager
@use_alias(M="margin")
@kwargs_to_strings(M="sequence")
def inset(
    self,
    position: Position | None = None,
    width: float | str | None = None,
    height: float | str | None = None,
    box: Box | bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    no_clip: bool = False,
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
        Specify the position of the inset on the map. See :class:`pygmt.params.Position`
        for details.

        Alternatively, give *west/east/south/north* of geographic rectangle bounded by
        parallels and meridians; append **+r** if the coordinates instead are the lower
        left and upper right corners of the desired rectangle. (Or, give
        *xmin/xmax/ymin/ymax* of bounding rectangle in projected coordinates and
        optionally append **+u**\ *unit* [Default coordinate unit is meters (**e**)].

    width
    height
        Width and height of the inset. *height* is optional.
    box
        Draw a background box behind the inset. If set to ``True``, a simple rectangular
        box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box appearance,
        pass a :class:`pygmt.params.Box` object to control style, fill, pen, and other
        box properties.
    margin : float, str, or list
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
    $region
    $projection
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
    ...     margin=0,
    ...     box=Box(pen="green"),
    ... ):  # Map elements under the "with" statement are plotted in the inset
    ...     fig.coast(
    ...         region="g",
    ...         projection="G47/-20/3.5c",
    ...         land="gray",
    ...         water="white",
    ...         dcw="MG+gred",
    ...     )
    >>> # Map elements outside the "with" statement are plotted in the main figure.
    >>> fig.logo(position="jBR+o0.2c+w3c")
    >>> fig.show()
    """
    self._activate_figure()

    if position is None or width is None:
        msg = "Parameters 'position' and 'width' must be specified."
        raise GMTInvalidInput(msg)

    if height is not None and width is None:
        msg = "'width' must be specified if 'height' is given."
        raise GMTInvalidInput(msg)

    # Prior PyGMT v0.17.0, 'position' can accept a raw GMT CLI string. Check for
    # conflicts with other parameters.
    if isinstance(position, str) and any(v is not None for v in (width, height)):
        msg = (
            "Parameter 'position' is given with a raw GMT command string, and conflicts "
            "with parameters 'height', and 'width'. "
        )
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
