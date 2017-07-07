"""
Function wrapper for the ps* modules.
"""
from .clib import call_module
from .utils import gmt_docs_link


def pscoast():
    """
    Create coastlines.
    """
    pass


@gmt_docs_link
def psbasemap(**kwargs):
    """
    Produce a basemap for the figure.

    Several map projections are available, and the user may specify separate
    tick-mark intervals for boundary annotation, ticking, and [optionally]
    gridlines. A simple map scale or directional rose may also be plotted.

    At least one of the options *B*, *L*, or *T* must be specified.

    {gmt_module_docs}

    Parameters
    ----------
    J : str
        *Required*. Select map projection.
    R : str or list
        *Required*.  ``'xmin/xmax/ymin/ymax[+r][+uunit]'``. Specify the region
        of interest.
    B : str
        Set map boundary frame and axes attributes.
    D : str
        ``'[unit]xmin/xmax/ymin/ymax[r][+sfile][+t]'``
        Draw a simple map insert box on the map. Requires *F*.
    F : bool or str
        Without further options, draws a rectangular border around any map
        insert (*D*), map scale (*L*) or map rose (*T*).
    L : str
        ``'[g|j|J|n|x]refpoint'``
        Draws a simple map scale centered on the reference point specified.
    P : bool
        Select “Portrait” plot orientation.
    Td : str
        Draws a map directional rose on the map at the location defined by the
        reference and anchor points.
    Tm : str
        Draws a map magnetic rose on the map at the location defined by the
        reference and anchor points
    U : bool or str
        Draw GMT time stamp logo on plot.

    """
    assert 'R' in kwargs, 'Parameter R is required.'
    assert 'J' in kwargs, 'Parameter J is required.'
    assert 'B' in kwargs or 'L' in kwargs or 'T' in kwargs, \
        "At least one of B, L, or T must be specified."
    if 'D' in kwargs:
        assert 'F' in kwargs, "Option D requires F to be specified as well."
    args = []
    for arg, value in kwargs.items():
        # Check if the value is an iterable so that we can parse arguments that
        # are lists or other non-string iterables
        try:
            [item for item in value]  # pylint: disable=pointless-statement
            is_iterable = True
        except TypeError:
            is_iterable = False

        if isinstance(value, bool) and value:
            args.append('-{}'.format(arg))
        elif not isinstance(value, str) and is_iterable:
            arg_str = '/'.join('{}'.format(item) for item in value)
            args.append('-{}{}'.format(arg, arg_str))
        else:
            args.append('-{}{}'.format(arg, value))
    call_module('psbasemap', ' '.join(args))


@gmt_docs_link
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
    args = []
    for arg, value in kwargs.items():
        if isinstance(value, bool) and value:
            args.append('-{}'.format(arg))
        else:
            args.append('-{}{}'.format(arg, value))
    call_module('psconvert', ' '.join(args))
