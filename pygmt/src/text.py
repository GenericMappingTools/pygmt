"""
text - Plot text on a figure.
"""
import numpy as np
from pygmt.alias import Alias, convert_aliases
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_string,
    data_kind,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    non_ascii_to_octal,
)


@fmt_docstring
@kwargs_to_strings(textfiles="sequence_space")
def text_(  # noqa: PLR0913
    self,
    textfiles=None,
    x=None,
    y=None,
    position=None,
    text=None,
    angle=None,
    font=None,
    justify=None,
    projection=None,  # noqa: ARG001
    region=None,  # noqa: ARG001
    transparency=None,
    **kwargs,
):
    r"""
    Plot or typeset text strings of variable size, font type, and orientation.

    Must provide at least one of the following combinations as input:

    - ``textfiles``
    - ``x``/``y``, and ``text``
    - ``position`` and ``text``

    The text strings passed via the ``text`` parameter can contain ASCII
    characters and non-ASCII characters defined in the ISOLatin1+ encoding
    (i.e., IEC_8859-1), and the Symbol and ZapfDingbats character sets.
    See :gmt-docs:`reference/octal-codes.html` for the full list of supported
    non-ASCII characters.

    Full option list at :gmt-docs:`text.html`

    Parameters
    ----------
    textfiles : str or list
        A file name or a list of file names containing one or more records.
        Each record has the following columns:

        * *x*: X coordinate or longitude
        * *y*: Y coordinate or latitude
        * *angle*: Angle in degrees counter-clockwise from horizontal
        * *font*: Text size, font, and color
        * *justify*: Two-character justification code
        * *text*: The text string to typeset

        The *angle*, *font*, and *justify* columns are optional and can be set
        by using the ``angle``, ``font``, and ``justify`` parameters,
        respectively. If these parameters are set to ``True``, then the
        corresponding columns must be present in the input file(s) and the
        columns must be in the order mentioned above.
    x/y : float or 1-D arrays
        The x and y coordinates, or an array of x and y coordinates to plot
        the text.
    position : str
        Set reference point on the map for the text by using x, y
        coordinates extracted from ``region`` instead of providing them
        through ``x``/``y``. Specify with a two-letter (order independent)
        code, chosen from:

        * Horizontal: **L**\ (eft), **C**\ (entre), **R**\ (ight)
        * Vertical: **T**\ (op), **M**\ (iddle), **B**\ (ottom)

        For example, ``position="TL"`` plots the text at the Top Left corner
        of the map.
    text : str or 1-D array
        The text string, or an array of strings to plot on the figure.
    angle: float, str, bool or list
        Set the angle measured in degrees counter-clockwise from
        horizontal (e.g. 30 sets the text at 30 degrees). If no angle is
        explicitly given (i.e. ``angle=True``) then the input to ``textfiles``
        must have this as a column.
    font : str, bool or list of str
        Set the font specification with format *size*\ ,\ *font*\ ,\ *color*
        where *size* is text size in points, *font* is the font to use, and
        *color* sets the font color. For example,
        ``font="12p,Helvetica-Bold,red"`` selects a 12p, red, Helvetica-Bold
        font. If no font info is explicitly given (i.e. ``font=True``), then
        the input to ``textfiles`` must have this information in one of its
        columns.
    justify : str, bool or list of str
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
        [Default is 15% of the font size]. Only used if ``pen`` or ``fill``
        are specified. Append the unit you want (*c* for centimeters,
        *i* for inches, or *p* for points; if not given we consult
        :gmt-term:`PROJ_LENGTH_UNIT`) or *%* for a percentage of the font
        size. Optionally, use modifier **+t** to set the shape of the text
        box when using ``fill`` and/or ``pen``. Append lower case **o**
        to get a straight rectangle [Default is **o**]. Append upper case
        **O** to get a rounded rectangle. In paragraph mode (*paragraph*)
        you can also append lower case **c** to get a concave rectangle or
        append upper case **C** to get a convex rectangle.
    fill : str
        Set color for filling text boxes [Default is no fill].
    offset : str
        [**j**\|\ **J**]\ *dx*\[/*dy*][**+v**\[*pen*]].
        Offset the text from the projected (x, y) point by *dx*/\ *dy*
        [Default is ``"0/0"``].
        If *dy* is not specified then it is set equal to *dx*. Use **j** to
        offset the text away from the point instead (i.e., the text
        justification will determine the direction of the shift). Using
        **J** will shorten diagonal offsets at corners by sqrt(2).
        Optionally, append **+v** which will draw a line from the original
        point to the shifted point; append a pen to change the attributes
        for this line.
    pen : str
        Set the pen used to draw a rectangle around the text string
        (see ``clearance``) [Default is ``"0.25p,black,solid"``].
    no_clip : bool
        Do **not** clip text at the frame boundaries [Default is
        ``False``].
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
    kwargs = self._preprocess(**kwargs)

    _aliases = [
        Alias("position", "F", "+c", ""),
        Alias("angle", "F", "+a", ""),
        Alias("font", "F", "+f", ""),
        Alias("justify", "F", "+j", ""),
        Alias("region", "R", "", "/"),
        Alias("projection", "J", "", ""),
        Alias("transparency", "t", "", ""),
        Alias("frame", "B", "", ""),
        Alias("clearance", "C", "", ""),
        Alias("offset", "D", "", ""),
        Alias("fill", "G", "", ""),
        Alias("no_clip", "N", "", ""),
        Alias("verbose", "V", "", ""),
        Alias("pen", "W", "", ""),
        Alias("aspatial", "a", "", ""),
        Alias("panel", "c", "", ","),
        Alias("find", "e", "", ""),
        Alias("coltypes", "f", "", ""),
        Alias("header", "h", "", ""),
        Alias("use_word", "it", "", ""),
        Alias("perspective", "p", "", "/"),
        Alias("wrap", "w", "", ""),
    ]

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
        if any(v is not None for v in (x, y, textfiles)):
            raise GMTInvalidInput(
                "Provide either position only, or x/y pairs, or textfiles."
            )
        if text is None or is_nonstr_iter(text):
            raise GMTInvalidInput("Text can't be None or array.")
        kind = None
        textfiles = ""

    # special handling with the position parameter
    if position is not None:
        position += f"+t{text}"

    extra_arrays = []
    # angle is numeric type
    if is_nonstr_iter(angle):
        extra_arrays.append(np.atleast_1d(angle))
    # font or justify is str type
    for arg in (font, justify):
        if is_nonstr_iter(arg):
            extra_arrays.append(np.atleast_1d(arg).astype(str))  # noqa: PERF401
    # If an array of transparency is given, GMT will read it from
    # the last numerical column per data record.
    if is_nonstr_iter(transparency):
        extra_arrays.append(transparency)

    # Append text at last column. Text must be passed in as str type.
    if kind == "vectors":
        extra_arrays.append(
            np.vectorize(non_ascii_to_octal)(np.atleast_1d(text).astype(str))
        )

    with Session() as lib:
        file_context = lib.virtualfile_from_data(
            check_kind="vector", data=textfiles, x=x, y=y, extra_arrays=extra_arrays
        )
        options = convert_aliases()
        with file_context as fname:
            lib.call_module(module="text", args=build_arg_string(options, infile=fname))
