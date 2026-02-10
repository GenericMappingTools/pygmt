"""
colorbar - Plot gray scale or color scale bar.
"""

from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring, use_alias
from pygmt.helpers.utils import is_nonstr_iter
from pygmt.params import Box, Position
from pygmt.src._common import _parse_position

__doctest_skip__ = ["colorbar"]


def _alias_option_D(  # noqa: N802, PLR0913
    position=None,
    length=None,
    width=None,
    orientation=None,
    reverse=False,
    nan=False,
    nan_position=None,
    fg_triangle=False,
    bg_triangle=False,
    triangle_height=None,
    move_text=None,
    label_as_column=False,
):
    """
    Return a list of Alias objects for the -D option.

    Examples
    --------
    >>> def parse(**kwargs):
    ...     return AliasSystem(D=_alias_option_D(**kwargs)).get("D")
    >>> parse(position=Position("TL", offset=0.2), length=4, width=0.5)
    'jTL+o0.2+w4/0.5'
    >>> parse(orientation="horizontal")
    '+h'
    >>> parse(orientation="vertical")
    '+v'
    >>> parse(reverse=True)
    '+r'
    >>> parse(nan=True)
    '+n'
    >>> parse(nan=True, nan_position="end")
    '+N'
    >>> parse(fg_triangle=True, bg_triangle=True)
    '+e'
    >>> parse(fg_triangle=True)
    '+ef'
    >>> parse(bg_triangle=True)
    '+eb'
    >>> parse(fg_triangle=True, triangle_height=0.4)
    '+ef0.4'
    >>> parse(fg_triangle=True, bg_triangle=True, triangle_height=0.3)
    '+e0.3'
    >>> parse(move_text="annotations")
    '+ma'
    >>> parse(move_text="label")
    '+ml'
    >>> parse(move_text="unit")
    '+mu'
    >>> parse(move_text=["annotations", "label", "unit"])
    '+malu'
    >>> parse(label_as_column=True)
    '+mc'
    >>> parse(move_text=["annotations", "label"], label_as_column=True)
    '+malc'
    >>> parse(
    ...     position=Position("BR", offset=(0.1, 0.2)),
    ...     length=5,
    ...     width=0.4,
    ...     orientation="vertical",
    ...     reverse=True,
    ...     nan=True,
    ...     nan_position="start",
    ...     bg_triangle=True,
    ...     triangle_height=0.2,
    ...     move_text=["annotations", "unit"],
    ...     label_as_column=True,
    ... )
    'jBR+o0.1/0.2+w5/0.4+v+r+n+eb0.2+mauc'
    """
    # Build the +e modifier from fg_triangle/bg_triangle/triangle_height
    if fg_triangle and bg_triangle:
        modifier_e = ""
    elif fg_triangle:
        modifier_e = "f"
    elif bg_triangle:
        modifier_e = "b"
    else:
        modifier_e = None
    if modifier_e is not None and triangle_height is not None:
        modifier_e = f"{modifier_e}{triangle_height}"

    # Build the +m modifier from move_text/label_as_column
    modifier_m = None
    if move_text or label_as_column:
        modifier_m = ""

        _valids = {"annotations", "label", "unit"}
        if move_text is not None:
            if (isinstance(move_text, str) and move_text not in _valids) or (
                is_nonstr_iter(move_text) and not all(v in _valids for v in move_text)
            ):
                raise GMTValueError(
                    move_text,
                    description="move_text",
                    choices=_valids,
                )
            if isinstance(move_text, str):
                modifier_m = move_text[0]
            elif is_nonstr_iter(move_text):
                modifier_m = "".join(item[0] for item in move_text)
        if label_as_column:
            modifier_m += "c"

    return [
        Alias(position, name="position"),
        Alias(length, name="length", prefix="+w"),  # +wlength/width
        Alias(width, name="width", prefix="/"),
        Alias(
            orientation,
            name="orientation",
            mapping={"horizontal": "+h", "vertical": "+v"},
        ),
        Alias(reverse, name="reverse", prefix="+r"),
        Alias(
            nan,
            name="nan",
            prefix="+n" if nan_position in {"start", None} else "+N",
        ),
        Alias(
            modifier_e,
            name="fg_triangle/bg_triangle/triangle_height",
            prefix="+e",
        ),
        Alias(modifier_m, name="move_text/label_as_column", prefix="+m"),
    ]


