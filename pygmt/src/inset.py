"""
inset - Manage figure inset setup and completion.
"""

import contextlib
from collections.abc import Sequence
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.params import Box

__doctest_skip__ = ["inset"]


@fmt_docstring
@contextlib.contextmanager
@use_alias(D="position", M="margin")
@kwargs_to_strings(D="sequence", M="sequence")
def inset(
    self,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    box: Box | bool = False,
    no_clip: bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
):
    r"""
    Manage figure inset setup and completion.

    This method sets the position, frame, and margins for a smaller figure
    inside of the larger figure. Plotting methods that are called within the
    context manager are added to the inset figure.

    Full GMT docs at :gmt-docs:`inset.html`.

    {aliases}
       - F = box
       - J = projection
       - N = no_clip
       - R = region
       - V = verbose

    Parameters
    ----------
    position : str or list
        *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*]] \
        | [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *width*\ [/*height*][**+j**\ *justify*]\
        [**+o**\ *dx*\ [/*dy*]].

        *This is the only required parameter.*
        Define the map inset rectangle on the map. Specify the rectangle
        in one of three ways:

        Append **g**\ *lon*/*lat* for map (user) coordinates,
        **j**\ *code* or **J**\ *code* for setting the *refpoint* via a
        :doc:`2-character justification code </techref/justification_codes>`
        that refers to the (invisible)
        projected map bounding box, **n**\ *xn*/*yn* for normalized (0-1)
        bounding box coordinates, or **x**\ *x*/*y* for plot
        coordinates (inches, centimeters, points, append unit).
        All but **x** requires both ``region`` and ``projection`` to be
        specified. You can offset the reference point via
        **+o**\ *dx*/*dy* in the direction implied by *code* or
        **+j**\ *justify*.

        Alternatively, give *west/east/south/north* of geographic
        rectangle bounded by parallels and meridians; append **+r** if the
        coordinates instead are the lower left and upper right corners of
        the desired rectangle. (Or, give *xmin/xmax/ymin/ymax* of bounding
        rectangle in projected coordinates and optionally
        append **+u**\ *unit* [Default coordinate unit is meters (**e**)].

        Append **+w**\ *width*\ [/*height*] of bounding rectangle or box
        in plot coordinates (inches, centimeters, etc.). By default, the
        anchor point on the scale is assumed to be the bottom left corner
        (**BL**), but this can be changed by appending **+j** followed by a
        :doc:`2-character justification code </techref/justification_codes>`
        *justify*.
        **Note**: If **j** is used then *justify* defaults to the same
        as *refpoint*, if **J** is used then *justify* defaults to the
        mirror opposite of *refpoint*. Specify inset box attributes via
        the ``box`` parameter [Default is outline only].
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
    {region}
    {projection}
    {verbose}

    Examples
    --------
    >>> import pygmt
    >>> from pygmt.params import Box
    >>>
    >>> # Create the larger figure
    >>> fig = pygmt.Figure()
    >>> fig.coast(region="MG+r2", water="lightblue", shorelines="thin")
    >>> # Use a "with" statement to initialize the inset context manager
    >>> # Setting the position to Top Left and a width of 3.5 centimeters
    >>> with fig.inset(position="jTL+w3.5c+o0.2c", margin=0, box=Box(pen="green")):
    ...     # Map elements under the "with" statement are plotted in the inset
    ...     fig.coast(
    ...         region="g",
    ...         projection="G47/-20/3.5c",
    ...         land="gray",
    ...         water="white",
    ...         dcw="MG+gred",
    ...     )
    ...
    >>> # Map elements outside the "with" statement are plotted in the main
    >>> # figure
    >>> fig.logo(position="jBR+o0.2c+w3c")
    >>> fig.show()
    """
    self._activate_figure()

    aliasdict = AliasSystem(
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
