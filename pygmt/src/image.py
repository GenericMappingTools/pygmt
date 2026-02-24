"""
image - Plot raster or EPS images.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode, PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position


@fmt_docstring
@use_alias(G="bitcolor")
def image(  # noqa: PLR0913
    self,
    imagefile: PathLike,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    width: float | str | None = None,
    height: float | str | None = None,
    dpi: float | str | None = None,
    replicate: int | Sequence[int] | None = None,
    box: Box | bool = False,
    monochrome: bool = False,
    invert: bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: str | Sequence[str] | Literal["none"] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot raster or EPS images.

    Reads an Encapsulated PostScript file or a raster image file and plot it on a map.
    The image can be scaled arbitrarily, and 1-bit raster images can be:

    - inverted, i.e., black pixels (on) become white (off) and vice versa.
    - colorized, by assigning different foreground and background colors.
    - made transparent where either the back- or foreground is painted.

    As an option, the user may choose to convert colored raster images to grayscale
    using TV's YIQ-transformation. For raster files, the user can select which color is
    made transparent. The user may also choose to replicate the image which, when
    preceded by appropriate clip paths, may allow larger custom-designed fill patterns
    to be implemented.

    Full GMT docs at :gmt-docs:`image.html`.

    $aliases
       - B = frame
       - D = position, **+w**: width/height, **+r**: dpi, **+n**: replicate
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
    position
        Position of the GMT logo on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x- and y-coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to the Bottom Left corner of the plot (position
        ``(0, 0)`` with anchor ``"BL"``).
    width
    height
        Width (and height) of the image in plot coordinates (inches, cm, etc.). If
        ``height`` (or ``width``) is set to 0, then the original aspect ratio of the
        image is maintained. If ``width`` (or ``height``) is negative, the absolute
        value is used to interpolate image to the device resolution using the PostScript
        image operator. If neither dimensions nor ``dpi`` are set then revert to the
        default dpi [:gmt-term:`GMT_GRAPHICS_DPU`].
    dpi
        Set the dpi of the image in dots per inch, or append **c** to indicate this is
        dots per cm.
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
    invert
        Invert 1-bit image before plotting, i.e., black pixels (on) become white (off)
        and vice versa. Ignored if used with color images.

        **Note**: There was an upstream GMT bug, so this feature may not work correctly
        for some 1-bit images for GMT<=6.6.0.
        See `PR #8837 <https://github.com/GenericMappingTools/gmt/pull/8837>`__.
    $projection
    $region
    $frame
    $verbose
    $panel
    $perspective
    $transparency
    """
    self._activate_figure()

    position = _parse_position(
        position,
        default=Position((0, 0), cstype="plotcoords"),  # Default to (0,0) in plotcoords
        kwdict={"width": width, "height": height, "dpi": dpi, "replicate": replicate},
    )

    # width is required when only height is given.
    if width is None and height is not None:
        width = 0

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position"),
            Alias(width, name="width", prefix="+w"),  # +wwidth/height
            Alias(height, name="height", prefix="/"),
            Alias(replicate, name="replicate", prefix="+n", sep="/", size=2),
            Alias(dpi, name="dpi", prefix="+r"),
        ],
        F=Alias(box, name="box"),
        M=Alias(monochrome, name="monochrome"),
        I=Alias(invert, name="invert"),
    ).add_common(
        B=frame,
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
