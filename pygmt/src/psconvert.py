"""
psconvert - Convert [E]PS file(s) to other formats using Ghostscript.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Literal

from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias


@fmt_docstring
@use_alias(A="crop", I="resize", N="bb_style", T="fmt", Q="anti_aliasing")
def psconvert(
    self,
    prefix: str | None = None,
    dpi: int | None = None,
    gs_option: str | Sequence[str] | None = None,
    gs_path: str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
):
    r"""
    Convert [E]PS file(s) to other formats using Ghostscript.

    Converts one or more PostScript files to other formats (BMP, EPS, JPEG,
    PDF, PNG, PPM, TIFF) using Ghostscript.

    If no input files are given, will convert the current active figure
    (see :class:`pygmt.Figure`). In this case, an output name must be given
    using parameter ``prefix``.

    Full GMT docs at :gmt-docs:`psconvert.html`.

    {aliases}
       - C = gs_option
       - E = dpi
       - F = prefix
       - G = gs_path
       - V = verbose

    Parameters
    ----------
    crop : str or bool
        Adjust the BoundingBox and HiResBoundingBox to the minimum
        required by the image content. Default is ``True``. Append **+u** to
        first remove any GMT-produced time-stamps. Append **+r** to
        *round* the HighResBoundingBox instead of using the ``ceil``
        function. This is going against Adobe Law but can be useful when
        creating very small images where the difference of one pixel
        might matter. If ``verbose`` is used we also report the
        dimensions of the final illustration.
    gs_path
        Full path to the Ghostscript executable.
    gs_option
        Specify one or a list of custom options that will be passed on to Ghostscript
        as is.
    dpi
        Set raster resolution in dpi [Default is 720 for PDF, 300 for others]. **Note**:
        Ghostscript limits the final width and height pixel dimensions of a raster file
        to be less than or equal to 65536.
    prefix
        Force the output file name. By default output names are constructed using the
        input names as base, which are appended with an appropriate extension. Use this
        parameter to provide a different name, but without extension. Extension is still
        determined automatically.
    resize : str
        [**+m**\ *margins*][**+s**\ [**m**]\ *width*\
        [/\ *height*]][**+S**\ *scale*].
        Adjust the BoundingBox and HiResBoundingBox by scaling and/or
        adding margins. Append **+m** to specify extra margins to extend
        the bounding box. Give either one (uniform), two (x and y) or four
        (individual sides) margins; append unit [Default is set by
        :gmt-term:`PROJ_LENGTH_UNIT`]. Append **+s**\ *width* to resize the
        output image to exactly *width* units. The default unit is set by
        :gmt-term:`PROJ_LENGTH_UNIT` but you can append a new unit and/or
        impose different width and height (**Note**: This may change the
        image aspect ratio). What happens here is that Ghostscript will do
        the re-interpolation work and the final image will retain the DPI
        resolution set by ``dpi``.  Append **+sm** to set a maximum size
        and the new *width* is only imposed if the original figure width
        exceeds it. Append /\ *height* to also impose a maximum height in
        addition to the width. Alternatively, append **+S**\ *scale* to
        scale the image by a constant factor.
    bb_style : str
        Set optional BoundingBox fill color, fading, or draw the outline
        of the BoundingBox. Append **+f**\ *fade* to fade the entire plot
        towards black (100%) [no fading, 0]. Append **+g**\ *paint* to
        paint the BoundingBox behind the illustration and append **+p**\
        [*pen*] to draw the BoundingBox outline (append a pen or accept
        the default pen of ``"0.25p,black,solid"``). **Note**: If both **+g** and
        **+f** are used then we use *paint* as the fade color instead of
        black. Append **+i** to enforce gray-shades by using ICC profiles.
    anti_aliasing : str
        [**g**\|\ **p**\|\ **t**\][**1**\|\ **2**\|\ **4**].
        Set the anti-aliasing options for **g**\ raphics or **t**\ ext.
        Append the size of the subsample box (1, 2, or 4) [Default is
        ``"4"``]. [Default is no anti-aliasing (same as bits = 1).]
    fmt : str
        Set the output format, where **b** means BMP, **e** means EPS,
        **E** means EPS with PageSize command, **f** means PDF, **F** means
        multi-page PDF, **j** means JPEG, **g** means PNG, **G** means
        transparent PNG (untouched regions are transparent), **m** means
        PPM, and **t** means TIFF [Default is JPEG]. To
        **b**\|\ **j**\|\ **g**\|\ **t**\ , optionally append **+m** in
        order to get a monochrome (grayscale) image. The EPS format can be
        combined with any of the other formats. For example, **ef** creates
        both an EPS and a PDF file. Using **F** creates a multi-page PDF
        file from the list of input PS or PDF files. It requires the
        ``prefix`` parameter.
    {verbose}
    """
    self._activate_figure()
    # Default cropping the figure to True
    if kwargs.get("A") is None:
        kwargs["A"] = ""

    if prefix in {"", None, False, True}:
        raise GMTValueError(
            prefix,
            description="output file name",
            reason="Parameter 'prefix' can't be None, bool, or an empty string.",
        )

    # Check if the parent directory exists
    prefix_path = Path(prefix).parent  # type: ignore[arg-type]
    if not prefix_path.exists():
        msg = f"No such directory: {prefix_path!r}, please create it first."
        raise FileNotFoundError(msg)

    aliasdict = AliasSystem(
        C=Alias(gs_option, name="gs_option"),
        E=Alias(dpi, name="dpi"),
        F=Alias(prefix, name="prefix"),
        G=Alias(gs_path, name="gs_path"),
    ).add_common(
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="psconvert", args=build_arg_list(aliasdict))
