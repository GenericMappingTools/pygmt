"""
Base class with plot generating commands.
Does not define any special non-GMT methods (savefig, show, etc).
"""
import contextlib
import csv
import os
import numpy as np
import pandas as pd

from .clib import Session
from .exceptions import GMTInvalidInput
from .helpers import (
    build_arg_string,
    dummy_context,
    data_kind,
    fmt_docstring,
    GMTTempFile,
    use_alias,
    kwargs_to_strings,
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
        >>> base._preprocess(resolution='low')
        {'resolution': 'low'}

        """
        return kwargs

    @fmt_docstring
    @use_alias(
        R="region",
        J="projection",
        A="area_thresh",
        B="frame",
        D="resolution",
        I="rivers",
        L="map_scale",
        N="borders",
        W="shorelines",
        G="land",
        S="water",
    )
    @kwargs_to_strings(R="sequence")
    def coast(self, **kwargs):
        """
        Plot continents, shorelines, rivers, and borders on maps

        Plots grayshaded, colored, or textured land-masses [or water-masses] on
        maps and [optionally] draws coastlines, rivers, and political
        boundaries.  Alternatively, it can (1) issue clip paths that will
        contain all land or all water areas, or (2) dump the data to an ASCII
        table. The data files come in 5 different resolutions: (**f**)ull,
        (**h**)igh, (**i**)ntermediate, (**l**)ow, and (**c**)rude. The full
        resolution files amount to more than 55 Mb of data and provide great
        detail; for maps of larger geographical extent it is more economical to
        use one of the other resolutions. If the user selects to paint the
        land-areas and does not specify fill of water-areas then the latter
        will be transparent (i.e., earlier graphics drawn in those areas will
        not be overwritten).  Likewise, if the water-areas are painted and no
        land fill is set then the land-areas will be transparent.

        A map projection must be supplied.

        Full option list at :gmt-docs:`coast.html`

        {aliases}

        Parameters
        ----------
        {J}
        {R}
        A : int, float, or str
            ``'min_area[/min_level/max_level][+ag|i|s|S][+r|l][+ppercent]'``
            Features with an area smaller than min_area in km^2 or of
            hierarchical level that is lower than min_level or higher than
            max_level will not be plotted.
        {B}
        C : str
            Set the shade, color, or pattern for lakes and river-lakes.
        D : str
            Selects the resolution of the data set to use ((f)ull, (h)igh,
            (i)ntermediate, (l)ow, and (c)rude).
        G : str
            Select filling or clipping of “dry” areas.
        I : str
            ``'river[/pen]'``
            Draw rivers. Specify the type of rivers and [optionally] append pen
            attributes.
        L : str
            ``'[g|j|J|n|x]refpoint'``
            Draws a simple map scale centered on the reference point specified.
        N : str
            ``'border[/pen]'``
            Draw political boundaries. Specify the type of boundary and
            [optionally] append pen attributes
        S : str
            Select filling or clipping of “wet” areas.
        {U}
        W : str
            ``'[level/]pen'``
            Draw shorelines [Default is no shorelines]. Append pen attributes.

        """
        kwargs = self._preprocess(**kwargs)
        with Session() as lib:
            lib.call_module("coast", build_arg_string(kwargs))

    @fmt_docstring
    @use_alias(
        R="region",
        J="projection",
        B="frame",
        C="cmap",
        D="position",
        F="box",
        G="truncate",
        W="scale",
    )
    @kwargs_to_strings(R="sequence", G="sequence")
    def colorbar(self, **kwargs):
        """
        Plot a gray or color scale-bar on maps.

        Both horizontal and vertical scales are supported. For CPTs with
        gradational colors (i.e., the lower and upper boundary of an interval
        have different colors) we will interpolate to give a continuous scale.
        Variations in intensity due to shading/illumination may be displayed by
        setting the option -I. Colors may be spaced according to a linear
        scale, all be equal size, or by providing a file with individual tile
        widths.

        Full option list at :gmt-docs:`colorbar.html`

        {aliases}

        Parameters
        ----------
        position (D) : str
            ``[g|j|J|n|x]refpoint[+wlength[/width]][+e[b|f][length]][+h|v]
            [+jjustify][+m[a|c|l|u]][+n[txt]][+odx[/dy]]``. Defines the
            reference point on the map for the color scale using one of four
            coordinate systems: (1) Use -Dg for map (user) coordinates, (2) use
            -Dj or -DJ for setting refpoint via a 2-char justification code
            that refers to the (invisible) map domain rectangle, (3) use -Dn
            for normalized (0-1) coordinates, or (4) use -Dx for plot
            coordinates (inches, cm, etc.). All but -Dx requires both -R and
            -J to be specified. Append +w followed by the length and width of
            the color bar. If width is not specified then it is set to 4% of
            the given length. Give a negative length to reverse the scale bar.
            Append +h to get a horizontal scale [Default is vertical (+v)]. By
            default, the anchor point on the scale is assumed to be the bottom
            left corner (BL), but this can be changed by appending +j followed
            by a 2-char justification code justify.
        box (F) : bool or str
            ``[+cclearances][+gfill][+i[[gap/]pen]][+p[pen]][+r[radius]]
            [+s[[dx/dy/][shade]]]``. If set to True, draws a rectangular
            border around the color scale. Alternatively, specify a different
            pen with +ppen. Add +gfill to fill the scale panel [no fill].
            Append +cclearance where clearance is either gap, xgap/ygap, or
            lgap/rgap/bgap/tgap where these items are uniform, separate in x-
            and y-direction, or individual side spacings between scale and
            border. Append +i to draw a secondary, inner border as well. We use
            a uniform gap between borders of 2p and the MAP_DEFAULTS_PEN unless
            other values are specified. Append +r to draw rounded rectangular
            borders instead, with a 6p corner radius. You can override this
            radius by appending another value. Finally, append +s to draw an
            offset background shaded region. Here, dx/dy indicates the shift
            relative to the foreground frame [4p/-4p] and shade sets the fill
            style to use for shading [gray50].
        truncate (G) : list or str
            ``zlo/zhi`` Truncate the incoming CPT so that the lowest and
            highest z-levels are to zlo and zhi. If one of these equal NaN then
            we leave that end of the CPT alone. The truncation takes place
            before the plotting.
        scale (W) : float
            Multiply all z-values in the CPT by the provided scale. By default
            the CPT is used as is.

        """
        kwargs = self._preprocess(**kwargs)
        with Session() as lib:
            lib.call_module("colorbar", build_arg_string(kwargs))

    @fmt_docstring
    @use_alias(
        A="annotation",
        B="frame",
        C="interval",
        G="label_placement",
        J="projection",
        L="limit",
        Q="cut",
        R="region",
        S="resample",
        U="logo",
        W="pen",
    )
    @kwargs_to_strings(R="sequence", L="sequence", A="sequence_plus")
    def grdcontour(self, grid, **kwargs):
        """
        Convert grids or images to contours and plot them on maps

        Takes a grid file name or an xarray.DataArray object as input.

        Full option list at :gmt-docs:`grdcontour.html`

        {aliases}

        Parameters
        ----------
        grid : str or xarray.DataArray
            The file name of the input grid or the grid loaded as a DataArray.
        C : str or int
            Specify the contour lines to generate.

            - The filename of a `CPT`  file where the color boundaries will
              be used as contour levels.
            - The filename of a 2 (or 3) column file containing the contour
              levels (col 1), (C)ontour or (A)nnotate (col 2), and optional
              angle (col 3)
            - A fixed contour interval ``cont_int`` or a single contour with
              ``+[cont_int]``
        A : str,  int, or list
            Specify or disable annotated contour levels, modifies annotated
            contours specified in ``-C``.

            - Specify a fixed annotation interval ``annot_int`` or a
              single annotation level ``+[annot_int]``
            - Disable all annotation  with  ``'-'``
            - Optional label modifiers can be specified as a single string
              ``'[annot_int]+e'``  or with a list of options
              ``([annot_int], 'e', 'f10p', 'gred')``.
        L : str or list of 2 ints
            Do no draw contours below `low` or above `high`, specify as string
            ``'[low]/[high]'``  or list ``[low,high]``.
        Q : string or int
            Do not draw contours with less than `cut` number of points.
        S : string or int
            Resample smoothing factor.
        {J}
        {R}
        {B}
        {G}
        {W}
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
                lib.call_module("grdcontour", arg_str)

    @fmt_docstring
    @use_alias(R="region", J="projection", W="pen", B="frame", I="shading", C="cmap")
    @kwargs_to_strings(R="sequence")
    def grdimage(self, grid, **kwargs):
        """
        Project grids or images and plot them on maps.

        Takes a grid file name or an xarray.DataArray object as input.

        Full option list at :gmt-docs:`grdimage.html`

        {aliases}

        Parameters
        ----------
        grid : str or xarray.DataArray
            The file name of the input grid or the grid loaded as a DataArray.

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
        p="perspective",
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

        perspective : list or str
            ``'[x|y|z]azim[/elev[/zlevel]][+wlon0/lat0[/z0]][+vx0/y0]'``.
            Select perspective view.

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
                fname = stack.enter_context(file_context)
                if "G" in kwargs:
                    drapegrid = kwargs["G"]
                    if data_kind(drapegrid) in ("file", "grid"):
                        if data_kind(drapegrid) == "grid":
                            drape_context = lib.virtualfile_from_grid(drapegrid)
                            drapefile = stack.enter_context(drape_context)
                            kwargs["G"] = drapefile
                    else:
                        raise GMTInvalidInput(
                            f"Unrecognized data type for drapegrid: {type(drapegrid)}"
                        )
                arg_str = " ".join([fname, build_arg_string(kwargs)])
                lib.call_module("grdview", arg_str)

    @fmt_docstring
    @use_alias(
        R="region",
        J="projection",
        B="frame",
        S="style",
        G="color",
        W="pen",
        i="columns",
        l="label",
        C="cmap",
    )
    @kwargs_to_strings(R="sequence", i="sequence_comma")
    def plot(self, x=None, y=None, data=None, sizes=None, direction=None, **kwargs):
        """
        Plot lines, polygons, and symbols on maps.

        Used to be psxy.

        Takes a matrix, (x,y) pairs, or a file name as input and plots lines,
        polygons, or symbols at those locations on a map.

        Must provide either *data* or *x* and *y*.

        If providing data through *x* and *y*, *color* (G) can be a 1d array
        that will be mapped to a colormap.

        If a symbol is selected and no symbol size given, then psxy will
        interpret the third column of the input data as symbol size. Symbols
        whose size is <= 0 are skipped. If no symbols are specified then the
        symbol code (see *S* below) must be present as last column in the
        input. If *S* is not used, a line connecting the data points will be
        drawn instead. To explicitly close polygons, use *L*. Select a fill
        with *G*. If *G* is set, *W* will control whether the polygon outline
        is drawn or not. If a symbol is selected, *G* and *W* determines the
        fill and outline/no outline, respectively.

        Full option list at :gmt-docs:`plot.html`

        {aliases}

        Parameters
        ----------
        x, y : float or 1d arrays
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
        A : bool or str
            ``'[m|p|x|y]'``
            By default, geographic line segments are drawn as great circle
            arcs. To draw them as straight lines, use *A*.
        {B}
        {CPT}
        D : str
            ``'dx/dy'``: Offset the plot symbol or line locations by the given
            amounts dx/dy.
        E : bool or str
            ``'[x|y|X|Y][+a][+cl|f][+n][+wcap][+ppen]'``.
            Draw symmetrical error bars.
        {G}
        S : str
            Plot symbols (including vectors, pie slices, fronts, decorated or
            quoted lines).
        {W}
        {U}
        l : str
            Add a legend entry for the symbol or line being plotted.
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
        R="region",
        J="projection",
        B="frame",
        S="skip",
        G="label_placement",
        W="pen",
        L="triangular_mesh_pen",
        i="columns",
        C="levels",
    )
    @kwargs_to_strings(R="sequence", i="sequence_comma")
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
        x, y, z : 1d arrays
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
        C : Contour file or level(s)
        D : Dump contour coordinates
        E : Network information
        G : Placement of labels
        I : Color the triangles using CPT
        L : Pen to draw the underlying triangulation (default none)
        N : Do not clip contours
        Q : Minimum contour length
            ``'[p|t]'``
        S : Skip input points outside region
            ``'[p|t]'``
        {W}
        X : Origin shift x
        Y : Origin shift y


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
    @use_alias(R="region", J="projection", B="frame")
    @kwargs_to_strings(R="sequence")
    def basemap(self, **kwargs):
        """
        Produce a basemap for the figure.

        Several map projections are available, and the user may specify
        separate tick-mark intervals for boundary annotation, ticking, and
        [optionally] gridlines. A simple map scale or directional rose may also
        be plotted.

        At least one of the options *B*, *L*, or *T* must be specified.

        Full option list at :gmt-docs:`basemap.html`

        {aliases}

        Parameters
        ----------
        {J}
        {R}
        {B}
        L : str
            ``'[g|j|J|n|x]refpoint'``
            Draws a simple map scale centered on the reference point specified.
        Td : str
            Draws a map directional rose on the map at the location defined by
            the reference and anchor points.
        Tm : str
            Draws a map magnetic rose on the map at the location defined by the
            reference and anchor points
        {U}

        """
        kwargs = self._preprocess(**kwargs)
        if not ("B" in kwargs or "L" in kwargs or "T" in kwargs):
            raise GMTInvalidInput("At least one of B, L, or T must be specified.")
        with Session() as lib:
            lib.call_module("basemap", build_arg_string(kwargs))

    @fmt_docstring
    @use_alias(R="region", J="projection")
    @kwargs_to_strings(R="sequence")
    def logo(self, **kwargs):
        """
        Place the GMT graphics logo on a map.

        By default, the GMT logo is 2 inches wide and 1 inch high and
        will be positioned relative to the current plot origin.
        Use various options to change this and to place a transparent or
        opaque rectangular map panel behind the GMT logo.

        Full option list at :gmt-docs:`logo.html`

        {aliases}

        Parameters
        ----------
        {J}
        {R}
        D : str
            ``'[g|j|J|n|x]refpoint+wwidth[+jjustify][+odx[/dy]]'``.
            Sets reference point on the map for the image.
        F : bool or str
            Without further options, draws a rectangular border around the
            GMT logo.
        {U}

        """
        kwargs = self._preprocess(**kwargs)
        if "D" not in kwargs:
            raise GMTInvalidInput("Option D must be specified.")
        with Session() as lib:
            lib.call_module("logo", build_arg_string(kwargs))

    @fmt_docstring
    @use_alias(R="region", J="projection")
    @kwargs_to_strings(R="sequence")
    def image(self, imagefile, **kwargs):
        """
        Place images or EPS files on maps.

        Reads an Encapsulated PostScript file or a raster image file and plots
        it on a map.

        Full option list at :gmt-docs:`image.html`

        {aliases}

        Parameters
        ----------
        {J}
        {R}
        D: str
            ``'[g|j|J|n|x]refpoint+rdpi+w[-]width[/height][+jjustify]
            [+nnx[/ny]][+odx[/dy]]'`` Sets reference point on the map for the
            image.
        F : bool or str
            ``'[+cclearances][+gfill][+i[[gap/]pen]][+p[pen]][+r[radius]]
            [+s[[dx/dy/][shade]]]'`` Without further options, draws a
            rectangular border around the image using **MAP_FRAME_PEN**.
        M : bool
            Convert color image to monochrome grayshades using the (television)
            YIQ-transformation.
        """
        kwargs = self._preprocess(**kwargs)
        with Session() as lib:
            arg_str = " ".join([imagefile, build_arg_string(kwargs)])
            lib.call_module("image", arg_str)

    @fmt_docstring
    @use_alias(R="region", J="projection", D="position", F="box")
    @kwargs_to_strings(R="sequence")
    def legend(self, spec=None, position="JTR+jTR+o0.2c", box="+gwhite+p1p", **kwargs):
        """
        Plot legends on maps.

        Makes legends that can be overlaid on maps. Reads specific
        legend-related information from an input file, or automatically creates
        legend entries from plotted symbols that have labels. Unless otherwise
        noted, annotations will be made using the primary annotation font and
        size in effect (i.e., FONT_ANNOT_PRIMARY).

        Full option list at :gmt-docs:`legend.html`

        {aliases}

        Parameters
        ----------
        spec : None or str
            Either None (default) for using the automatically generated legend
            specification file, or a filename pointing to the legend
            specification file.
        {J}
        {R}
        position (D) : str
            ``'[g|j|J|n|x]refpoint+wwidth[/height][+jjustify][+lspacing]
            [+odx[/dy]]'`` Defines the reference point on the map for the
            legend. By default, uses 'JTR+jTR+o0.2c' which places the legend at
            the top-right corner inside the map frame, with a 0.2 cm offset.
        box (F) : bool or str
            ``'[+cclearances][+gfill][+i[[gap/]pen]][+p[pen]][+r[radius]]
            [+s[[dx/dy/][shade]]]'`` Without further options, draws a
            rectangular border around the legend using **MAP_FRAME_PEN**. By
            default, uses '+gwhite+p1p' which draws a box around the legend
            using a 1 point black pen and adds a white background.
        """
        kwargs = self._preprocess(**kwargs)

        if "D" not in kwargs:
            kwargs["D"] = position

            if "F" not in kwargs:
                kwargs["F"] = box

        with Session() as lib:
            if spec is None:
                specfile = ""
            elif data_kind(spec) == "file":
                specfile = spec
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(spec)))
            arg_str = " ".join([specfile, build_arg_string(kwargs)])
            lib.call_module("legend", arg_str)

    @fmt_docstring
    @use_alias(R="region", J="projection", B="frame")
    @kwargs_to_strings(
        R="sequence",
        textfiles="sequence_space",
        angle="sequence_comma",
        font="sequence_comma",
        justify="sequence_comma",
    )
    def text(
        self,
        textfiles=None,
        x=None,
        y=None,
        text=None,
        angle=None,
        font=None,
        justify=None,
        **kwargs,
    ):
        """
        Plot or typeset text on maps

        Used to be pstext.

        Takes in textfile(s) or (x,y,text) triples as input.

        Must provide at least *textfiles* or *x*, *y*, and *text*.

        Full option list at :gmt-docs:`text.html`

        {aliases}

        Parameters
        ----------
        textfiles : str or list
            A text data file name, or a list of filenames containing 1 or more
            records with (x, y[, font, angle, justify], text).
        x, y : float or 1d arrays
            The x and y coordinates, or an array of x and y coordinates to plot
            the text
        text : str or 1d array
            The text string, or an array of strings to plot on the figure
        angle: int/float or bool
            Set the angle measured in degrees counter-clockwise from
            horizontal. E.g. 30 sets the text at 30 degrees. If no angle is
            given then the input textfile(s) must have this as a column.
        font : str or bool
            Set the font specification with format "size,font,color" where size
            is text size in points, font is the font to use, and color sets the
            font color. E.g. "12p,Helvetica-Bold,red" selects a 12p red
            Helvetica-Bold font. If no font info is given then the input
            textfile(s) must have this information in one of its columns.
        justify: str or bool
            Set the alignment which refers to the part of the text string that
            will be mapped onto the (x,y) point. Choose a 2 character
            combination of L, C, R (for left, center, or right) and T, M, B for
            top, middle, or bottom. E.g., BL for lower left. If no
            justification is given then the input textfile(s) must have this as
            a column.
        {J}
        {R}
        """
        kwargs = self._preprocess(**kwargs)

        kind = data_kind(textfiles, x, y, text)
        if kind == "vectors" and text is None:
            raise GMTInvalidInput("Must provide text with x and y.")
        if kind == "file":
            for textfile in textfiles.split(" "):  # ensure that textfile(s) exist
                if not os.path.exists(textfile):
                    raise GMTInvalidInput(f"Cannot find the file: {textfile}")

        if angle is not None or font is not None or justify is not None:
            if "F" not in kwargs.keys():
                kwargs.update({"F": ""})
            if angle is not None and isinstance(angle, (int, float)):
                kwargs["F"] += f"+a{str(angle)}"
            if font is not None and isinstance(font, str):
                kwargs["F"] += f"+f{font}"
            if justify is not None and isinstance(justify, str):
                kwargs["F"] += f"+j{justify}"

        with GMTTempFile(suffix=".txt") as tmpfile:
            with Session() as lib:
                if kind == "file":
                    fname = textfiles
                elif kind == "vectors":
                    pd.DataFrame.from_dict(
                        {
                            "x": np.atleast_1d(x),
                            "y": np.atleast_1d(y),
                            "text": np.atleast_1d(text),
                        }
                    ).to_csv(
                        tmpfile.name,
                        sep="\t",
                        header=False,
                        index=False,
                        quoting=csv.QUOTE_NONE,
                    )
                    fname = tmpfile.name

                arg_str = " ".join([fname, build_arg_string(kwargs)])
                lib.call_module("text", arg_str)
