"""
image - Plot raster or EPS images.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias
from pygmt.params import Box, Position


@fmt_docstring
@use_alias(G="bitcolor")
def image(  # noqa: PLR0913
    self,
    imagefile: PathLike,
    position: Position | None = None,
    height: float | str | None = None,
    width: float | str | None = None,
    replicate: int | tuple[int, int] | None = None,
    dpi: float | str | None = None,
    box: Box | bool = False,
    monochrome: bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    transparency: float | None = None,
    perspective: float | Sequence[float] | str | bool = False,
    **kwargs,
):
    r"""
    Plot raster or EPS images.

    Reads an Encapsulated PostScript file or a raster image file and plot it on a map.
    The image can be scaled arbitrarily, and 1-bit raster images can be:

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
       - D = position, **+w**: width/height, **+n**: replicate, **+r**: dpi
       - F = box
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
    position
        Specify the position of the image on the plot. See
        :class:`pygmt.params.Position` for details.
    width
        height
        Width (and height) of the image in plot coordinates (inches, cm, etc.). If
        **height** (or **width**) is set to 0, then the original aspect ratio of the
        image is maintained. If **width** (or **height**) is negative, the absolute
        value is used to interpolate image to the device resolution using the PostScript
        image operator. If neither dimensions nor dpi are set then revert to the default
        dpi [:gmt-term:`GMT_GRAPHICS_DPU`].
    dpi
        Specify dpi to set the dpi of the image in dots per inch, or append **c** to
        indicate this is dots per cm.
    replicate
        *nx* or (*nx*, *ny*).
        Replicate the (scaled) image *nx* times in the horizontal direction, and *ny*
        times in the vertical direction. If a single integer *nx* is given, *ny* = *nx*.
        [Default is (1, 1)].
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
    $projection
    $region
    $verbose
    $panel
    $perspective
    $transparency
    """
    self._activate_figure()

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position"),
            Alias(width, name="width", prefix="+w"),
            Alias(height, name="height", prefix="/"),
            Alias(replicate, name="replicate", prefix="+n", sep="/", size=2),
            Alias(dpi, name="dpi", prefix="+r"),
        ],
        F=Alias(box, name="box"),
        M=Alias(monochrome, name="monochrome"),
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
