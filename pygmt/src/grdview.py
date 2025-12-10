"""
grdview - Create 3-D perspective image or surface mesh from a grid.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, deprecate_parameter, fmt_docstring, use_alias

__doctest_skip__ = ["grdview"]


@fmt_docstring
@deprecate_parameter("contourpen", "contour_pen", "v0.18.0", remove_version="v0.20.0")
@deprecate_parameter("facadepen", "facade_pen", "v0.18.0", remove_version="v0.20.0")
@deprecate_parameter("meshpen", "mesh_pen", "v0.18.0", remove_version="v0.20.0")
@use_alias(
    C="cmap",
    G="drapegrid",
    N="plane",
    I="shading",
    f="coltypes",
    n="interpolation",
)
def grdview(  # noqa: PLR0913
    self,
    grid: PathLike | xr.DataArray,
    surftype: Literal[
        "mesh", "surface", "surface+mesh", "image", "waterfall_x", "waterfall_y"
    ]
    | None = None,
    dpi: int | None = None,
    mesh_fill: float | None = None,
    nan_transparent: bool = False,
    monochrome: bool = False,
    contour_pen: str | None = None,
    facade_pen: str | None = None,
    mesh_pen: str | None = None,
    projection: str | None = None,
    zscale: float | str | None = None,
    zsize: float | str | None = None,
    frame: str | Sequence[str] | bool = False,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    transparency: float | None = None,
    perspective: float | Sequence[float] | str | bool = False,
    **kwargs,
):
    r"""
    Create 3-D perspective image or surface mesh from a grid.

    Reads a 2-D grid file and produces a 3-D perspective plot by drawing a mesh,
    painting a colored/gray-shaded surface made up of polygons, or by scanline
    conversion of these polygons to a raster image. Options include draping a data
    set on top of a surface, plotting of contours on top of the surface, and apply
    artificial illumination based on intensities provided in a separate grid file.

    Full GMT docs at :gmt-docs:`grdview.html`.

    $aliases
       - B = frame
       - J = projection
       - Jz = zscale
       - JZ = zsize
       - R = region
       - Q = surftype, dpi, mesh_fill, nan_transparent, monochrome
       - V = verbose
       - Wc = contour_pen
       - Wf = facade_pen
       - Wm = mesh_pen
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    $grid
    region : str or list
        *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*].
        Specify the :doc:`region </tutorials/basics/regions>` of interest. When used
        with ``perspective``, optionally append */zmin/zmax* to indicate the range to
        use for the 3-D axes [Default is the region given by the input grid].
    $projection
    zscale/zsize
        Set z-axis scaling or z-axis size.
    $frame
    cmap : str
        The name of the color palette table to use.
    drapegrid : str or :class:`xarray.DataArray`
        The file name or a :class:`xarray.DataArray` of the image grid to be draped on
        top of the relief provided by ``grid`` [Default determines colors from ``grid``]
        Note that ``zscale`` and ``plane`` always refer to ``grid``. ``drapegrid`` only
        provides the information pertaining to colors, which (if ``drapegrid`` is a
        grid) will be looked-up via the CPT (see ``cmap``).
    plane : float or str
        *level*\ [**+g**\ *fill*].
        Draw a plane at this z-level. If the optional color is provided via the **+g**
        modifier, and the projection is not oblique, the frontal facade between the
        plane and the data perimeter is colored.
    surftype
        Specify surface type of the grid. Valid values are:

        - ``"mesh"``: mesh plot [Default].
        - ``"surface``: surface plot.
        - ``"surface+mesh"``: surface plot with mesh lines drawn on top of the surface.
        - ``"image"``: image plot.
        - ``"waterfall_x"``/``"waterfall_y"``: waterfall plots (row or column profiles).
    dpi
        Effective dots-per-unit resolution for the rasterization for image plots (i.e.,
        ``surftype="image"``) [Default is :gmt-term:`GMT_GRAPHICS_DPU`]
    mesh_fill
        Set the mesh fill in mesh plot or waterfall plots [Default is white].
    nan_transparent
        Make grid nodes with z = NaN transparent, using the color-masking feature in
        PostScript Level 3. Only applies when ``surftype="image"``.
    monochrome
        Force conversion to monochrome image using the (television) YIQ transformation.
    contour_pen
        Draw contour lines on top of surface or mesh (not image). Append pen attributes
        used for the contours.
    facade_pen
        Set the pen attributes used for the facade. You must also select ``plane`` for
        the facade outline to be drawn.
    mesh_pen
        Set the pen attributes used for the mesh. Need to set ``surftype`` to
        ``"mesh"``, or ``"surface+mesh"`` to draw meshlines.
    shading : str
        Provide the name of a grid file with intensities in the (-1,+1) range, or a
        constant intensity to apply everywhere (affects the ambient light).
        Alternatively, derive an intensity grid from the main input data grid by using
        :func:`pygmt.grdgradient` first; append **+a**\ *azimuth*, **+n**\ *args*, and
        **+m**\ *ambient* to specify azimuth, intensity, and ambient arguments for that
        function, or just give **+d** to select the default arguments [Default is
        ``"+a-45+nt1+m0"``].
    $verbose
    $panel
    $coltypes
    $interpolation
    $perspective
    $transparency

    Example
    -------
    >>> import pygmt
    >>> # Load the 30 arc-minutes grid with "gridline" registration in a given region
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m",
    ...     region=[-92.5, -82.5, -3, 7],
    ...     registration="gridline",
    ... )
    >>> # Create a new figure instance with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # Create the contour plot
    >>> fig.grdview(
    ...     # Pass in the grid downloaded above
    ...     grid=grid,
    ...     # Set the perspective to an azimuth of 130° and an elevation of 30°
    ...     perspective=[130, 30],
    ...     # Add a frame to the x- and y-axes
    ...     # Specify annotations on the south and east borders of the plot
    ...     frame=["xa", "ya", "wSnE"],
    ...     # Set the projection of the 2-D map to Mercator with a 10 cm width
    ...     projection="M10c",
    ...     # Set the vertical scale (z-axis) to 2 cm
    ...     zsize="2c",
    ...     # Set "surface plot" to color the surface via a CPT
    ...     surftype="surface",
    ...     # Specify CPT to "geo"
    ...     cmap="geo",
    ... )
    >>> # Show the plot
    >>> fig.show()
    """
    self._activate_figure()

    if dpi is not None and surftype != "image":
        msg = "Parameter 'dpi' can only be used when 'surftype' is 'image'."
        raise GMTInvalidInput(msg)
    if nan_transparent and surftype != "image":
        msg = "Parameter 'nan_transparent' can only be used when 'surftype' is 'image'."
        raise GMTInvalidInput(msg)
    if mesh_fill is not None and surftype not in {"mesh", "waterfall_x", "waterfall_y"}:
        msg = (
            "Parameter 'mesh_fill' can only be used when 'surftype' is 'mesh', "
            "'waterfall_x', or 'waterfall_y'."
        )
        raise GMTInvalidInput(msg)

    _surftype_mapping = {
        "surface": "s",
        "mesh": "m",
        "surface+mesh": "sm",
        "image": "c" if nan_transparent is True else "i",
        "waterfall_x": "mx",
        "waterfall_y": "my",
    }

    # Previously, 'surftype' was aliased to Q.
    _old_surftype_syntax = surftype is not None and surftype not in _surftype_mapping

    if _old_surftype_syntax and any(
        v not in {None, False} for v in (dpi, mesh_fill, monochrome, nan_transparent)
    ):
        msg = (
            "Parameter 'surftype' is given with a raw GMT command string, and conflicts "
            "with parameters 'dpi', 'mesh_fill', 'monochrome', or 'nan_transparent'."
        )
        raise GMTInvalidInput(msg)

    aliasdict = AliasSystem(
        Jz=Alias(zscale, name="zscale"),
        JZ=Alias(zsize, name="zsize"),
        Q=[
            Alias(
                surftype,
                name="surftype",
                mapping=_surftype_mapping if not _old_surftype_syntax else None,
            ),
            Alias(dpi, name="dpi"),
            Alias(mesh_fill, name="mesh_fill"),
            Alias(monochrome, name="monochrome", prefix="+m"),
        ],
        Wc=Alias(contour_pen, name="contour_pen"),
        Wf=Alias(facade_pen, name="facade_pen"),
        Wm=Alias(mesh_pen, name="mesh_pen"),
    ).add_common(
        B=frame,
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_in(
                check_kind="raster", data=kwargs.get("G"), required=False
            ) as vdrapegrid,
        ):
            aliasdict["G"] = vdrapegrid
            lib.call_module(
                module="grdview", args=build_arg_list(aliasdict, infile=vingrd)
            )
