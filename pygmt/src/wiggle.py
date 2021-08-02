"""
wiggle - Plot z=f(x,y) anomalies along tracks.
"""
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    B="frame",
    D="position",
    G="color",
    J="projection",
    R="region",
    T="track",
    U="timestamp",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    Z="scale",
    b="binary",
    c="panel",
    d="nodata",
    e="find",
    g="gap",
    h="header",
    i="columns",
    p="perspective",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def wiggle(self, x=None, y=None, z=None, data=None, **kwargs):
    r"""
    Plot z=f(x,y) anomalies along tracks.

    Takes a matrix, (x,y,z) triplets, or a file name as input and plots z as a
    function of distance along track.

    Must provide either ``data`` or ``x``/``y``/``z``.

    Full parameter list at :gmt-docs:`wiggle.html`

    {aliases}

    Parameters
    ----------
    x/y/z : 1d arrays
        The arrays of x and y coordinates and z data points.
    data : str or {table-like}
        Pass in either a file name to an ASCII data table, a 2D
        {table-classes}.
        Use parameter ``columns`` to choose which columns are x, y, z,
        respectively.
    {J}
    {R}
    scale : str or float
        Gives anomaly scale in data-units/distance-unit. Append **c**, **i**,
        or **p** to indicate the distance unit (cm, inch, or point); if no unit
        is given we use the default unit that is controlled by
        :gmt-term:`PROJ_LENGTH_UNIT`.
    {B}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *length*\ [**+j**\ *justify*]\ [**+al**\|\ **r**]\
        [**+o**\ *dx*\ [/*dy*]][**+l**\ [*label*]].
        Defines the reference point on the map for the vertical scale bar.
    color : str
        Set fill shade, color or pattern for positive and/or negative wiggles
        [Default is no fill]. Optionally, append **+p** to fill positive areas
        (this is the default behavior). Append **+n** to fill negative areas.
        Append **+n+p** to fill both positive and negative areas with the same
        fill. Note: You will need to repeat the color parameter to select
        different fills for the positive and negative wiggles.

    track : str
        Draw track [Default is no track]. Append pen attributes to use
        [Default is **0.25p,black,solid**].
    {U}
    {V}
    pen : str
        Specify outline pen attributes [Default is no outline].
    {XY}
    {b}
    {c}
    {d}
    {e}
    {g}
    {h}
    columns : str or 1d array
        Choose which columns are x, y, and z, respectively if input is provided
        via *data*. E.g. ``columns = [0, 1, 2]`` or ``columns = "0,1,2"`` if
        the *x* values are stored in the first column, *y* values in the second
        one and *z* values in the third one. Note: zero-based indexing is used.
    {p}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    with Session() as lib:
        # Choose how data will be passed in to the module
        file_context = lib.virtualfile_from_data(
            check_kind="vector", data=data, x=x, y=y, z=z
        )

        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("wiggle", arg_str)
