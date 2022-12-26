"""
text - Plot text on a figure.
"""
import numpy as np
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    deprecate_parameter,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@deprecate_parameter("incols", "use_word", "v0.8.0", remove_version="v0.10.0")
@use_alias(
    R="region",
    J="projection",
    B="frame",
    C="clearance",
    D="offset",
    G="fill",
    N="no_clip",
    U="timestamp",
    V="verbose",
    W="pen",
    a="aspatial",
    c="panel",
    e="find",
    f="coltypes",
    h="header",
    it="use_word",
    p="perspective",
    t="transparency",
    w="wrap",
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

    Full option list at :gmt-docs:`text.html`

    {aliases}

    Parameters
    ----------
    textfiles : str or list
        A text data file name, or a list of file names containing 1 or more
        records with (x, y[, angle, font, justify], text).
    x/y : float or 1-D arrays
        The x and y coordinates, or an array of x and y coordinates to plot
        the text.
    position : str
        Sets reference point on the map for the text by using x, y
        coordinates extracted from ``region`` instead of providing them
        through ``x``/``y``. Specify with a two-letter (order independent)
        code, chosen from:

        * Horizontal: **L**\ (eft), **C**\ (entre), **R**\ (ight)
        * Vertical: **T**\ (op), **M**\ (iddle), **B**\ (ottom)

        For example, ``position="TL"`` plots the text at the Top Left corner
        of the map.
    text : str or 1-D array
        The text string, or an array of strings to plot on the figure.
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
        will be mapped onto the (x, y) point. Choose a two-letter
        combination of **L**, **C**, **R** (for left, center, or right) and
        **T**, **M**, **B** (for top, middle, or bottom). E.g., **BL** for
        bottom left. If no justification is explicitly given
        (i.e. ``justify=True``), then the input to ``textfiles`` must have
        this as a column.
    {projection}
    {region}
        *Required if this is the first plot command.*
    clearance : str
        [*dx/dy*][**+to**\|\ **O**\|\ **c**\|\ **C**].
        Adjust the clearance between the text and the surrounding box
        [Default is 15% of the font size]. Only used if ``pen`` or ``fill`` are
        specified. Append the unit you want (*c* for cm, *i* for inch, or *p*
        for point; if not given we consult :gmt-term:`PROJ_LENGTH_UNIT`)
        or *%* for a percentage of the font size. Optionally, use modifier
        **+t** to set the shape of the text box when using ``fill`` and/or
        ``pen``. Append lower case **o** to get a straight rectangle
        [Default is **o**]. Append upper case **O** to get a rounded
        rectangle. In paragraph mode (*paragraph*) you can also append lower
        case **c** to get a concave rectangle or append upper case **C**
        to get a convex rectangle.
    fill : str
        Sets the shade or color used for filling the text box [Default is
        no fill].
    offset : str
        [**j**\|\ **J**]\ *dx*\[/*dy*][**+v**\[*pen*]].
        Offsets the text from the projected (x, y) point by *dx*/\ *dy*
        [Default is ``"0/0"``].
        If *dy* is not specified then it is set equal to *dx*. Use **j** to
        offset the text away from the point instead (i.e., the text
        justification will determine the direction of the shift). Using
        **J** will shorten diagonal offsets at corners by sqrt(2).
        Optionally, append **+v** which will draw a line from the original
        point to the shifted point; append a pen to change the attributes
        for this line.
    pen : str
        Sets the pen used to draw a rectangle around the text string
        (see ``clearance``) [Default is ``"0.25p,black,solid"``].
    no_clip : bool
        Do NOT clip text at map boundaries [Default is with clip].
    {timestamp}
    {verbose}
    {aspatial}
    {panel}
    {find}
    {coltypes}
    {header}
    use_word : int
        Select a specific word from the trailing text, with the first
        word being 0 [Default is the entire trailing text]. No numerical
        columns can be specified.
    {perspective}
    {transparency}
        ``transparency`` can also be a 1-D array to set varying
        transparency for texts, but this option is only valid if using
        ``x``/``y`` and ``text``.
    {wrap}
    """
    # pylint: disable=too-many-branches
    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access

    # Ensure inputs are either textfiles, x/y/text, or position/text
    if position is None:
        if (x is not None or y is not None) and textfiles is not None:
            raise GMTInvalidInput(
                "Provide either position only, or x/y pairs, or textfiles."
            )
        kind = data_kind(textfiles, x, y, text)
        if kind == "vectors" and text is None:
            raise GMTInvalidInput("Must provide text with x/y pairs")
    else:
        if x is not None or y is not None or textfiles is not None:
            raise GMTInvalidInput(
                "Provide either position only, or x/y pairs, or textfiles."
            )
        if text is None or is_nonstr_iter(text):
            raise GMTInvalidInput("Text can't be None or array.")
        kind = None
        textfiles = ""

    # Build the -F option in gmt text.
    if kwargs.get("F") is None and (
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
        kwargs["F"] += f"+c{position}+t{text}"

    extra_arrays = []
    # If an array of transparency is given, GMT will read it from
    # the last numerical column per data record.
    if kwargs.get("t") is not None and is_nonstr_iter(kwargs["t"]):
        extra_arrays.append(kwargs["t"])
        kwargs["t"] = ""

    # Append text at last column. Text must be passed in as str type.
    if kind == "vectors":
        extra_arrays.append(np.atleast_1d(text).astype(str))

    with Session() as lib:
        file_context = lib.virtualfile_from_data(
            check_kind="vector", data=textfiles, x=x, y=y, extra_arrays=extra_arrays
        )
        with file_context as fname:
            lib.call_module(module="text", args=build_arg_string(kwargs, infile=fname))
