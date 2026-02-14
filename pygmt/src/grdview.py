"""
grdview - Create 3-D perspective image or surface mesh from a grid.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from packaging.version import Version
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session, __gmt_version__
from pygmt.exceptions import GMTParameterError
from pygmt.helpers import build_arg_list, deprecate_parameter, fmt_docstring, use_alias
from pygmt.src.grdinfo import grdinfo

__doctest_skip__ = ["grdview"]


def _alias_option_Q(  # noqa: N802
    surftype=None, dpi=None, mesh_fill=None, monochrome=False, nan_transparent=False
):
    """
    Helper function to build the Alias list for the -Q option.

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return AliasSystem(Q=_alias_option_Q(**kwargs)).get("Q")
    >>> parse(surftype="surface")
    's'
    >>> parse(surftype="mesh")
    'm'
    >>> parse(surftype="surface+mesh")
    'sm'
    >>> parse(surftype="waterfall_x")
    'mx'
    >>> parse(surftype="waterfall_y")
    'my'
    >>> parse(surftype="image")
    'i'
    >>> parse(surftype="image", nan_transparent=True)
    'c'
    >>> parse(surftype="image", dpi=150)
    'i150'
    >>> parse(surftype="image", dpi=150, nan_transparent=True)
    'c150'
    >>> parse(surftype="mesh", mesh_fill="blue")
    'mblue'
    >>> parse(surftype="surface", monochrome=True)
    's+m'
    >>> parse(surftype="surface+mesh", monochrome=True)
    'sm+m'

    >>> # Check for backward compatibility with old raw GMT syntax.
    >>> for surftype in ["s", "m", "sm", "i", "c", "mx", "my", "mblue", "i150"]:
    ...     assert parse(surftype=surftype) == surftype
    """
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
        v is not None and v is not False
        for v in (dpi, mesh_fill, monochrome, nan_transparent)
    ):
        raise GMTParameterError(
            conflicts_with=(
                "surftype",
                ["dpi", "mesh_fill", "monochrome", "nan_transparent"],
            ),
            reason="'surftype' is specified using the unrecommended GMT command string syntax.",
        )

    if dpi is not None and surftype != "image":
        raise GMTParameterError(
            conflicts_with=("dpi", [f"surftype={surftype!r}"]),
            reason="'dpi' is allowed only when 'surftype' is 'image'.",
        )
    if nan_transparent and surftype != "image":
        raise GMTParameterError(
            conflicts_with=("nan_transparent", [f"surftype={surftype!r}"]),
            reason="'nan_transparent' is allowed only when 'surftype' is 'image'.",
        )
    if mesh_fill is not None and surftype not in {"mesh", "waterfall_x", "waterfall_y"}:
        raise GMTParameterError(
            conflicts_with=("mesh_fill", [f"surftype={surftype!r}"]),
            reason="'mesh_fill' is allowed only when 'surftype' is 'mesh', 'waterfall_x', or 'waterfall_y'.",
        )

    return [
        Alias(
            surftype,
            name="surftype",
            mapping=_surftype_mapping if not _old_surftype_syntax else None,
        ),
        Alias(dpi, name="dpi"),
        Alias(mesh_fill, name="mesh_fill"),
        Alias(monochrome, name="monochrome", prefix="+m"),
    ]


@fmt_docstring
# TODO(PyGMT>=0.20.0): Remove the deprecated '*pen' parameters.
# TODO(PyGMT>=0.20.0): Remove the deprecated 'drapegrid' parameter.
@deprecate_parameter("contourpen", "contour_pen", "v0.18.0", remove_version="v0.20.0")
@deprecate_parameter("facadepen", "facade_pen", "v0.18.0", remove_version="v0.20.0")
@deprecate_parameter("meshpen", "mesh_pen", "v0.18.0", remove_version="v0.20.0")
@deprecate_parameter("drapegrid", "drape_grid", "v0.18.0", remove_version="v0.20.0")
@use_alias(C="cmap", G="drape_grid", I="shading", f="coltypes", n="interpolation")
def grdview(  # noqa: PLR0913
    self,
    grid: PathLike | xr.DataArray,
    surftype: Literal[
        "mesh", "surface", "surface+mesh", "image", "waterfall_x", "waterfall_y"
    ]
    | None = None,
    dpi: int | None = None,
    nan_transparent: bool = False,
    monochrome: bool = False,
    contour_pen: str | None = None,
    mesh_fill: str | None = None,
    mesh_pen: str | None = None,
    plane: float | bool = False,
    facade_fill: str | None = None,
    facade_pen: str | None = None,
    projection: str | None = None,
    zscale: float | str | None = None,
    zsize: float | str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: str | Sequence[str] | Literal["none"] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
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
       - N = plane, facade_fill
       - R = region
       - Q = surftype, dpi, mesh_fill, nan_transparent, **+m**: monochrome
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
    cmap : str
        The name of the color palette table to use.
    drape_grid : str or :class:`xarray.DataArray`
        The file name or a :class:`xarray.DataArray` of the image grid to be draped on
        top of the relief provided by ``grid`` [Default determines colors from ``grid``]
        Note that ``zscale`` and ``plane`` always refer to ``grid``. ``drape_grid`` only
        provides the information pertaining to colors, which (if ``drape_grid`` is a
        grid) will be looked-up via the CPT (see ``cmap``).
    surftype
        Specify surface type for the grid. Valid values are:

        - ``"mesh"``: mesh plot [Default].
        - ``"surface"``: surface plot.
        - ``"surface+mesh"``: surface plot with mesh lines drawn on top of the surface.
        - ``"image"``: image plot.
        - ``"waterfall_x"``/``"waterfall_y"``: waterfall plots (row or column profiles).
    dpi
        Effective dots-per-unit resolution for the rasterization for image plots (i.e.,
        ``surftype="image"``) [Default is :gmt-term:`GMT_GRAPHICS_DPU`]
    nan_transparent
        Make grid nodes with z = NaN transparent, using the color-masking feature in
        PostScript Level 3. Only applies when ``surftype="image"``.
    monochrome
        Force conversion to monochrome image using the (television) YIQ transformation.
    contour_pen
        Draw contour lines on top of surface or mesh (not image). Append pen attributes
        used for the contours.
    mesh_pen
        Set the pen attributes used for the mesh. Need to set ``surftype`` to
        ``"mesh"``, or ``"surface+mesh"`` to draw meshlines.
    mesh_fill
        Set the mesh fill in mesh plot or waterfall plots [Default is white].
    plane
        Draw a plane at the specified z-level. If ``True``, defaults to the minimum
        value in the grid. However, if ``region`` was used to set *zmin/zmax* then
        *zmin* is used if it is less than the grid minimum value. Use ``facade_pen`` and
        ``facade_fill`` to control the appearance of the plane.
        **Note**: For GMT<=6.6.0, *zmin* set in ``region`` has no effect due to a GMT
        bug.
    facade_fill
        Fill for the frontal facade between the plane specified by ``plane`` and the
        data perimeter.
    facade_pen
        Set the pen attributes used for the facade.
    shading : str or float
        Provide the name of a grid file with intensities in the (-1,+1) range, or a
        constant intensity to apply everywhere (affects the ambient light).
        Alternatively, derive an intensity grid from the main input data grid by using
        :func:`pygmt.grdgradient` first; append **+a**\ *azimuth*, **+n**\ *args*, and
        **+m**\ *ambient* to specify azimuth, intensity, and ambient arguments for that
        function, or just give **+d** to select the default arguments [Default is
        ``"+a-45+nt1+m0"``].
    $projection
    zscale
    zsize
        Set z-axis scaling or z-axis size.
    region : str or list
        *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*].
        Specify the :doc:`region </tutorials/basics/regions>` of interest. When used
        with ``perspective``, optionally append */zmin/zmax* to indicate the range to
        use for the 3-D axes [Default is the region given by the input grid].
    $frame
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
    ...     cmap="gmt/geo",
    ... )
    >>> # Show the plot
    >>> fig.show()
    """
    self._activate_figure()

    # Enable 'plane' if 'facade_fill' or 'facade_pen' are set
    if plane is False and (facade_fill is not None or facade_pen is not None):
        plane = True

    # Workaround for GMT bug https://github.com/GenericMappingTools/gmt/pull/8838
    # Fix the plane value to be the grid minimum if plane=True.
    # Notes:
    # 1. It's the minimum of the grid, not a subset of the grid defined by 'region'.
    # 2. The GMT docs says "if -R was used to set zmin/zmax then we use that value if
    #    it is less than the grid minimum value.". We can't add a workaround for this
    #    case since we can't parse zmin/zmax from 'region' if 'region' was set in
    #    previous plotting commands.
    # TODO(GMT>6.6.0): Remove this workaround.
    if Version(__gmt_version__) <= Version("6.6.0") and plane is True:
        plane = grdinfo(grid, per_column=True).split()[4]

    aliasdict = AliasSystem(
        Jz=Alias(zscale, name="zscale"),
        JZ=Alias(zsize, name="zsize"),
        Q=_alias_option_Q(
            surftype=surftype,
            dpi=dpi,
            mesh_fill=mesh_fill,
            monochrome=monochrome,
            nan_transparent=nan_transparent,
        ),
        N=[
            Alias(plane, name="plane"),
            Alias(facade_fill, name="facade_fill", prefix="+g"),
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
