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
def psconvert(**kwargs):
    """
    Convert [E]PS file(s) to other formats.

    Converts one or more PostScript files to other formats (BMP, EPS, JPEG,
    PDF, PNG, PPM, SVG, TIFF) using GhostScript.

    If no input files are given, will convert the current active figure (see
    :func:`gmt.figure`). In this case, an output name must be given using
    parameter *F*.

    See full documentation for all options at the GMT website:
    {gmt_mod}

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
    for key in kwargs:
        if isinstance(kwargs[key], bool) and kwargs[key]:
            args.append('-{}'.format(key))
        else:
            args.append('-{}{}'.format(key, kwargs[key]))
    call_module('psconvert', ' '.join(args))
