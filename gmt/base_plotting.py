"""
Base class with plot generating commands.
Does not define any special non-GMT methods (savefig, show, etc).
"""
from .clib import call_module, APISession
from .utils import build_arg_string
from .decorators import fmt_docstring, use_alias, kwargs_to_strings


class BasePlotting():
    """
    Base class for Figure and Subplot.

    Defines the plot generating methods and a hook for subclasses to insert
    special arguments (the _preprocess method).
    """

    def _preprocess(self, **kwargs):  # pylint: disable=no-self-use
        """
        Make changes to kwargs before passing them to ``call_module``.

        This method is run before all plotting commands and can be used to
        insert special arguments into the kwargs or make any actions that are
        required before ``call_module``.

        For example, the :class:`gmt.Figure` needs this to tell the GMT modules
        to plot to a specific figure.

        Returns
        -------
        kwargs : dict
            A modified version of the input kwargs.

        """
        return kwargs

    @fmt_docstring
    @use_alias(R='region', J='projection', A='area_thresh', B='frame',
               D='resolution', P='portrait', I='rivers', N='borders',
               W='shorelines', G='land', S='water')
    @kwargs_to_strings(R='sequence')
    def pscoast(self, **kwargs):
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

        {gmt_module_docs}

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
        with APISession() as session:
            call_module(session, 'pscoast', build_arg_string(kwargs))

    @fmt_docstring
    @use_alias(R='region', J='projection', B='frame', P='portrait', S='style',
               G='color', W='pen', i='columns')
    @kwargs_to_strings(R='sequence', i='sequence_comma')
    def psxy(self, data, **kwargs):
        """
        Plot lines, polygons, and symbols on maps.

        Takes (x,y) pairs as inputs or reads them from a file and plots lines,
        polygons, or symbols at those locations on a map.

        If a symbol is selected and no symbol size given, then psxy will
        interpret the third column of the input data as symbol size. Symbols
        whose size is <= 0 are skipped. If no symbols are specified then the
        symbol code (see *S* below) must be present as last column in the
        input. If *S* is not used, a line connecting the data points will be
        drawn instead. To explicitly close polygons, use *L*. Select a fill
        with *G*. If *G* is set, *W* will control whether the polygon outline
        is drawn or not. If a symbol is selected, *G* and *W* determines the
        fill and outline/no outline, respectively.

        {gmt_module_docs}

        {aliases}

        Parameters
        ----------
        data : str or array
            *Required*. Input data table as an array or a file name.
            **Only accepts file names for now.**
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
        {P}
        S : str
            Plot symbols (including vectors, pie slices, fronts, decorated or
            quoted lines).
        {W}
        {U}


        """
        kwargs = self._preprocess(**kwargs)
        assert isinstance(data, str), 'Only accepts file names for now.'
        arg_str = ' '.join([data, build_arg_string(kwargs)])
        with APISession() as session:
            call_module(session, 'psxy', arg_str)

    @fmt_docstring
    @use_alias(R='region', J='projection', B='frame', P='portrait')
    @kwargs_to_strings(R='sequence')
    def psbasemap(self, **kwargs):
        """
        Produce a basemap for the figure.

        Several map projections are available, and the user may specify
        separate tick-mark intervals for boundary annotation, ticking, and
        [optionally] gridlines. A simple map scale or directional rose may also
        be plotted.

        At least one of the options *B*, *L*, or *T* must be specified.

        {gmt_module_docs}

        {aliases}

        Parameters
        ----------
        {J}
        {R}
        {B}
        D : str
            ``'[unit]xmin/xmax/ymin/ymax[r][+sfile][+t]'``
            Draw a simple map insert box on the map. Requires *F*.
        F : bool or str
            Without further options, draws a rectangular border around any map
            insert (*D*), map scale (*L*) or map rose (*T*).
        L : str
            ``'[g|j|J|n|x]refpoint'``
            Draws a simple map scale centered on the reference point specified.
        {P}
        Td : str
            Draws a map directional rose on the map at the location defined by
            the reference and anchor points.
        Tm : str
            Draws a map magnetic rose on the map at the location defined by the
            reference and anchor points
        {U}

        """
        kwargs = self._preprocess(**kwargs)
        assert 'B' in kwargs or 'L' in kwargs or 'T' in kwargs, \
            "At least one of B, L, or T must be specified."
        if 'D' in kwargs:
            assert 'F' in kwargs, \
                "Option D requires F to be specified as well."
        with APISession() as session:
            call_module(session, 'psbasemap', build_arg_string(kwargs))
