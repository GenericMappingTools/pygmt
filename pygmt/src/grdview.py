"""
grdview - Create a three-dimensional plot from a grid.
"""
import contextlib

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
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
    V="verbose",
    X="xshift",
    Y="yshift",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", p="sequence")
def grdview(self, grid, **kwargs):
    """
    Create 3-D perspective image or surface mesh from a grid.

    Reads a 2-D grid file and produces a 3-D perspective plot by drawing a
    mesh, painting a colored/gray-shaded surface made up of polygons, or by
    scanline conversion of these polygons to a raster image. Options
    include draping a data set on top of a surface, plotting of contours on
    top of the surface, and apply artificial illumination based on
    intensities provided in a separate grid file.

    Full option list at :gmt-docs:`grdview.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input relief grid or the grid loaded as a
        DataArray.

    zscale/zsize : float or str
        Set z-axis scaling or z-axis size.

    {B}

    cmap : str
        The name of the color palette table to use.

    drapegrid : str or xarray.DataArray
        The file name or a DataArray of the image grid to be draped on top
        of the relief provided by grid. [Default determines colors from
        grid]. Note that -Jz and -N always refers to the grid. The
        drapegrid only provides the information pertaining to colors, which
        (if drapegrid is a grid) will be looked-up via the CPT (see -C).

    plane : float or str
        ``level[+gfill]``.
        Draws a plane at this z-level. If the optional color is provided
        via the +g modifier, and the projection is not oblique, the frontal
        facade between the plane and the data perimeter is colored.

    surftype : str
        Specifies cover type of the grid.
        Select one of following settings:
        1. 'm' for mesh plot [Default].
        2. 'mx' or 'my' for waterfall plots (row or column profiles).
        3. 's' for surface plot.
        4. 'i' for image plot.
        5. 'c'. Same as 'i' but will make nodes with z = NaN transparent.
        For any of these choices, you may force a monochrome image by
        appending the modifier +m.

    contourpen : str
        Draw contour lines on top of surface or mesh (not image). Append
        pen attributes used for the contours.
    meshpen : str
        Sets the pen attributes used for the mesh. You must also select -Qm
        or -Qsm for meshlines to be drawn.
    facadepen :str
        Sets the pen attributes used for the facade. You must also select
        -N for the facade outline to be drawn.

    shading : str
        Provide the name of a grid file with intensities in the (-1,+1)
        range, or a constant intensity to apply everywhere (affects the
        ambient light). Alternatively, derive an intensity grid from the
        input data grid reliefgrid via a call to ``grdgradient``; append
        ``+aazimuth``, ``+nargs``, and ``+mambient`` to specify azimuth,
        intensity, and ambient arguments for that module, or just give
        ``+d`` to select the default arguments (``+a-45+nt1+m0``).

    {V}
    {XY}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    kind = data_kind(grid, None, None)
    with Session() as lib:
        if kind == "file":
            file_context = dummy_context(grid)
        elif kind == "grid":
            file_context = lib.virtualfile_from_grid(grid)
        else:
            raise GMTInvalidInput(f"Unrecognized data type for grid: {type(grid)}")

        with contextlib.ExitStack() as stack:
            if "G" in kwargs:  # deal with kwargs["G"] if drapegrid is xr.DataArray
                drapegrid = kwargs["G"]
                if data_kind(drapegrid) in ("file", "grid"):
                    if data_kind(drapegrid) == "grid":
                        drape_context = lib.virtualfile_from_grid(drapegrid)
                        kwargs["G"] = stack.enter_context(drape_context)
                else:
                    raise GMTInvalidInput(
                        f"Unrecognized data type for drapegrid: {type(drapegrid)}"
                    )
            fname = stack.enter_context(file_context)
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("grdview", arg_str)