@fmt_docstring
@use_alias(C="cmap", L="equalsize", Z="zfile")
def colorbar(  # noqa: PLR0913
    self,
    position: Position | Sequence[float | str] | AnchorCode | None = None,
    length: float | str | None = None,
    width: float | str | None = None,
    orientation: Literal["horizontal", "vertical"] | None = None,
    reverse: bool = False,
    nan: bool = False,
    nan_position: Literal["start", "end"] | None = None,
    bg_triangle: bool = False,
    fg_triangle: bool = False,
    triangle_height: float | None = None,
    move_text: Literal["annotations", "label", "unit"] | Sequence[str] | None = None,
    label_as_column: bool = False,
    box: Box | bool = False,
    truncate: Sequence[float] | None = None,
    shading: float | Sequence[float] | bool = False,
    log: bool = False,
    scale: float | None = None,
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
    Plot gray scale or color scale bar.

    Both horizontal and vertical colorbars are supported. For CPTs with
    gradational colors (i.e., the lower and upper boundary of an interval
    have different colors) we will interpolate to give a continuous scale.
    Variations in intensity due to shading/illumination may be displayed by
    setting the ``shading`` parameter. Colors may be spaced according to a
    linear scale, all be equal size, or by providing a file with individual
    tile widths.

    .. note::
       For GMT >=6.5.0, the fontsizes of the colorbar x-label, x-annotations,
       and y-label are scaled based on the width of the colorbar following
       :math:`\sqrt{colorbar\_width / 15}`. To set a desired fontsize via the
       GMT default parameters :gmt-term:`FONT_ANNOT_PRIMARY`,
       :gmt-term:`FONT_ANNOT_SECONDARY`, and :gmt-term:`FONT_LABEL` (or jointly
       :gmt-term:`FONT`) users have to divide the desired fontsize by the value
       calculated with the formula given above before passing it to the default
       parameters. To only affect fontsizes related to the colorbar, the
       defaults can be changed locally only using ``with pygmt.config(...):``.

    Full GMT docs at :gmt-docs:`colorbar.html`.

    $aliases
       - B = frame
       - F = box
       - G = truncate
       - I = shading
       - J = projection
       - Q = log
       - R = region
       - V = verbose
       - W = scale
       - c = panel
       - p = perspective
       - t = transparency

    .. hlist::
       :columns: 1

       - D = position, **+w**: length/width, **+h**/**+v**: orientation,
         **+r**: reverse, **+n**: nan/nan_position,
         **+e**: fg_triangle/bg_triangle/triangle_height,
         **+m**: move_text/label_as_column

    Parameters
    ----------
    $cmap
    position
        Position of the colorbar on the plot. It can be specified in multiple ways:

        - A :class:`pygmt.params.Position` object to fully control the reference point,
          anchor point, and offset.
        - A sequence of two values representing the x- and y-coordinates in plot
          coordinates, e.g., ``(1, 2)`` or ``("1c", "2c")``.
        - A :doc:`2-character justification code </techref/justification_codes>` for a
          position inside the plot, e.g., ``"TL"`` for Top Left corner inside the plot.

        If not specified, defaults to bottom-center outside of the plot.
    length
    width
        Length and width of the colorbar. If length is given with a unit ``%`` then it
        is in percentage of the corresponding plot side dimension (i.e., plot width for
        a horizontal colorbar, or plot height for a vertical colorbar). If width is
        given with unit ``%`` then it is in percentage of the bar length. [Length
        defaults to 80% of the corresponding plot side dimension, and width defaults
        to 4% of the bar length].
    orientation
        Set the colorbar orientation to either ``"horizontal"`` or ``"vertical"``.
        [Default is vertical, unless ``position`` is set to bottom-center or top-center
        with ``cstype="outside"`` or ``cstype="inside"``, then horizontal is the
        default].
    reverse
        Reverse the positive direction of the bar.
    nan
        Draw a rectangle filled with the NaN color (via the **N** entry in the CPT or
        :gmt-term:`COLOR_NAN` if no such entry) at the start or end of the colorbar
        (controlled via ``nan_position``). If a string is given, use that string as the
        label for the NaN color.
    nan_position
        Set the position of the NaN rectangle. Choose either ``"start"`` or ``"end"`` to
        place the NaN color rectangle at the start or end of the colorbar [Default is
        ``"start"``].
    bg_triangle
    fg_triangle
        If ``True``, draw triangles for the back- or foreground colors [Default is
        no triangles]. The back- and/or foreground colors are taken from the **B**
        and **F** entries in the CPT. If no such entries exist, then the system default
        colors for **B** and **F** are used instead (:gmt-term:`COLOR_BACKGROUND` and
        :gmt-term:`COLOR_FOREGROUND`).
    triangle_height
        Height of the triangles for back- and foreground colors [Default is half of the
        bar width].
    move_text
        Move text (annotations, label, and unit) to opposite side. Accept a sequence of
        strings containing one or more of ``"annotations"``, ``"label"``, and
        ``"unit"``. The default placements of these texts depend on the colorbar
        orientation and position.
    label_as_column
        Print a vertical label as a column of characters (does not work with special
        characters).
    box
        Draw a background box behind the colorbar. If set to ``True``, a simple
        rectangular box is drawn using :gmt-term:`MAP_FRAME_PEN`. To customize the box
        appearance, pass a :class:`pygmt.params.Box` object to control style, fill, pen,
        and other box properties.
    truncate
        (*zlow*, *zhigh*).
        Truncate the incoming CPT so that the lowest and highest z-levels are to *zlow*
        and *zhigh*. If one of these equal NaN then we leave that end of the CPT alone.
        The truncation takes place before the plotting.
    scale
        Multiply all z-values in the CPT by the provided scale. By default, the CPT is
        used as is.
    shading
        Add illumination effects [Default is no illumination].

        - If ``True``, a default intensity range of -1 to +1 is used.
        - Passing a single numerical value *max_intens* sets the range of intensities
          from *-max_intens* to *+max_intens*.
        - Passing a sequence of two numerical values (*low*, *high*) sets the intensity
          range from *low* to *high* to specify an asymmetric range.
    equalsize : float or str
        [**i**]\ [*gap*].
        Equal-sized color rectangles. By default, the rectangles are scaled
        according to the z-range in the CPT (see also ``zfile``). If *gap* is
        appended and the CPT is discrete each annotation is centered on each
        rectangle, using the lower boundary z-value for the annotation. If
        **i** is prepended the interval range is annotated instead. If
        ``shading`` is used each rectangle will have its constant color
        modified by the specified intensity.
    log
        Select logarithmic scale and power of ten annotations. All z-values in the CPT
        will be converted to :math:`p = \log_{10}(z)` and only integer p values will be
        annotated using the :math:`10^{p}` format [Default is linear scale].
    zfile : str
        File with colorbar-width per color entry. By default, the width of the
        entry is scaled to the color range, i.e., z = 0-100 gives twice the
        width as z = 100-150 (see also ``equalsize``). **Note**: The widths
        may be in plot distance units or given as relative fractions and will
        be automatically scaled so that the sum of the widths equals the
        requested colorbar length.
    $projection
    $region
    frame
        Set colorbar boundary frame, labels, and axes attributes. If set to ``"none"``,
        then no frame will be drawn.
    $verbose
    $panel
    $perspective
    $transparency

    Example
    -------
    >>> import pygmt
    >>> # Create a new figure instance with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # Create a basemap
    >>> fig.basemap(region=[0, 10, 0, 3], projection="X10c/3c", frame=True)
    >>> # Call the colorbar method for the plot
    >>> fig.colorbar(
    ...     # Set cmap to the "roma" CPT
    ...     cmap="SCM/roma",
    ...     # Label the x-axis "Velocity" and the y-axis "m/s"
    ...     frame=["x+lVelocity", "y+lm/s"],
    ... )
    >>> # Show the plot
    >>> fig.show()
    """
    self._activate_figure()

    position = _parse_position(
        position,
        default=None,  # Use GMT's default behavior if position is not provided.
        kwdict={
            "length": length,
            "width": width,
            "orientation": orientation,
            "reverse": reverse,
            "nan": nan,
            "nan_position": nan_position,
            "bg_triangle": bg_triangle,
            "fg_triangle": fg_triangle,
            "triangle_height": triangle_height,
            "move_text": move_text,
            "label_as_column": label_as_column,
        },
    )

    aliasdict = AliasSystem(
        D=_alias_option_D(
            position=position,
            length=length,
            width=width,
            orientation=orientation,
            reverse=reverse,
            nan=nan,
            nan_position=nan_position,
            bg_triangle=bg_triangle,
            fg_triangle=fg_triangle,
            triangle_height=triangle_height,
            move_text=move_text,
            label_as_column=label_as_column,
        ),
        F=Alias(box, name="box"),
        G=Alias(truncate, name="truncate", sep="/", size=2),
        I=Alias(shading, name="shading", sep="/", size=2),
        Q=Alias(log, name="log"),
        W=Alias(scale, name="scale"),
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
        lib.call_module(module="colorbar", args=build_arg_list(aliasdict))
