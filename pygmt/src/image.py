"""
image - Plot raster or EPS images.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias
from pygmt.params import Box


@fmt_docstring
@use_alias(D="position", G="bitcolor")
def image(  # noqa: PLR0913
    self,
    imagefile: PathLike,
    box: Box | bool = False,
    monochrome: bool = False,
    invert: bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
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

    $aliases
       - F = box
       - I = invert
       - J = projection
       - M = monochrome
       - R = region
       - V = verbose
       - c = panel
       - p = perspective
       - t = transparency

    Parameters
    ----------
    imagefile
        An Encapsulated PostScript (EPS) file or a raster image file. An EPS file must
        contain an appropriate BoundingBox. A raster file can have a depth of 1, 8, 24,
        or 32 bits and is read via GDAL.
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
    invert
        Invert 1-bit image before plotting, i.e., black pixels (on) becomes white (off)
        and vice versa. Ignored if used with color images.

        **Note**: There was an upstream GMT bug, so this feature may not work correctly
        for some 1-bit images for GMT<=6.6.0.
        See `PR #8837 <https://github.com/GenericMappingTools/gmt/pull/8837>`__.
    $projection
    $region
    $verbose
    $panel
    $perspective
    $transparency
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        F=Alias(box, name="box"),
        M=Alias(monochrome, name="monochrome"),
        I=Alias(invert, name="invert"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        p=perspective,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(
            module="image", args=build_arg_list(aliasdict, infile=imagefile)
        )
