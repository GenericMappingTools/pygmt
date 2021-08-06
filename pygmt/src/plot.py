"""
plot - Plot in two dimensions.
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    deprecate_parameter,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@deprecate_parameter("sizes", "size", "v0.4.0", remove_version="v0.6.0")
@deprecate_parameter("columns", "incols", "v0.4.0", remove_version="v0.6.0")
@use_alias(
    A="straight_line",
    B="frame",
    C="cmap",
    D="offset",
    E="error_bar",
    F="connection",
    G="color",
    I="intensity",
    J="projection",
    L="close",
    N="no_clip",
    R="region",
    S="style",
    U="timestamp",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    Z="zvalue",
    a="aspatial",
    i="incols",
    l="label",
    c="panel",
    f="coltypes",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def plot(self, x=None, y=None, data=None, size=None, direction=None, **kwargs):
    r"""
    Plot lines, polygons, and symbols in 2-D.

    Takes a matrix, (x,y) pairs, or a file name as input and plots lines,
    polygons, or symbols at those locations on a map.

    Must provide either ``data`` or ``x``/``y``.

    If providing data through ``x``/``y``, ``color`` can be a 1d array that
    will be mapped to a colormap.

    If a symbol is selected and no symbol size given, then plot will
    interpret the third column of the input data as symbol size. Symbols
    whose size is <= 0 are skipped. If no symbols are specified then the
    symbol code (see ``style`` below) must be present as last column in the
    input. If ``style`` is not used, a line connecting the data points will
    be drawn instead. To explicitly close polygons, use ``close``. Select a
    fill with ``color``. If ``color`` is set, ``pen`` will control whether the
    polygon outline is drawn or not. If a symbol is selected, ``color`` and
    ``pen`` determines the fill and outline/no outline, respectively.

    Full parameter list at :gmt-docs:`plot.html`

    {aliases}

    Parameters
    ----------
    x/y : float or 1d arrays
        The x and y coordinates, or arrays of x and y coordinates of the
        data points
    data : str or {table-like}
        Pass in either a file name to an ASCII data table, a 2D
        {table-classes}.
        Use parameter ``incols`` to choose which columns are x, y, color, and
        size, respectively.
    size : 1d array
        The size of the data points in units specified using ``style``.
        Only valid if using ``x``/``y``.
    direction : list of two 1d arrays
        If plotting vectors (using ``style='V'`` or ``style='v'``), then
        should be a list of two 1d arrays with the vector directions. These
        can be angle and length, azimuth and length, or x and y components,
        depending on the style options chosen.
    {J}
    {R}
    straight_line : bool or str
        [**m**\|\ **p**\|\ **x**\|\ **y**].
        By default, geographic line segments are drawn as great circle
        arcs. To draw them as straight lines, use ``straight_line``.
        Alternatively, add **m** to draw the line by first following a
        meridian, then a parallel. Or append **p** to start following a
        parallel, then a meridian. (This can be practical to draw a line
        along parallels, for example). For Cartesian data, points are
        simply connected, unless you append **x** or **y** to draw
        stair-case curves that whose first move is along *x* or *y*,
        respectively.
    {B}
    {CPT}
    offset : str
        *dx*/*dy*.
        Offset the plot symbol or line locations by the given amounts
        *dx/dy* [Default is no offset]. If *dy* is not given it is set
        equal to *dx*.
    error_bar : bool or str
        [**+b**\|\ **d**\|\ **D**][**+xl**\|\ **r**\|\ *x0*]\
        [**+yl**\|\ **r**\|\ *y0*][**+p**\ *pen*].
        Draw symmetrical error bars. Full documentation is at
        :gmt-docs:`plot.html#e`.
    connection : str
        [**c**\|\ **n**\|\ **r**]\
        [**a**\|\ **f**\|\ **s**\|\ **r**\|\ *refpoint*].
        Alter the way points are connected (by specifying a *scheme*) and
        data are grouped (by specifying a *method*). Append one of three
        line connection schemes:

        - **c** : Draw continuous line segments for each group [Default].
        - **r** : Draw line segments from a reference point reset for each
          group.
        - **n** : Draw networks of line segments between all points in
          each group.

        Optionally, append the one of four segmentation methods to define
        the group:

        - **a** : Ignore all segment headers, i.e., let all points belong
          to a single group, and set group reference point to the very
          first point of the first file.
        - **f** : Consider all data in each file to be a single separate
          group and reset the group reference point to the first point of
          each group.
        - **s** : Segment headers are honored so each segment is a group;
          the group reference point is reset to the first point of each
          incoming segment [Default].
        - **r** : Same as **s**, but the group reference point is reset
          after each record to the previous point (this method is only
          available with the ``connection='r'`` scheme).

        Instead of the codes **a**\|\ **f**\|\ **s**\|\ **r** you may append
        the coordinates of a *refpoint* which will serve as a fixed external
        reference point for all groups.
    {G}
        *color* can be a 1d array, but it is only valid if using ``x``/``y``
        and ``cmap=True`` is also required.
    intensity : float or bool or 1d array
        Provide an *intensity* value (nominally in the -1 to +1 range) to
        modulate the fill color by simulating illumination. If using
        ``intensity=True``, we will instead read *intensity* from the first
        data column after the symbol parameters (if given). *intensity* can
        also be a 1d array to set varying intensity for symbols, but it is only
        valid for ``x``/``y`` pairs.
    close : str
        [**+b**\|\ **d**\|\ **D**][**+xl**\|\ **r**\|\ *x0*]\
        [**+yl**\|\ **r**\|\ *y0*][**+p**\ *pen*].
        Force closed polygons. Full documentation is at
        :gmt-docs:`plot.html#l`.
    no_clip : bool or str
        [**c**\|\ **r**].
        Do NOT clip symbols that fall outside map border [Default plots
        points whose coordinates are strictly inside the map border only].
        The parameter does not apply to lines and polygons which are always
        clipped to the map region. For periodic (360-longitude) maps we
        must plot all symbols twice in case they are clipped by the
        repeating boundary. ``no_clip=True`` will turn off clipping and not
        plot repeating symbols. Use ``no_clip="r"`` to turn off clipping
        but retain the plotting of such repeating symbols, or use
        ``no_clip="c"`` to retain clipping but turn off plotting of
        repeating symbols.
    style : str
        Plot symbols (including vectors, pie slices, fronts, decorated or
        quoted lines).
    {W}
    {U}
    {V}
    {XY}
    zvalue : str
        *value*\|\ *file*.
        Instead of specifying a symbol or polygon fill and outline color
        via ``color`` and ``pen``, give both a *value* via ``zvalue`` and a
        color lookup table via ``cmap``.  Alternatively, give the name of a
        *file* with one z-value (read from the last column) for each
        polygon in the input data. To apply it to the fill color, use
        ``color='+z'``. To apply it to the pen color, append **+z** to
        ``pen``.
    {a}
    {c}
    {f}
    {i}
    {l}
    {p}
    {t}
        *transparency* can also be a 1d array to set varying transparency
        for symbols, but this option is only valid if using x/y.
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    kind = data_kind(data, x, y)

    extra_arrays = []
    if "S" in kwargs and kwargs["S"][0] in "vV" and direction is not None:
        extra_arrays.extend(direction)
    if "G" in kwargs and not isinstance(kwargs["G"], str):
        if kind != "vectors":
            raise GMTInvalidInput(
                "Can't use arrays for color if data is matrix or file."
            )
        extra_arrays.append(kwargs["G"])
        del kwargs["G"]
    if size is not None:
        if kind != "vectors":
            raise GMTInvalidInput(
                "Can't use arrays for 'size' if data is a matrix or file."
            )
        extra_arrays.append(size)

    for flag in ["I", "t"]:
        if flag in kwargs and is_nonstr_iter(kwargs[flag]):
            if kind != "vectors":
                raise GMTInvalidInput(
                    f"Can't use arrays for {plot.aliases[flag]} if data is matrix or file."
                )
            extra_arrays.append(kwargs[flag])
            kwargs[flag] = ""

    with Session() as lib:
        # Choose how data will be passed in to the module
        file_context = lib.virtualfile_from_data(
            check_kind="vector", data=data, x=x, y=y, extra_arrays=extra_arrays
        )

        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("plot", arg_str)
