"""
plot3d - Plot in three dimensions.
"""

from pathlib import Path

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    data_kind,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)
from pygmt.src.which import which


@fmt_docstring
@use_alias(
    A="straight_line",
    B="frame",
    C="cmap",
    D="offset",
    G="fill",
    I="intensity",
    J="projection",
    Jz="zscale",
    JZ="zsize",
    L="close",
    N="no_clip",
    Q="no_sort",
    R="region",
    S="style",
    V="verbose",
    W="pen",
    Z="zvalue",
    a="aspatial",
    b="binary",
    c="panel",
    d="nodata",
    e="find",
    f="coltypes",
    g="gap",
    h="header",
    i="incols",
    l="label",
    p="perspective",
    t="transparency",
    w="wrap",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", i="sequence_comma", p="sequence")
def plot3d(  # noqa: PLR0912
    self, data=None, x=None, y=None, z=None, size=None, direction=None, **kwargs
):
    r"""
    Plot lines, polygons, and symbols in 3-D.

    Takes a matrix, (x, y, z) triplets, or a file name as input and plots
    lines, polygons, or symbols at those locations in 3-D.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    If providing data through ``x``, ``y``, and ``z``, ``fill`` can be a
    1-D array that will be mapped to a colormap.

    If a symbol is selected and no symbol size given, then plot3d will
    interpret the fourth column of the input data as symbol size. Symbols
    whose size is <= 0 are skipped. If no symbols are specified then the
    symbol code (see ``style`` below) must be present as last column in the
    input. If ``style`` is not used, a line connecting the data points will
    be drawn instead. To explicitly close polygons, use ``close``. Select a
    fill with ``fill``. If ``fill`` is set, ``pen`` will control whether the
    polygon outline is drawn or not. If a symbol is selected, ``fill`` and
    ``pen`` determine the fill and outline/no outline, respectively.

    Full option list at :gmt-docs:`plot3d.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Either a data file name, a 2-D {table-classes}.
        Optionally, use parameter ``incols`` to specify which columns are x, y,
        z, fill, and size, respectively.
    x/y/z : float or 1-D arrays
        The x, y, and z coordinates, or arrays of x, y and z coordinates of
        the data points.
    size : 1-D array
        The size of the data points in units specified in ``style``.
        Only valid if using ``x``/``y``/``z``.
    direction : list of two 1-D arrays
        If plotting vectors (using ``style="V"`` or ``style="v"``), then
        should be a list of two 1-D arrays with the vector directions. These
        can be angle and length, azimuth and length, or x and y components,
        depending on the style options chosen.
    {projection}
    zscale/zsize : float or str
        Set z-axis scaling or z-axis size.
    {region}
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
        respectively. **Note**: The ``straight_line`` parameter requires
        constant *z*-coordinates.
    {frame}
    {cmap}
    offset : str
        *dx*/*dy*\ [/*dz*].
        Offset the plot symbol or line locations by the given amounts
        *dx*/*dy*\ [/*dz*] [Default is no offset].
    {fill}
        *fill* can be a 1-D array, but it is only valid if using ``x``/``y``
        and ``cmap=True`` is also required.
    intensity : float, bool, or 1-D array
        Provide an *intensity* value (nominally in the -1 to +1 range) to
        modulate the fill color by simulating illumination. If using
        ``intensity=True``, we will instead read *intensity* from the first
        data column after the symbol parameters (if given). *intensity* can
        also be a 1-D array to set varying intensity for symbols, but it is
        only valid for ``x``/``y``/``z``.

    close : str
        [**+b**\|\ **d**\|\ **D**][**+xl**\|\ **r**\|\ *x0*]\
        [**+yl**\|\ **r**\|\ *y0*][**+p**\ *pen*].
        Force closed polygons. Full documentation is at
        :gmt-docs:`plot3d.html#l`.
    no_clip : bool or str
        [**c**\|\ **r**].
        Do **not** clip symbols that fall outside the frame boundaries
        [Default plots points whose coordinates are strictly inside the
        frame boundaries only].
        This parameter does not apply to lines and polygons which are always
        clipped to the map region. For periodic (360° longitude) maps we
        must plot all symbols twice in case they are clipped by the
        repeating boundary. ``no_clip=True`` will turn off clipping and not
        plot repeating symbols. Use ``no_clip="r"`` to turn off clipping
        but retain the plotting of such repeating symbols, or use
        ``no_clip="c"`` to retain clipping but turn off plotting of
        repeating symbols.
    no_sort : bool
        Turn off the automatic sorting of items based on their distance
        from the viewer. The default is to sort the items so that items in
        the foreground are plotted after items in the background.
    style : str
        Plot symbols. Full documentation is at :gmt-docs:`plot3d.html#s`.
    {verbose}
    {pen}
    zvalue : str
        *value*\|\ *file*.
        Instead of specifying a symbol or polygon fill and outline color
        via ``fill`` and ``pen``, give both a *value* via **zvalue** and a
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
        ``transparency`` can also be a 1-D array to set varying
        transparency for symbols, but this option is only valid if using
        ``x``/``y``/``z``.
    {wrap}
    """
    kwargs = self._preprocess(**kwargs)

    kind = data_kind(data)
    extra_arrays = []

    if kind == "vectors":  # Add more columns for vectors input
        # Parameters for vector styles
        if (
            kwargs.get("S") is not None
            and kwargs["S"][0] in "vV"
            and is_nonstr_iter(direction)
        ):
            extra_arrays.extend(direction)
        # Fill
        if is_nonstr_iter(kwargs.get("G")):
            extra_arrays.append(kwargs.get("G"))
            del kwargs["G"]
        # Size
        if is_nonstr_iter(size):
            extra_arrays.append(size)
        # Intensity and transparency
        for flag in ["I", "t"]:
            if is_nonstr_iter(kwargs.get(flag)):
                extra_arrays.append(kwargs.get(flag))
                kwargs[flag] = ""
    else:
        for name, value in [
            ("direction", direction),
            ("fill", kwargs.get("G")),
            ("size", size),
            ("intensity", kwargs.get("I")),
            ("transparency", kwargs.get("t")),
        ]:
            if is_nonstr_iter(value):
                raise GMTInvalidInput(f"'{name}' can't be 1-D array if 'data' is used.")

    # Set the default style if data has a geometry of Point or MultiPoint
    if kwargs.get("S") is None:
        if kind == "geojson" and data.geom_type.isin(["Point", "MultiPoint"]).all():
            kwargs["S"] = "u0.2c"
        elif kind == "file" and str(data).endswith(".gmt"):  # OGR_GMT file
            try:
                with Path(which(data)).open(encoding="utf-8") as file:
                    line = file.readline()
                if "@GMULTIPOINT" in line or "@GPOINT" in line:
                    kwargs["S"] = "u0.2c"
            except FileNotFoundError:
                pass

    with Session() as lib:
        with lib.virtualfile_in(
            check_kind="vector",
            data=data,
            x=x,
            y=y,
            z=z,
            extra_arrays=extra_arrays,
            required_z=True,
        ) as vintbl:
            lib.call_module(module="plot3d", args=build_arg_list(kwargs, infile=vintbl))
