"""
image - Plot raster or EPS images.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode, PathLike
from pygmt._typing import PathLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias
from pygmt.params import Box


@fmt_docstring
@use_alias(G="bitcolor", M="monochrome", R="region", p="perspective")
@kwargs_to_strings(R="sequence", p="sequence")
def image(  # noqa: PLR0913
    self,
    imagefile: PathLike,
    position: Sequence[str | float] | AnchorCode | None = None,
    position_type: Literal[
        "mapcoords", "boxcoords", "plotcoords", "inside", "outside"
    ] = "plotcoords",
    anchor: AnchorCode | None = None,
    anchor_offset: Sequence[float | str] | None = None,
    height: float | str | None = None,
    width: float | str | None = None,
    replicate: int | tuple[int, int] | None = None,
    dpi: float | str | None = None,
    projection=None,
    box: Box | bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot raster or EPS images.

    Reads an Encapsulated PostScript file or a raster image file and plot it on a map.

    Full GMT docs at :gmt-docs:`image.html`.

    {aliases}
       - D = position/position_type/anchor/anchor_offset/width/height/replicate/dpi
       - F = box
       - J = projection
       - V = verbose
       - c = panel
       - t = transparency

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
    position/position_type
        Specify the reference point on the plot for the image. The method of defining
        the the reference point is controlled by **position_type**, and the exact
        location is set by **position**.

        The **position_type** parameter can take one of the following values:

        - ``"mapcoords"``: **position** is specified as (*longitude*, *latitude*) in map
          coordinates. Example: (120, -45) places the reference point at 120°E, 45°S.
        - ``"boxcoords"``: **position** is specified as (*nx*, *ny*) in normalized
          coordinates, i.e., fractional values between 0 and 1 along the x- and y-axes.
          Example: (0, 0) corresponds to the lower-left corner, and (1, 1) to the
          upper-right corner of the plot bounding box.
        - ``"plotcoords"``: **position** is specified as (*x*, *y*) in plot coordinates,
          i.e., distances from the lower-left plot origin given in inches, centimeters,
          or points. Example: ("1c", "2c") places the reference point 1 cm to the right
          and 2 cm above the plot origin.
        - ``"inside"`` or ``"outside"``: **position** is one of the nine
          :doc:two-character justification codes </techref/justification_codes>,
          indicating a specific location relative to the plot bounding box. Example:
          ``"TL"`` places the reference point at the top-left corner, either inside or
          outside the bounding box.
    anchor
        Specify the anchor point of the image, using one of the
        :doc:`2-character justification codes </techref/justification_codes>`.
        The default value depends on **position_type**.

        - ``position_type="inside"``: **anchor** defaults to the same as **position**.
        - ``position_type="outside"``: **anchor** defaults to the mirror opposite of
          **position**.
        - Otherwise, **anchor** defaults to ``"MC"`` (middle center).
    anchor_offset
        Specifies an offset for the anchor point as *offset* or
        (*offset_x*, *offset_y*). If a single value *offset* is given, both *offset_x*
        and *offset_y* are set to *offset*.
    dpi
        Specify dpi to set the dpi of the image in dots per inch, or append **c** to
        indicate this is dots per cm.
    replicate
        *nx* or (*nx*, *ny*).
        Replicate the (scaled) image *nx* times in the horizontal direction, and *ny*
        times in the vertical direction. If a single integer *nx* is given, *ny* = *nx*.
        [Default is (1, 1)].
    width/height
        Width (and height) of the image in plot coordinates (inches, cm, etc.). If
        **height** (or **width**) is set to 0, then the original aspect ratio of the
        image is maintained. If **width** (or **height**) is negative, the absolute
        value is used to interpolate image to the device resolution using the PostScript
        image operator. If neither dimensions nor dpi are set then revert to the default
        dpi [:gmt-term:`GMT_GRAPHICS_DPU`].
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
    monochrome : bool
        Convert color image to monochrome grayshades using the (television)
        YIQ-transformation.
    {verbose}
    {panel}
    {perspective}
    {transparency}
    """

    self._activate_figure()

    _dimension = (width, height) if height is not None else width

    # Mapping position_type to GMT single-letter code.
    _position_type = {
        "mapcoords": "g",
        "boxcoords": "n",
        "plotcoords": "x",
        "inside": "j",
        "outside": "J",
    }[position_type]

    aliasdict = AliasSystem(
        D=[
            Alias(position, name="position", sep="/", size=2, prefix=_position_type),
            Alias(anchor, name="anchor", prefix="+j"),
            Alias(anchor_offset, name="anchor_offset", prefix="+o", sep="/", size=2),
            Alias(_dimension, name="width/height", prefix="+w"),
            Alias(replicate, name="replicate", prefix="+n", sep="/", size=2),
            Alias(dpi, name="dpi", prefix="+r"),
        ],
        F=Alias(box, name="box"),
    ).add_common(
        J=projection,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(
            module="image", args=build_arg_list(aliasdict, infile=imagefile)
        )
