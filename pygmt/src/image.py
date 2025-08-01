"""
image - Plot raster or EPS images.
"""

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    D="position",
    F="box",
    G="bitcolor",
    M="monochrome",
    R="region",
    V="verbose",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def image(self, imagefile: PathLike, projection=None, **kwargs):
    r"""
    Plot raster or EPS images.

    Reads an Encapsulated PostScript file or a raster image file and plots
    it on a map.

    Full GMT docs at :gmt-docs:`image.html`.

    {aliases}
       - J=projection

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
        [**+n**\ *nx*\ [/*ny*]]\ [**+o**\ *dx*\ [/*dy*]].
        Set reference point on the map for the image.
    box : bool or str
        [**+c**\ *clearances*][**+g**\ *fill*][**+i**\ [[*gap*/]\ *pen*]]\
        [**+p**\ [*pen*]][**+r**\ [*radius*]][**+s**\ [[*dx*/*dy*/][*shade*]]].
        If set to ``True``, draw a rectangular border around the image
        using :gmt-term:`MAP_FRAME_PEN`.
    bitcolor : str or list
        [*color*][**+b**\|\ **f**\|\ **t**].
        Change certain pixel values to another color or make them transparent.
        For 1-bit images you can specify an alternate *color* for the
        background (**+b**) or the foreground (**+f**) pixels, or give no color
        to make those pixels transparent. Can be repeated with different
        settings. Alternatively, for color images you can select a single
        *color* that should be made transparent instead (**+t**).
    monochrome : bool
        Convert color image to monochrome grayshades using the (television)
        YIQ-transformation.
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        J=Alias(projection, name="projection"),
    ).merge(kwargs)

    with Session() as lib:
        lib.call_module(
            module="image", args=build_arg_list(aliasdict, infile=imagefile)
        )
