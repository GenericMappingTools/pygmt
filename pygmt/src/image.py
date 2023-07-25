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
    G="bitcolor",
    M="monochrome",
    V="verbose",
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
        via GDAL. **Note**: If GDAL was not configured during GMT installation
        then only EPS files are supported.
    {projection}
    {region}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\ **+r**\ *dpi*\
        **+w**\ [**-**]\ *width*\ [/*height*]\ [**+j**\ *justify*]\
        [**+n**\ *nx*\ [/*ny*] ]\ [**+o**\ *dx*\ [/*dy*]].
        Set reference point on the map for the image.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draw a rectangular border around the image
        using :gmt-term:`MAP_FRAME_PEN`.
    bitcolor : str
        [*color*][**+b**\|\ **f**\|\ **t**]
        Change certain pixel values to another color or make them transparent.
        For 1-bit images you can specify an alternate *color* for the
        background (**+b**) or the foreground (**+f**) pixels, or give no color
        to make those pixels transparent. Alternatively, for color images you
        can select a single *color* that should be made transparent instead
        (**+t**). This option may be repeated with different settings.
    monochrome : bool
        Convert color image to monochrome grayshades using the (television)
        YIQ-transformation.
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    with Session() as lib:
        lib.call_module(module="image", args=build_arg_string(kwargs, infile=imagefile))
