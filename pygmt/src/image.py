"""
image - Plot an image.
"""
from pygmt.clib import Session
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    D="position",
    F="box",
    M="monochrome",
    V="verbose",
    X="xshift",
    Y="yshift",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def image(self, imagefile, **kwargs):
    r"""
    Place images or EPS files on maps.

    Reads an Encapsulated PostScript file or a raster image file and plots
    it on a map.

    Full option list at :gmt-docs:`image.html`

    {aliases}

    Parameters
    ----------
    imagefile : str
        This must be an Encapsulated PostScript (EPS) file or a raster
        image. An EPS file must contain an appropriate BoundingBox. A
        raster file can have a depth of 1, 8, 24, or 32 bits and is read
        via GDAL. Note: If GDAL was not configured during GMT installation
        then only EPS files are supported.
    {J}
    {R}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\ **+r**\ *dpi*\
        **+w**\ [**-**]\ *width*\ [/*height*]\ [**+j**\ *justify*]\
        [**+n**\ *nx*\ [/*ny*] ]\ [**+o**\ *dx*\ [/*dy*]].
        Sets reference point on the map for the image.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        Without further arguments, draws a rectangular border around the image
        using :gmt-term:`MAP_FRAME_PEN`.
    monochrome : bool
        Convert color image to monochrome grayshades using the (television)
        YIQ-transformation.
    {V}
    {XY}
    {c}
    {p}
    {t}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        arg_str = " ".join([imagefile, build_arg_string(kwargs)])
        lib.call_module("image", arg_str)
