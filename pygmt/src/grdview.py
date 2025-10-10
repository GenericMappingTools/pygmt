"""
grdview - Create 3-D perspective image or surface mesh from a grid.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["grdview"]


@fmt_docstring
@use_alias(
    Jz="zscale",
    JZ="zsize",
    B="frame",
    C="cmap",
    G="drapegrid",
    N="plane",
    Q="surftype",
    Wc="contourpen",
    Wm="meshpen",
    Wf="facadepen",
    I="shading",
    f="coltypes",
    n="interpolation",
    p="perspective",
)
@kwargs_to_strings(p="sequence")
def grdview(
    self,
    grid: PathLike | xr.DataArray,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
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

    {aliases}
       - J = projection
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    {grid}
    region : str or list
        *xmin/xmax/ymin/ymax*\ [**+r**][**+u**\ *unit*].
        Specify the :doc:`region </tutorials/basics/regions>` of interest. When used
        with ``perspective``, optionally append */zmin/zmax* to indicate the range to
        use for the 3-D axes [Default is the region given by the input grid].
    {projection}
    zscale/zsize : float or str
        Set z-axis scaling or z-axis size.
    {frame}
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
    surftype : str
        Specify cover type of the grid. Select one of following settings:

        - **m**: mesh plot [Default].
        - **mx** or **my**: waterfall plots (row or column profiles).
        - **s**: surface plot, and optionally append **m** to have mesh lines drawn on
          top of the surface.
        - **i**: image plot.
        - **c**: Same as **i** but will make nodes with z = NaN transparent.

        For any of these choices, you may force a monochrome image by appending the
        modifier **+m**.
    contourpen : str
        Draw contour lines on top of surface or mesh (not image). Append pen attributes
        used for the contours.
    meshpen : str
        Set the pen attributes used for the mesh. You must also select ``surftype`` of
        **m** or **sm** for meshlines to be drawn.
    facadepen :str
        Set the pen attributes used for the facade. You must also select ``plane`` for
        the facade outline to be drawn.
    shading : str
        Provide the name of a grid file with intensities in the (-1,+1) range, or a
        constant intensity to apply everywhere (affects the ambient light).
        Alternatively, derive an intensity grid from the main input data grid by using
        :func:`pygmt.grdgradient` first; append **+a**\ *azimuth*, **+n**\ *args*, and
        **+m**\ *ambient* to specify azimuth, intensity, and ambient arguments for that
        function, or just give **+d** to select the default arguments [Default is
        "+a-45+nt1+m0"].
    {verbose}
    {panel}
    {coltypes}
    {interpolation}
    {perspective}
    {transparency}

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
    ...     surftype="s",
    ...     # Specify CPT to "geo"
    ...     cmap="geo",
    ... )
    >>> # Show the plot
    >>> fig.show()
    """
    self._activate_figure()

    aliasdict = AliasSystem().add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
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
