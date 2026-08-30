"""
image - Plot raster or EPS images.
"""

import warnings
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode, PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTParameterError, GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring
from pygmt.params import Axis, Box, Frame, Position
from pygmt.src._common import _parse_position


@fmt_docstring
def image(
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
    bgcolor: str | None = None,
    fgcolor: str | None = None,
    transparent_color: str | None = None,
    bitcolor: str | Sequence[str] | None = None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    frame: Frame | Axis | Literal["none"] | str | Sequence[str] | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    perspective: float | Sequence[float] | str | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot raster or EPS images.

    Reads an Encapsulated PostScript file or a raster image file and plots it.
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

    **Aliases:**

    .. hlist::
       :columns: 3

       - B = frame
       - D = position, **+w**: width/height, **+r**: dpi, **+n**: replicate
       - F = box
       - G = bgcolor, fgcolor, transparent_color, bitcolor
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
        Position of the image on the plot. It can be specified in multiple ways:

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
        Width (and height) of the image in plot dimension, with an optional
        :ref:`dimension unit <dimension-units>`. If ``height`` (or ``width``) is set to
        0, then the original aspect ratio of the image is maintained. If ``width`` (or
        ``height``) is negative, the absolute value is used to interpolate image to the
        device resolution using the PostScript image operator. If neither dimensions nor
        ``dpi`` are set then revert to the default dpi [:gmt-term:`GMT_GRAPHICS_DPU`].
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
    bgcolor
    fgcolor
        For 1-bit images, set the background and foreground colors [Default is black and
        white, respectively]. Setting either to an empty string makes those pixels
        transparent. Cannot be both empty.
    transparent_color
        For color images, set a single color that should be made transparent.
    bitcolor
        [*color*][**+b**\|\ **f**\|\ **t**].
        Change certain pixel values to another color or make them transparent. For 1-bit
        images you can specify an alternate *color* for the background (**+b**) or the
        foreground (**+f**) pixels, or give no color to make those pixels transparent.
        Alternatively, for color images you can select a single *color* that should be
        made transparent instead (**+t**). Pass a list of to specify multiple settings.

        .. deprecated:: 0.20.0

            Use ``bgcolor``, ``fgcolor``, or ``transparent_color`` instead. Will be
            removed in 0.24.0.
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
    position = _parse_position(
        position,
        default=Position((0, 0), cstype="plotcoords"),  # Default to (0,0) in plotcoords
        kwdict={"width": width, "height": height, "dpi": dpi, "replicate": replicate},
    )

    # width is required when only height is given.
    if width is None and height is not None:
        width = 0

    # TODO(PyGMT>=0.24.0): Remove the deprecated "bitcolor" parameter.
    if bitcolor is not None:
        msg = (
            "The 'bitcolor' parameter has been deprecated since v0.20.0 and will be "
            "removed in v0.24.0. Use 'bgcolor', 'fgcolor' or 'transparent_color' "
            "instead."
        )
        warnings.warn(msg, category=FutureWarning, stacklevel=2)
        if any(v is not None for v in [bgcolor, fgcolor, transparent_color]):
            raise GMTParameterError(
                conflicts_with=(
                    "bitcolor",
                    ["bgcolor", "fgcolor", "transparent_color"],
                ),
            )

    # 'bgcolor' and 'fgcolor' cannot both be empty.
    if bgcolor == "" and fgcolor == "":
        _value = f"{bgcolor=}, {fgcolor=}"
        raise GMTValueError(
            _value,
            description="bgcolor and fgcolor",
            reason="'bgcolor' and 'fgcolor' cannot both be empty.",
        )
    # GMT requires a color for the "+t" modifier.
    if transparent_color == "":
        raise GMTValueError(
            transparent_color,
            description="value for 'transparent_color'",
            reason="'transparent_color' cannot be empty.",
        )

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position"),
            Alias(width, name="width", prefix="+w"),  # +wwidth/height
            Alias(height, name="height", prefix="/"),
            Alias(replicate, name="replicate", prefix="+n", sep="/", size=2),
            Alias(dpi, name="dpi", prefix="+r"),
        ],
        F=Alias(box, name="box"),
        G=[
            Alias(bgcolor, name="bgcolor", suffix="+b"),
            Alias(fgcolor, name="fgcolor", suffix="+f"),
            Alias(transparent_color, name="transparent_color", suffix="+t"),
        ]
        if bitcolor is None
        else Alias(bitcolor, name="bitcolor"),
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

    self._activate_figure()
    with Session() as lib:
        lib.call_module(
            module="image", args=build_arg_list(aliasdict, infile=imagefile)
        )
