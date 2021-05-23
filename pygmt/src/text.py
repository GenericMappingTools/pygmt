"""
text - Plot text on a figure.
"""
import numpy as np
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    B="frame",
    C="clearance",
    D="offset",
    G="fill",
    N="no_clip",
    V="verbose",
    W="pen",
    X="xshift",
    Y="yshift",
    c="panel",
    f="coltypes",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(
    R="sequence",
    textfiles="sequence_space",
    angle="sequence_comma",
    font="sequence_comma",
    justify="sequence_comma",
    c="sequence_comma",
    p="sequence",
)
def text_(
    self,
    textfiles=None,
    x=None,
    y=None,
    position=None,
    text=None,
    angle=None,
    font=None,
    justify=None,
    **kwargs,
):
    r"""
    Plot or typeset text strings of variable size, font type, and orientation.

    Must provide at least one of the following combinations as input:

    - ``textfiles``
    - ``x``/``y``, and ``text``
    - ``position`` and ``text``

    Full parameter list at :gmt-docs:`text.html`

    {aliases}

    Parameters
    ----------
    textfiles : str or list
        A text data file name, or a list of filenames containing 1 or more
        records with (x, y[, angle, font, justify], text).
    x/y : float or 1d arrays
        The x and y coordinates, or an array of x and y coordinates to plot
        the text
    position : str
        Sets reference point on the map for the text by using x,y
        coordinates extracted from ``region`` instead of providing them
        through ``x``/``y``. Specify with a two letter (order independent)
        code, chosen from:

        * Horizontal: **L**\ (eft), **C**\ (entre), **R**\ (ight)
        * Vertical: **T**\ (op), **M**\ (iddle), **B**\ (ottom)

        For example, ``position="TL"`` plots the text at the Upper Left corner
        of the map.
    text : str or 1d array
        The text string, or an array of strings to plot on the figure
    angle: int, float, str or bool
        Set the angle measured in degrees counter-clockwise from
        horizontal (e.g. 30 sets the text at 30 degrees). If no angle is
        explicitly given (i.e. ``angle=True``) then the input to ``textfiles``
        must have this as a column.
    font : str or bool
        Set the font specification with format *size*\ ,\ *font*\ ,\ *color*
        where *size* is text size in points, *font* is the font to use, and
        *color* sets the font color. For example,
        ``font="12p,Helvetica-Bold,red"`` selects a 12p, red, Helvetica-Bold
        font. If no font info is explicitly given (i.e. ``font=True``), then
        the input to ``textfiles`` must have this information in one of its
        columns.
    justify : str or bool
        Set the alignment which refers to the part of the text string that
        will be mapped onto the (x,y) point. Choose a 2 character
        combination of **L**, **C**, **R** (for left, center, or right) and
        **T**, **M**, **B** for top, middle, or bottom. E.g., **BL** for lower
        left. If no justification is explicitly given (i.e. ``justify=True``),
        then the input to ``textfiles`` must have this as a column.
    {J}
    {R}
    clearance : str
        [*dx/dy*][**+to**\|\ **O**\|\ **c**\|\ **C**].
        Adjust the clearance between the text and the surrounding box
        [Default is 15% of the font size]. Only used if ``pen`` or ``fill`` are
        specified. Append the unit you want (*c* for cm, *i* for inch, or *p*
        for point; if not given we consult **PROJ_LENGTH_UNIT**) or *%* for a
        percentage of the font size. Optionally, use modifier **+t** to set
        the shape of the textbox when using ``fill`` and/or ``pen``. Append
        lower case **o** to get a straight rectangle [Default is **o**]. Append
        upper case **O** to get a rounded rectangle. In paragraph mode
        (*paragraph*) you can also append lower case **c** to get a concave
        rectangle or append upper case **C** to get a convex rectangle.
    fill : str
        Sets the shade or color used for filling the text box [Default is
        no fill].
    offset : str
        [**j**\|\ **J**]\ *dx*\[/*dy*][**+v**\[*pen*]].
        Offsets the text from the projected (x,y) point by *dx*,\ *dy* [0/0].
        If *dy* is not specified then it is set equal to *dx*. Use **j** to
        offset the text away from the point instead (i.e., the text
        justification will determine the direction of the shift). Using
        **J** will shorten diagonal offsets at corners by sqrt(2).
        Optionally, append **+v** which will draw a line from the original
        point to the shifted point; append a pen to change the attributes
        for this line.
    pen : str
        Sets the pen used to draw a rectangle around the text string
        (see ``clearance``) [Default is width = default, color = black,
        style = solid].
    no_clip : bool
        Do NOT clip text at map boundaries [Default is will clip].
    {V}
    {XY}
    {c}
    {f}
    {p}
    {t}
        *transparency* can also be a 1d array to set varying transparency
        for texts, but this option is only valid if using x/y/text.
    """

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches

    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    # Ensure inputs are either textfiles, x/y/text, or position/text
    if position is None:
        kind = data_kind(textfiles, x, y, text)
    else:
        if x is not None or y is not None:
            raise GMTInvalidInput(
                "Provide either position only, or x/y pairs, not both"
            )
        kind = "vectors"

    if kind == "vectors" and text is None:
        raise GMTInvalidInput("Must provide text with x/y pairs or position")

    # Build the -F option in gmt text.
    if "F" not in kwargs.keys() and (
        (
            position is not None
            or angle is not None
            or font is not None
            or justify is not None
        )
    ):
        kwargs.update({"F": ""})

    if angle is True:
        kwargs["F"] += "+a"
    elif isinstance(angle, (int, float, str)):
        kwargs["F"] += f"+a{str(angle)}"

    if font is True:
        kwargs["F"] += "+f"
    elif isinstance(font, str):
        kwargs["F"] += f"+f{font}"

    if justify is True:
        kwargs["F"] += "+j"
    elif isinstance(justify, str):
        kwargs["F"] += f"+j{justify}"

    if isinstance(position, str):
        kwargs["F"] += f'+c{position}+t"{text}"'

    extra_arrays = []
    # If an array of transparency is given, GMT will read it from
    # the last numerical column per data record.
    if "t" in kwargs and is_nonstr_iter(kwargs["t"]):
        extra_arrays.append(kwargs["t"])
        kwargs["t"] = ""

    with Session() as lib:
        file_context = dummy_context(textfiles) if kind == "file" else ""
        if kind == "vectors":
            if position is not None:
                file_context = dummy_context("")
            else:
                file_context = lib.virtualfile_from_vectors(
                    np.atleast_1d(x),
                    np.atleast_1d(y),
                    *extra_arrays,
                    # text must be in str type, see issue #706
                    np.atleast_1d(text).astype(str),
                )
        with file_context as fname:
            arg_str = " ".join([fname, build_arg_string(kwargs)])
            lib.call_module("text", arg_str)
