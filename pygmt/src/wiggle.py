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
    c="panel",
    i="columns",
    p="perspective",
    t="transparency",
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
    x/y/z : float or 1d arrays
        The x and y coordinates, or arrays of x and y coordinates of the
        z data point or an array of z data points.
    data : str or 2d array
        Either a data file name or a 2d numpy array with the tabular data.
        Use parameter ``columns`` to choose which columns are x, y, z,
        respectively.
    {J}
    {R}
    scale : str or float
        Gives anomaly scale in data-units/distance-unit. Append **c**, **i**,
        or **p** to indicate the distance unit (cm, inch, or point); if no unit
        is given we use the default unit that is controlled by
        :gmt-docs:`PROJ_LENGTH_UNIT <gmt.conf.html#term-PROJ_LENGTH_UNIT>`.
    {B}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\
        **+w**\ *length*\ [**+j**\ *justify*]\ [**+al**\ |\ **r**]\
        [**+o**\ *dx*\ [/*dy*]][**+l**\ [*label*]]
        Defines the reference point on the map for the vertical scale bar.
    {G}
    track : str
        Draw track [Default is no track]. Append pen attributes to use
        [Defaults: width = 0.25p, color = black, style = solid].
    {U}
    {V}
    {W}
    {XY}
    {c}
    columns : str or 1d array
        Choose which columns are x, y, and z, respectively if input is provided
        via *data*. E.g. ``columns = [0, 1, 2]`` or ``columns = "0,1,2"`` if
        the *x* values are stored in the first column, *y* values in the second
        one and *z* values in the third one. Note: zero-based indexing is used.
    {p}
    {t}
        *transparency* can also be a 1d array to set varying transparency
        for symbols.
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
