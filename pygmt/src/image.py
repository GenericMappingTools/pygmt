"""
image - Plot raster or EPS images.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.params import Box


@fmt_docstring
@use_alias(D="position", G="bitcolor", p="perspective")
@kwargs_to_strings(p="sequence")
def image(
    self,
    imagefile: PathLike,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    box: Box | bool = False,
    monochrome: bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot raster or EPS images.

    Reads Encapsulated PostScript (EPS) or raster image files and plots them. The
    image can be scaled arbitrarily, and 1-bit raster images can be:

    - inverted, i.e., black pixels (on) becomes white (off) and vice versa.
    - colorized, by assigning different foreground and background colors.
    - made transparent where either the back- or foreground is painted.

    As an option, the user may choose to convert colored raster images to grayscale
    using TV's YIQ-transformation. For raster files, the user can select which color is
    made transparent. The user may also choose to replicate the image which, when
    preceded by appropriate clip paths, may allow larger custom-designed fill patterns
    to be implemented.

    Full GMT docs at :gmt-docs:`image.html`.

    {aliases}
       - F = box
       - J = projection
       - M = monochrome
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    imagefile
        An Encapsulated PostScript (EPS) file or a raster image file. An EPS file must
        contain an appropriate BoundingBox. A raster file can have a depth of 1, 8, 24,
        or 32 bits and is read via GDAL.
    {projection}
    {region}
    position : str
        [**g**\|\ **j**\|\ **J**\|\ **n**\|\ **x**]\ *refpoint*\ **+r**\ *dpi*\
        **+w**\ [**-**]\ *width*\ [/*height*]\ [**+j**\ *justify*]\
        [**+n**\ *nx*\ [/*ny*]]\ [**+o**\ *dx*\ [/*dy*]].
        Set reference point on the map for the image.
    box
        Draw a background box behind the image. If set to ``True``, a simple rectangular
        box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box appearance,
        pass a :class:`pygmt.params.Box` object to control style, fill, pen, and other
        box properties.
    bitcolor : str or list
        [*color*][**+b**\|\ **f**\|\ **t**].
        Change certain pixel values to another color or make them transparent.
        For 1-bit images you can specify an alternate *color* for the
        background (**+b**) or the foreground (**+f**) pixels, or give no color
        to make those pixels transparent. Can be repeated with different
        settings. Alternatively, for color images you can select a single
        *color* that should be made transparent instead (**+t**).
    monochrome
        Convert color image to monochrome grayshades using the (television)
        YIQ-transformation.
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
        M=Alias(monochrome, name="monochrome"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(
            module="image", args=build_arg_list(aliasdict, infile=imagefile)
        )
