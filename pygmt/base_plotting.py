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

    @fmt_docstring
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
        i="columns",
        l="label",
        p="perspective",
        t="transparency",
    )
    @kwargs_to_strings(R="sequence", i="sequence_comma", p="sequence")
    def plot(self, x=None, y=None, data=None, sizes=None, direction=None, **kwargs):
        """
        Plot lines, polygons, and symbols in 2-D.

        Takes a matrix, (x,y) pairs, or a file name as input and plots lines,
        polygons, or symbols at those locations on a map.

        Must provide either *data* or *x* and *y*.

        If providing data through *x* and *y*, *color* can be a 1d array that
        will be mapped to a colormap.

        If a symbol is selected and no symbol size given, then plot will
        interpret the third column of the input data as symbol size. Symbols
        whose size is <= 0 are skipped. If no symbols are specified then the
        symbol code (see *style* below) must be present as last column in the
        input. If *style* is not used, a line connecting the data points will
        be drawn instead. To explicitly close polygons, use *close*. Select a
        fill with *color*. If *color* is set, *pen* will control whether the
        polygon outline is drawn or not. If a symbol is selected, *color* and
        *pen* determines the fill and outline/no outline, respectively.

        Full option list at :gmt-docs:`plot.html`

        {aliases}

        Parameters
        ----------
        x/y : float or 1d arrays
            The x and y coordinates, or arrays of x and y coordinates of the
            data points
        data : str or 2d array
            Either a data file name or a 2d numpy array with the tabular data.
            Use option *columns* (i) to choose which columns are x, y, color,
            and size, respectively.
        sizes : 1d array
            The sizes of the data points in units specified in *style* (S).
            Only valid if using *x* and *y*.
        direction : list of two 1d arrays
            If plotting vectors (using ``style='V'`` or ``style='v'``), then
            should be a list of two 1d arrays with the vector directions. These
            can be angle and length, azimuth and length, or x and y components,
            depending on the style options chosen.
        {J}
        {R}
        straight_line : bool or str
            ``[m|p|x|y]``.
            By default, geographic line segments are drawn as great circle
            arcs. To draw them as straight lines, use *straight_line*.
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
            ``dx/dy``.
            Offset the plot symbol or line locations by the given amounts
            *dx/dy* [Default is no offset]. If *dy* is not given it is set
            equal to *dx*.
        error_bar : bool or str
            ``[x|y|X|Y][+a][+cl|f][+n][+wcap][+ppen]``.
            Draw symmetrical error bars. Full documentation is at
            :gmt-docs:`plot.html#e`.
        connection : str
            ``[c|n|r][a|f|s|r|refpoint]``.
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

            Instead of the codes **a**|**f**|**s**|**r** you may append the
            coordinates of a *refpoint* which will serve as a fixed external
            reference point for all groups.
        {G}
        intensity : float or bool
            Provide an *intens* value (nominally in the -1 to +1 range) to
            modulate the fill color by simulating illumination [None]. If
            using ``intensity=True``, we will instead read *intens* from the
            first data column after the symbol parameters (if given).
        close : str
            ``[+b|d|D][+xl|r|x0][+yl|r|y0][+ppen]``.
            Force closed polygons. Full documentation is at
            :gmt-docs:`plot.html#l`.
        no_clip : bool or str
            ``'[c|r]'``.
            Do NOT clip symbols that fall outside map border [Default plots
            points whose coordinates are strictly inside the map border only].
            The option does not apply to lines and polygons which are always
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
            ``value|file``.
            Instead of specifying a symbol or polygon fill and outline color
            via **color** and **pen**, give both a *value* via **zvalue** and a
            color lookup table via **cmap**.  Alternatively, give the name of a
            *file* with one z-value (read from the last column) for each
            polygon in the input data. To apply it to the fill color, use
            ``color='+z'``. To apply it to the pen color, append **+z** to
            **pen**.
        columns : str or 1d array
            Choose which columns are x, y, color, and size, respectively if
            input is provided via *data*. E.g. ``columns = [0, 1]`` or
            ``columns = '0,1'`` if the *x* values are stored in the first
            column and *y* values in the second one. Note: zero-based
            indexing is used.
        label : str
            Add a legend entry for the symbol or line being plotted.

        {p}
        {t}
            *transparency* can also be a 1d array to set varying transparency
            for symbols.
        """
        kwargs = self._preprocess(**kwargs)

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
        if sizes is not None:
            if kind != "vectors":
                raise GMTInvalidInput(
                    "Can't use arrays for sizes if data is matrix or file."
                )
            extra_arrays.append(sizes)

        if "t" in kwargs and is_nonstr_iter(kwargs["t"]):
            extra_arrays.append(kwargs["t"])
            kwargs["t"] = ""

        with Session() as lib:
            # Choose how data will be passed in to the module
            if kind == "file":
                file_context = dummy_context(data)
            elif kind == "matrix":
                file_context = lib.virtualfile_from_matrix(data)
            elif kind == "vectors":
                file_context = lib.virtualfile_from_vectors(
                    np.atleast_1d(x), np.atleast_1d(y), *extra_arrays
                )

            with file_context as fname:
                arg_str = " ".join([fname, build_arg_string(kwargs)])
                lib.call_module("plot", arg_str)

    @fmt_docstring
    @use_alias(
        A="straight_line",
        B="frame",
        C="cmap",
        D="offset",
        G="color",
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
        X="xshift",
        Y="yshift",
        Z="zvalue",
        i="columns",
        l="label",
        p="perspective",
        t="transparency",
    )
    @kwargs_to_strings(R="sequence", i="sequence_comma", p="sequence")
    def plot3d(
        self, x=None, y=None, z=None, data=None, sizes=None, direction=None, **kwargs
    ):
        """
        Plot lines, polygons, and symbols in 3-D.

        Takes a matrix, (x,y,z) triplets, or a file name as input and plots
        lines, polygons, or symbols at those locations in 3-D.

        Must provide either *data* or *x*, *y* and *z*.

        If providing data through *x*, *y* and *z*, *color* can be a 1d array
        that will be mapped to a colormap.

        If a symbol is selected and no symbol size given, then plot3d will
        interpret the fourth column of the input data as symbol size. Symbols
        whose size is <= 0 are skipped. If no symbols are specified then the
        symbol code (see *style* below) must be present as last column in the
        input. If *style* is not used, a line connecting the data points will
        be drawn instead. To explicitly close polygons, use *close*. Select a
        fill with *color*. If *color* is set, *pen* will control whether the
        polygon outline is drawn or not. If a symbol is selected, *color* and
        *pen* determines the fill and outline/no outline, respectively.

        Full option list at :gmt-docs:`plot3d.html`

        {aliases}

        Parameters
        ----------
        x/y/z : float or 1d arrays
            The x, y, and z coordinates, or arrays of x, y and z coordinates of
            the data points
        data : str or 2d array
            Either a data file name or a 2d numpy array with the tabular data.
            Use option *columns* (i) to choose which columns are x, y, z,
            color, and size, respectively.
        sizes : 1d array
            The sizes of the data points in units specified in *style* (S).
            Only valid if using *x*, *y* and *z*.
        direction : list of two 1d arrays
            If plotting vectors (using ``style='V'`` or ``style='v'``), then
            should be a list of two 1d arrays with the vector directions. These
            can be angle and length, azimuth and length, or x and y components,
            depending on the style options chosen.
        {J}
        zscale/zsize : float or str
            Set z-axis scaling or z-axis size.
        {R}
        straight_line : bool or str
            ``[m|p|x|y]``.
            By default, geographic line segments are drawn as great circle
            arcs. To draw them as straight lines, use *straight_line*.
            Alternatively, add **m** to draw the line by first following a
            meridian, then a parallel. Or append **p** to start following a
            parallel, then a meridian. (This can be practical to draw a line
            along parallels, for example). For Cartesian data, points are
            simply connected, unless you append **x** or **y** to draw
            stair-case curves that whose first move is along *x* or *y*,
            respectively. **Note**: The **straight_line** option requires
            constant *z*-coordinates.
        {B}
        {CPT}
        offset : str
            ``dx/dy[/dz]``.
            Offset the plot symbol or line locations by the given amounts
            *dx/dy*[*dz*] [Default is no offset].
        {G}
        intensity : float or bool
            Provide an *intens* value (nominally in the -1 to +1 range) to
            modulate the fill color by simulating illumination [None]. If
            using ``intensity=True``, we will instead read *intens* from the
            first data column after the symbol parameters (if given).
        close : str
            ``[+b|d|D][+xl|r|x0][+yl|r|y0][+ppen]``.
            Force closed polygons. Full documentation is at
            :gmt-docs:`plot3d.html#l`.
        no_clip : bool or str
            ``[c|r]``.
            Do NOT clip symbols that fall outside map border [Default plots
            points whose coordinates are strictly inside the map border only].
            The option does not apply to lines and polygons which are always
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
        {U}
        {V}
        {W}
        {XY}
        zvalue : str
            ``value|file``.
            Instead of specifying a symbol or polygon fill and outline color
            via **color** and **pen**, give both a *value* via **zvalue** and a
            color lookup table via **cmap**.  Alternatively, give the name of a
            *file* with one z-value (read from the last column) for each
            polygon in the input data. To apply it to the fill color, use
            ``color='+z'``. To apply it to the pen color, append **+z** to
            **pen**.
        label : str
            Add a legend entry for the symbol or line being plotted.
        {p}
        {t}
            *transparency* can also be a 1d array to set varying transparency
            for symbols.
        """
        kwargs = self._preprocess(**kwargs)

        kind = data_kind(data, x, y, z)

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
        if sizes is not None:
            if kind != "vectors":
                raise GMTInvalidInput(
                    "Can't use arrays for sizes if data is matrix or file."
                )
            extra_arrays.append(sizes)

        if "t" in kwargs and is_nonstr_iter(kwargs["t"]):
            extra_arrays.append(kwargs["t"])
            kwargs["t"] = ""

        with Session() as lib:
            # Choose how data will be passed in to the module
            if kind == "file":
                file_context = dummy_context(data)
            elif kind == "matrix":
                file_context = lib.virtualfile_from_matrix(data)
            elif kind == "vectors":
                file_context = lib.virtualfile_from_vectors(
                    np.atleast_1d(x), np.atleast_1d(y), np.atleast_1d(z), *extra_arrays
                )

            with file_context as fname:
                arg_str = " ".join([fname, build_arg_string(kwargs)])
                lib.call_module("plot3d", arg_str)

    @fmt_docstring
    @use_alias(
        R="region",
        J="projection",
        B="frame",
        S="skip",
        G="label_placement",
        W="pen",
        L="triangular_mesh_pen",
        N="no_clip",
        i="columns",
        l="label",
        C="levels",
        V="verbose",
        X="xshift",
        Y="yshift",
        p="perspective",
        t="transparency",
    )
    @kwargs_to_strings(R="sequence", i="sequence_comma", p="sequence")
    def contour(self, x=None, y=None, z=None, data=None, **kwargs):
        """
        Contour table data by direct triangulation.

        Takes a matrix, (x,y,z) pairs, or a file name as input and plots lines,
        polygons, or symbols at those locations on a map.

        Must provide either *data* or *x*, *y*, and *z*.

        [TODO: Insert more documentation]

        Full option list at :gmt-docs:`contour.html`

        {aliases}

        Parameters
        ----------
        x/y/z : 1d arrays
            Arrays of x and y coordinates and values z of the data points.
        data : str or 2d array
            Either a data file name or a 2d numpy array with the tabular data.
        {J}
        {R}
        A : bool or str
            ``'[m|p|x|y]'``
            By default, geographic line segments are drawn as great circle
            arcs. To draw them as straight lines, use *A*.
        {B}
        levels : str
            Contour file or level(s)
        D : str
            Dump contour coordinates
        E : str
            Network information
        label_placement : str
            Placement of labels
        I : bool
            Color the triangles using CPT
        triangular_mesh_pen : str
            Pen to draw the underlying triangulation (default none)
        no_clip : bool
            Do NOT clip contours or image at the boundaries [Default will clip
            to fit inside region].
        Q : float or str
            Do not draw contours with less than cut number of points.
            ``'[cut[unit]][+z]'``
        skip : bool or str
            Skip input points outside region ``'[p|t]'``
        {W}
        label : str
            Add a legend entry for the contour being plotted. Normally, the
            annotated contour is selected for the legend. You can select the
            regular contour instead, or both of them, by considering the label
            to be of the format [*annotcontlabel*][/*contlabel*]. If either
            label contains a slash (/) character then use ``|`` as the
            separator for the two labels instead.
        {V}
        {XY}
        {p}
        {t}
        """
        kwargs = self._preprocess(**kwargs)

        kind = data_kind(data, x, y, z)
        if kind == "vectors" and z is None:
            raise GMTInvalidInput("Must provided both x, y, and z.")

        with Session() as lib:
            # Choose how data will be passed in to the module
            if kind == "file":
                file_context = dummy_context(data)
            elif kind == "matrix":
                file_context = lib.virtualfile_from_matrix(data)
            elif kind == "vectors":
                file_context = lib.virtualfile_from_vectors(x, y, z)

            with file_context as fname:
                arg_str = " ".join([fname, build_arg_string(kwargs)])
                lib.call_module("contour", arg_str)

    @fmt_docstring
    @use_alias(
        R="region",
        J="projection",
        Jz="zscale",
        JZ="zsize",
        B="frame",
        L="map_scale",
        Td="rose",
        Tm="compass",
        U="timestamp",
        V="verbose",
        X="xshift",
        Y="yshift",
        p="perspective",
        t="transparency",
    )
    @kwargs_to_strings(R="sequence", p="sequence")
    def basemap(self, **kwargs):
        """
        Plot base maps and frames for the figure.

        Creates a basic or fancy basemap with axes, fill, and titles. Several
        map projections are available, and the user may specify separate
        tick-mark intervals for boundary annotation, ticking, and [optionally]
        gridlines. A simple map scale or directional rose may also be plotted.

        At least one of the options *frame*, *map_scale*, *rose* or *compass*
        must be specified.

        Full option list at :gmt-docs:`basemap.html`

        {aliases}

        Parameters
        ----------
        {J}
        zscale/zsize : float or str
            Set z-axis scaling or z-axis size.
        {R}
        {B}
        map_scale : str
            ``'[g|j|J|n|x]refpoint'``
            Draws a simple map scale centered on the reference point specified.
        rose : str
            Draws a map directional rose on the map at the location defined by
            the reference and anchor points.
        compass : str
            Draws a map magnetic rose on the map at the location defined by the
            reference and anchor points
        {U}
        {V}
        {XY}
        {p}
        {t}
        """
        kwargs = self._preprocess(**kwargs)
        if not args_in_kwargs(args=["B", "L", "Td", "Tm"], kwargs=kwargs):
            raise GMTInvalidInput(
                "At least one of frame, map_scale, compass, or rose must be specified."
            )
        with Session() as lib:
            lib.call_module("basemap", build_arg_string(kwargs))

    from pygmt.src import coast  # pylint: disable=import-outside-toplevel
    from pygmt.src import colorbar  # pylint: disable=import-outside-toplevel
    from pygmt.src import grdcontour  # pylint: disable=import-outside-toplevel
    from pygmt.src import image  # pylint: disable=import-outside-toplevel
    from pygmt.src import legend  # pylint: disable=import-outside-toplevel
    from pygmt.src import logo  # pylint: disable=import-outside-toplevel
    from pygmt.src import meca  # pylint: disable=import-outside-toplevel
    from pygmt.src import text  # pylint: disable=import-outside-toplevel
