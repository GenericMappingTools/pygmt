"""
plot - Plot lines, polygons, and symbols in 2-D.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput, GMTTypeError
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)
from pygmt.src._common import _data_geometry_is_point


@fmt_docstring
@use_alias(
    B="frame",
    C="cmap",
    D="offset",
    E="error_bar",
    F="connection",
    G="fill",
    I="intensity",
    L="close",
    N="no_clip",
    S="style",
    W="pen",
    Z="zvalue",
    a="aspatial",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    g="gap",
    h="header",
    i="incols",
    l="label",
    p="perspective",
    w="wrap",
)
@kwargs_to_strings(i="sequence_comma", p="sequence")
def plot(  # noqa: PLR0912, PLR0913
    self,
    data: PathLike | TableLike | None = None,
    x=None,
    y=None,
    size=None,
    symbol=None,
    direction=None,
    straight_line: bool | Literal["x", "y"] = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | Sequence[float] | bool | None = None,
    **kwargs,
):
    r"""
    Plot lines, polygons, and symbols in 2-D.

    Takes a matrix, (x,y) pairs, or a file name as input and plots lines,
    polygons, or symbols at those locations on a map.

    Must provide either ``data`` or ``x``/``y``.

    If providing data through ``x``/``y``, ``fill`` can be a 1-D array that
    will be mapped to a colormap.

    If a symbol is selected and no symbol size given, then plot will
    interpret the third column of the input data as symbol size. Symbols
    whose size is <= 0 are skipped. If no symbols are specified then the
    symbol code (see ``style`` below) must be present as last column in the
    input. If ``style`` is not used, a line connecting the data points will
    be drawn instead. To explicitly close polygons, use ``close``. Select a
    fill with ``fill``. If ``fill`` is set, ``pen`` will control whether the
    polygon outline is drawn or not. If a symbol is selected, ``fill`` and
    ``pen`` determine the fill and outline/no outline, respectively.

    Full GMT docs at :gmt-docs:`plot.html`.

    {aliases}
       - A = straight_line
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    data
        Pass in either a file name to an ASCII data table, a 2-D
        {table-classes}.
        Use parameter ``incols`` to choose which columns are x, y, fill, and
        size, respectively.
    x/y : float or 1-D arrays
        The x and y coordinates, or arrays of x and y coordinates of the
        data points
    size : 1-D array
        The size of the data points in units specified using ``style``.
        Only valid if using ``x``/``y``.
    symbol : 1-D array
        The symbols of the data points. Only valid if using ``x``/``y``.
    direction : list of two 1-D arrays
        If plotting vectors (using ``style="V"`` or ``style="v"``), then
        should be a list of two 1-D arrays with the vector directions. These
        can be angle and length, azimuth and length, or x and y components,
        depending on the style options chosen.
    {projection}
    {region}
    straight_line
        By default, line segments are drawn as straight lines in the Cartesian and polar
        coordinate systems, and as great circle arcs (by resampling coarse input data
        along such arcs) in the geographic coordinate system. The ``straight_line``
        parameter can control the drawing of line segments. Valid values are:

        - ``True``: Draw line segments as straight lines in geographic coordinate
          systems.
        - ``"x"``: Draw line segments by first along *x*, then along *y*.
        - ``"y"``: Draw line segments by first along *y*, then along *x*.

        Here, *x* and *y* have different meanings depending on the coordinate system:

        - **Cartesian** coordinate system: *x* and *y* are the X- and Y-axes.
        - **Polar** coordinate system: *x* and *y* are theta and radius.
        - **Geographic** coordinate system: *x* and *y* are parallels and meridians.

        .. attention::

            There exits a bug in GMT<=6.5.0 that, in geographic coordinate systems, the
            meaning of *x* and *y* is reversed, i.e., *x* means meridians and *y* means
            parallels. The bug is fixed by upstream
            `PR #8648 <https://github.com/GenericMappingTools/gmt/pull/8648>`__.
    {frame}
    {cmap}
    offset : str
        *dx*/*dy*.
        Offset the plot symbol or line locations by the given amounts
        *dx/dy* [Default is no offset]. If *dy* is not given it is set
        equal to *dx*.
    error_bar : bool or str
        [**x**\|\ **y**\|\ **X**\|\ **Y**][**+a**\|\ **A**]\
        [**+cl**\|\ **f**][**+n**][**+w**\ *cap*][**+p**\ *pen*].
        Draw error bars. Full documentation is at
        :gmt-docs:`plot.html#e`.
    connection : str
        [**c**\|\ **n**\|\ **p**][**a**\|\ **r**\|\ **s**\|\ **t**\|\ *refpoint*].
        Alter the way points are connected (by specifying a *scheme*) and data are
        grouped (by specifying a *method*). Append one of three line connection schemes:

        - **c**: Draw continuous line segments for each group [Default].
        - **n**: Draw networks of line segments between all points in each group.
        - **p**: Draw line segments from a reference point reset for each group.

        Optionally, append the one of four segmentation methods to define the group:

        - **a**: Ignore all segment headers, i.e., let all points belong to a single
          group, and set group the reference point to the very first point of the first
          file.
        - **r**: Segment headers are honored so each segment is a group; the group
          reference point is reset after each record to the previous point (this method
          is only available with the ``connection="p"`` scheme).
        - **s**: Same as **r**, but the group reference point is reset to the first
          point of each incoming segment [Default].
        - **t**: Consider all data in each file to be a single separate group and reset
          the group reference point to the first point of each group.

        Instead of the codes **a**\|\ **r**\|\ **s**\|\ **t** you may append the
        coordinates of a *refpoint* which will serve as a fixed external reference point
        for all groups.
    {fill}
        *fill* can be a 1-D array, but it is only valid if using ``x``/``y``
        and ``cmap=True`` is also required.
    intensity : float, bool, or 1-D array
        Provide an *intensity* value (nominally in the -1 to +1 range) to
        modulate the fill color by simulating illumination. If using
        ``intensity=True``, we will instead read *intensity* from the first
        data column after the symbol parameters (if given). *intensity* can
        also be a 1-D array to set varying intensity for symbols, but it is
        only valid for ``x``/``y`` pairs.
    close : str
        [**+b**\|\ **d**\|\ **D**][**+xl**\|\ **r**\|\ *x0*]\
        [**+yl**\|\ **r**\|\ *y0*][**+p**\ *pen*].
        Force closed polygons. Full documentation is at
        :gmt-docs:`plot.html#l`.
    no_clip : bool or str
        [**c**\|\ **r**].
        Do **not** clip symbols that fall outside the frame boundaries
        [Default plots points whose coordinates are strictly inside the
        frame boundaries only].
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
    {pen}
    {verbose}
    zvalue : str
        *value*\|\ *file*.
        Instead of specifying a symbol or polygon fill and outline color
        via ``fill`` and ``pen``, give both a *value* via ``zvalue`` and a
        color lookup table via ``cmap``.  Alternatively, give the name of a
        *file* with one z-value (read from the last column) for each
        polygon in the input data. To apply it to the fill color, use
        ``fill="+z"``. To apply it to the pen color, append **+z** to
        ``pen``.
    {aspatial}
    {binary}
    {panel}
    {nodata}
    {find}
    {coltypes}
    {gap}
    {header}
    {incols}
    {label}
    {perspective}
    {transparency}
        ``transparency`` can also be a 1-D array to set varying transparency for
        symbols, but this option is only valid if using ``x``/``y``.
    {wrap}
    """
    # TODO(GMT>6.5.0): Remove the note for the upstream bug of the "straight_line"
    # parameter.
    self._activate_figure()

    kind = data_kind(data)
    if kind == "empty":  # Data is given via a series of vectors.
        data = {"x": x, "y": y}
        # Parameters for vector styles
        if (
            isinstance(kwargs.get("S"), str)
            and len(kwargs["S"]) >= 1
            and kwargs["S"][0] in "vV"
            and is_nonstr_iter(direction)
        ):
            data.update({"x2": direction[0], "y2": direction[1]})
        # Fill
        if is_nonstr_iter(kwargs.get("G")):
            data["fill"] = kwargs.pop("G")
        # Size
        if is_nonstr_iter(size):
            data["size"] = size
        # Intensity
        if is_nonstr_iter(kwargs.get("I")):
            data["intensity"] = kwargs["I"]
            kwargs["I"] = ""
        # Transparency
        if is_nonstr_iter(transparency):
            data["transparency"] = transparency
            transparency = True
        # Symbol must be at the last column
        if is_nonstr_iter(symbol):
            if "S" not in kwargs:
                kwargs["S"] = True
            data["symbol"] = symbol
    else:
        if any(v is not None for v in (x, y)):
            msg = "Too much data. Use either data or x/y/z."
            raise GMTInvalidInput(msg)
        for name, value in [
            ("direction", direction),
            ("fill", kwargs.get("G")),
            ("size", size),
            ("intensity", kwargs.get("I")),
            ("transparency", transparency),
            ("symbol", symbol),
        ]:
            if is_nonstr_iter(value):
                raise GMTTypeError(
                    type(value),
                    reason=f"Parameter {name!r} can't be a 1-D array if 'data' is used.",
                )

    # Set the default style if data has a geometry of Point or MultiPoint
    if kwargs.get("S") is None and _data_geometry_is_point(data, kind):
        kwargs["S"] = "s0.2c"

    aliasdict = AliasSystem(
        A=Alias(straight_line, name="straight_line"),
    ).add_common(
        R=region,
        J=projection,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(check_kind="vector", data=data) as vintbl:
            lib.call_module(
                module="plot", args=build_arg_list(aliasdict, infile=vintbl)
            )
