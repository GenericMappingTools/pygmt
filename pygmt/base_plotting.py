"""
Base class with plot generating commands.
Does not define any special non-GMT methods (savefig, show, etc).
"""
from .clib import Session
from .exceptions import GMTInvalidInput
from .helpers import (
    build_arg_string,
    dummy_context,
    data_kind,
    fmt_docstring,
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

        For example, the :class:`pygmt.Figure` needs this to tell the GMT modules
        to plot to a specific figure.

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
            - Optional label modifers can be specifed as a single string
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
        B="frame",
        S="style",
        G="color",
        W="pen",
        i="columns",
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
        x, y : 1d arrays
            Arrays of x and y coordinates of the data points.
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
                file_context = lib.virtualfile_from_vectors(x, y, *extra_arrays)

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

        Reads an Encapsulated PostScript file or a raster image file and plots it on a map.

        Full option list at :gmt-docs:`image.html`

        {aliases}

        Parameters
        ----------
        {J}
        {R}
        D: str
            ``'[g|j|J|n|x]refpoint+rdpi+w[-]width[/height][+jjustify][+nnx[/ny]][+odx[/dy]]'``
            Sets reference point on the map for the image.
        F : bool or str
            ``'[+cclearances][+gfill][+i[[gap/]pen]][+p[pen]][+r[radius]][+s[[dx/dy/][shade]]]'``
            Without further options, draws a rectangular border around the
            image using **MAP_FRAME_PEN**.
        M : bool
            Convert color image to monochrome grayshades using the (television)
            YIQ-transformation.
        """
        kwargs = self._preprocess(**kwargs)
        with Session() as lib:
            arg_str = " ".join([imagefile, build_arg_string(kwargs)])
            lib.call_module("image", arg_str)
