"""
Base class with plot generating commands.

Does not define any special non-GMT methods (savefig, show, etc).
"""
import contextlib

import numpy as np
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    args_in_kwargs,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


class BasePlotting:
    """
    Base class for Figure and Subplot.

    Defines the plot generating methods and a hook for subclasses to insert
    special arguments (the _preprocess method).
    """

    def _preprocess(self, **kwargs):  # pylint: disable=no-self-use
        """
        Make any changes to kwargs or required actions before plotting.

        This method is run before all plotting commands and can be used to
        insert special arguments into the kwargs or make any actions that are
        required before ``call_module``.

        For example, the :class:`pygmt.Figure` needs this to tell the GMT
        modules to plot to a specific figure.

        This is a dummy method that does nothing.

        Returns
        -------
        kwargs : dict
            The same input kwargs dictionary.

        Examples
        --------

        >>> base = BasePlotting()
        >>> base._preprocess(resolution="low")
        {'resolution': 'low'}
        """
        return kwargs

    @fmt_docstring
    @use_alias(
        A="img_out",
        B="frame",
        C="cmap",
        D="img_in",
        E="dpi",
        G="bit_color",
        I="shading",
        J="projection",
        M="monochrome",
        N="no_clip",
        Q="nan_transparent",
        R="region",
        U="timestamp",
        V="verbose",
        X="xshift",
        Y="yshift",
        n="interpolation",
        p="perspective",
        t="transparency",
        x="cores",
    )
    @kwargs_to_strings(R="sequence", p="sequence")
    def grdimage(self, grid, **kwargs):
        """
        Project and plot grids or images.

        Reads a 2-D grid file and produces a gray-shaded (or colored) map by
        building a rectangular image and assigning pixels a gray-shade (or
        color) based on the z-value and the CPT file. Optionally, illumination
        may be added by providing a file with intensities in the (-1,+1) range
        or instructions to derive intensities from the input data grid. Values
        outside this range will be clipped. Such intensity files can be created
        from the grid using `grdgradient` and, optionally, modified by
        `grdmath` or `grdhisteq`. If GMT is built with GDAL support, *grid* can
        be an image file (geo-referenced or not). In this case the image can
        optionally be illuminated with the file provided via the *shading*
        option. Here, if image has no coordinates then those of the intensity
        file will be used.

        When using map projections, the grid is first resampled on a new
        rectangular grid with the same dimensions. Higher resolution images can
        be obtained by using the *dpi* option. To obtain the resampled value
        (and hence shade or color) of each map pixel, its location is inversely
        projected back onto the input grid after which a value is interpolated
        between the surrounding input grid values. By default bi-cubic
        interpolation is used. Aliasing is avoided by also forward projecting
        the input grid nodes. If two or more nodes are projected onto the same
        pixel, their average will dominate in the calculation of the pixel
        value. Interpolation and aliasing is controlled with the
        *interpolation* option.

        The *region* option can be used to select a map region larger or
        smaller than that implied by the extent of the grid.

        Full option list at :gmt-docs:`grdimage.html`

        {aliases}

        Parameters
        ----------
        grid : str or xarray.DataArray
            The file name or a DataArray containing the input 2-D gridded data
            set or image to be plotted (See GRID FILE FORMATS at
            :gmt-docs:`grdimage.html#grid-file-formats`).
        img_out : str
            ``out_img[=driver]``.
            Save an image in a raster format instead of PostScript. Use
            extension .ppm for a Portable Pixel Map format which is the only
            raster format GMT can natively write. For GMT installations
            configured with GDAL support there are more choices: Append
            *out_img* to select the image file name and extension. If the
            extension is one of .bmp, .gif, .jpg, .png, or .tif then no driver
            information is required. For other output formats you must append
            the required GDAL driver. The *driver* is the driver code name used
            by GDAL; see your GDAL installation's documentation for available
            drivers. Append a **+c**\\ *options* string where options is a list
            of one or more concatenated number of GDAL **-co** options. For
            example, to write a GeoPDF with the TerraGo format use
            ``=PDF+cGEO_ENCODING=OGC_BP``. Notes: (1) If a tiff file (.tif) is
            selected then we will write a GeoTiff image if the GMT projection
            syntax translates into a PROJ syntax, otherwise a plain tiff file
            is produced. (2) Any vector elements will be lost.
        {B}
        {CPT}
        img_in : str
            ``[r]``
            GMT will automatically detect standard image files (Geotiff, TIFF,
            JPG, PNG, GIF, etc.) and will read those via GDAL. For very obscure
            image formats you may need to explicitly set *img_in*, which
            specifies that the grid is in fact an image file to be read via
            GDAL. Append **r** to assign the region specified by *region*
            to the image. For example, if you have used ``region='d'`` then the
            image will be assigned a global domain. This mode allows you to
            project a raw image (an image without referencing coordinates).
        dpi : int
            ``[i|dpi]``.
            Sets the resolution of the projected grid that will be created if a
            map projection other than Linear or Mercator was selected [100]. By
            default, the projected grid will be of the same size (rows and
            columns) as the input file. Specify **i** to use the PostScript
            image operator to interpolate the image at the device resolution.
        bit_color : str
            ``color[+b|f]``.
            This option only applies when a resulting 1-bit image otherwise
            would consist of only two colors: black (0) and white (255). If so,
            this option will instead use the image as a transparent mask and
            paint the mask with the given color. Append **+b** to paint the
            background pixels (1) or **+f** for the foreground pixels
            [Default].
        shading : str
            ``[intensfile|intensity|modifiers]``.
            Give the name of a grid file with intensities in the (-1,+1) range,
            or a constant intensity to apply everywhere (affects the ambient
            light). Alternatively, derive an intensity grid from the input data
            grid via a call to `grdgradient`; append **+a**\\ *azimuth*,
            **+n**\\ *args*, and **+m**\\ *ambient* to specify azimuth,
            intensity, and ambient arguments for that module, or just give
            **+d** to select the default arguments (``+a-45+nt1+m0``). If you
            want a more specific intensity scenario then run `grdgradient`
            separately first. If we should derive intensities from another file
            than grid, specify the file with suitable modifiers [Default is no
            illumination].
        {J}
        monochrome : bool
            Force conversion to monochrome image using the (television) YIQ
            transformation. Cannot be used with *nan_transparent*.
        no_clip : bool
            Do not clip the image at the map boundary (only relevant for
            non-rectangular maps).
        nan_transparent : bool
            Make grid nodes with z = NaN transparent, using the color-masking
            feature in PostScript Level 3 (the PS device must support PS Level
            3).
        {R}
        {V}
        {XY}
        {n}
        {p}
        {t}
        {x}
        """
        kwargs = self._preprocess(**kwargs)
        kind = data_kind(grid, None, None)
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(grid)
            elif kind == "grid":
                file_context = lib.virtualfile_from_grid(grid)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(grid)))
            with file_context as fname:
                arg_str = " ".join([fname, build_arg_string(kwargs)])
                lib.call_module("grdimage", arg_str)

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
        kwargs = self._preprocess(**kwargs)
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

    from pygmt.src import basemap  # pylint: disable=import-outside-toplevel
    from pygmt.src import coast  # pylint: disable=import-outside-toplevel
    from pygmt.src import colorbar  # pylint: disable=import-outside-toplevel
    from pygmt.src import contour  # pylint: disable=import-outside-toplevel
    from pygmt.src import grdcontour  # pylint: disable=import-outside-toplevel
    from pygmt.src import image  # pylint: disable=import-outside-toplevel
    from pygmt.src import legend  # pylint: disable=import-outside-toplevel
    from pygmt.src import logo  # pylint: disable=import-outside-toplevel
    from pygmt.src import meca  # pylint: disable=import-outside-toplevel
    from pygmt.src import plot  # pylint: disable=import-outside-toplevel
    from pygmt.src import plot3d  # pylint: disable=import-outside-toplevel
    from pygmt.src import text  # pylint: disable=import-outside-toplevel
