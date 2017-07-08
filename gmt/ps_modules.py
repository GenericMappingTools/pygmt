"""
Function wrapper for the ps* modules.
"""
from .clib import call_module
from .utils import fmt_docstring, parse_bools, parse_region, kwargs2string, \
    use_alias


@fmt_docstring
@use_alias(R='region', J='projection', B='frame', P='portrait', S='style',
           G='color')
@parse_bools
@parse_region
def psxy(data, **kwargs):
    """
    Plot lines, polygons, and symbols on maps.

    Takes (x,y) pairs as inputs or reads them from a file and plots lines,
    polygons, or symbols at those locations on a map.

    If a symbol is selected and no symbol size given, then psxy will interpret
    the third column of the input data as symbol size. Symbols whose size is <=
    0 are skipped. If no symbols are specified then the symbol code (see *S*
    below) must be present as last column in the input. If *S* is not used, a
    line connecting the data points will be drawn instead. To explicitly close
    polygons, use *L*. Select a fill with *G*. If *G* is set, *W* will control
    whether the polygon outline is drawn or not. If a symbol is selected, *G*
    and *W* determines the fill and outline/no outline, respectively.

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
        By default, geographic line segments are drawn as great circle arcs. To
        draw them as straight lines, use *A*.
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
    {U}
    W : str
        Set pen attributes for lines or the outline of symbols.


    """
    assert isinstance(data, str), 'Only accepts file names for now.'
    arg_str = ' '.join([data, kwargs2string(kwargs)])
    call_module('psxy', arg_str)


@fmt_docstring
@use_alias(R='region', J='projection', B='frame', P='portrait')
@parse_bools
@parse_region
def psbasemap(**kwargs):
    """
    Produce a basemap for the figure.

    Several map projections are available, and the user may specify separate
    tick-mark intervals for boundary annotation, ticking, and [optionally]
    gridlines. A simple map scale or directional rose may also be plotted.

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
        Draws a map directional rose on the map at the location defined by the
        reference and anchor points.
    Tm : str
        Draws a map magnetic rose on the map at the location defined by the
        reference and anchor points
    {U}

    """
    assert 'B' in kwargs or 'L' in kwargs or 'T' in kwargs, \
        "At least one of B, L, or T must be specified."
    if 'D' in kwargs:
        assert 'F' in kwargs, "Option D requires F to be specified as well."
    call_module('psbasemap', kwargs2string(kwargs))


@fmt_docstring
@parse_bools
def psconvert(**kwargs):
    """
    Convert [E]PS file(s) to other formats.

    Converts one or more PostScript files to other formats (BMP, EPS, JPEG,
    PDF, PNG, PPM, SVG, TIFF) using GhostScript.

    If no input files are given, will convert the current active figure (see
    :func:`gmt.figure`). In this case, an output name must be given using
    parameter *F*.

    {gmt_module_docs}

    Parameters
    ----------
    A : str
        ``'[u][margins][-][+gpaint][+p[pen]][+r][+s[m]|Swidth[u]/height[u]]'``
        Adjust the BoundingBox and HiResBoundingBox to the minimum required by
        the image content. Append ``u`` to first remove any GMT-produced
        time-stamps.
    C : str
        Specify a single, custom option that will be passed on to GhostScript
        as is.
    D : str
        Sets an alternative output directory (which must exist). Default is the
        same directory as the PS files.
    E : int
        Set raster resolution in dpi. Default = 720 for PDF, 300 for others.
    F : str
        Force the output file name. By default output names are constructed
        using the input names as base, which are appended with an appropriate
        extension. Use this option to provide a different name, but without
        extension. Extension is still determined automatically.
    I : bool
        Enforce gray-shades by using ICC profiles.
    P : bool
        Force Portrait mode. All Landscape mode plots will be rotated back so
        that they show unrotated in Portrait mode. This is practical when
        converting to image formats or preparing EPS or PDF plots for inclusion
        in documents.
    Q : str
        Set the anti-aliasing options for graphics or text. Append the size of
        the subsample box (1, 2, or 4) [4]. Default is no anti-aliasing (same
        as bits = 1).
    T : str
        Sets the output format, where b means BMP, e means EPS, E means EPS
        with PageSize command, f means PDF, F means multi-page PDF, j means
        JPEG, g means PNG, G means transparent PNG (untouched regions are
        transparent), m means PPM, s means SVG, and t means TIFF [default is
        JPEG]. To bjgt you can append - in order to get a grayscale image. The
        EPS format can be combined with any of the other formats. For example,
        ``'ef'`` creates both an EPS and a PDF file. The ``'F'`` creates a
        multi-page PDF file from the list of input PS or PDF files. It requires
        the *F* option.

    """
    call_module('psconvert', kwargs2string(kwargs))
