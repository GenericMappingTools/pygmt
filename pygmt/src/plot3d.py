"""
plot3d - Plot in three dimensions.
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
from pygmt.src.which import which


@fmt_docstring
@deprecate_parameter("color", "fill", "v0.8.0", remove_version="v0.12.0")
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
def plot3d(
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
    data : str or {table-like}
        Either a data file name, a 2-D {table-classes}.
        Optionally, use parameter ``incols`` to specify which columns are x, y,
        z, fill, and size, respectively.
    x/y/z : float or 1-D arrays
        The x, y, and z coordinates, or arrays of x, y and z coordinates of
        the data points
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
    intensity : float or bool or 1-D array
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
        Do NOT clip symbols that fall outside map border [Default plots
        points whose coordinates are strictly inside the map border only].
        This parameter does not apply to lines and polygons which are always
        clipped to the map region. For periodic (360-longitude) maps we
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
    {timestamp}
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
    # pylint: disable=too-many-locals
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    kind = data_kind(data, x, y, z)

    extra_arrays = []
    if kwargs.get("S") is not None and kwargs["S"][0] in "vV" and direction is not None:
        extra_arrays.extend(direction)
    elif (
        kwargs.get("S") is None
        and kind == "geojson"
        and data.geom_type.isin(["Point", "MultiPoint"]).all()
    ):  # checking if the geometry of a geoDataFrame is Point or MultiPoint
        kwargs["S"] = "u0.2c"
    elif kwargs.get("S") is None and kind == "file" and str(data).endswith(".gmt"):
        # checking that the data is a file path to set default style
        try:
            with open(which(data), mode="r", encoding="utf8") as file:
                line = file.readline()
            if "@GMULTIPOINT" in line or "@GPOINT" in line:
                # if the file is gmt style and geometry is set to Point
                kwargs["S"] = "u0.2c"
        except FileNotFoundError:
            pass
    if kwargs.get("G") is not None and is_nonstr_iter(kwargs["G"]):
        if kind != "vectors":
            raise GMTInvalidInput(
                "Can't use arrays for fill if data is matrix or file."
            )
        extra_arrays.append(kwargs["G"])
        del kwargs["G"]
    if size is not None:
        if kind != "vectors":
            raise GMTInvalidInput(
                "Can't use arrays for 'size' if data is a matrix or a file."
            )
        extra_arrays.append(size)

    for flag in ["I", "t"]:
        if kwargs.get(flag) is not None and is_nonstr_iter(kwargs[flag]):
            if kind != "vectors":
                raise GMTInvalidInput(
                    f"Can't use arrays for {plot3d.aliases[flag]} if data is matrix or file."
                )
            extra_arrays.append(kwargs[flag])
            kwargs[flag] = ""

    with Session() as lib:
        # Choose how data will be passed in to the module
        file_context = lib.virtualfile_from_data(
            check_kind="vector",
            data=data,
            x=x,
            y=y,
            z=z,
            extra_arrays=extra_arrays,
            required_z=True,
        )

        with file_context as fname:
            lib.call_module(
                module="plot3d", args=build_arg_string(kwargs, infile=fname)
            )
