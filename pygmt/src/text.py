"""
text - Plot or typeset text.
"""

from collections.abc import Sequence
from typing import Literal

import numpy as np
from pygmt._typing import AnchorCode, PathLike, StringArrayTypes, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput, GMTTypeError
from pygmt.helpers import (
    _check_encoding,
    build_arg_list,
    data_kind,
    fmt_docstring,
    is_nonstr_iter,
    kwargs_to_strings,
    non_ascii_to_octal,
    use_alias,
)


@fmt_docstring
@use_alias(
    B="frame",
    C="clearance",
    D="offset",
    G="fill",
    W="pen",
    a="aspatial",
    e="find",
    f="coltypes",
    h="header",
    it="use_word",
    p="perspective",
    w="wrap",
)
@kwargs_to_strings(p="sequence")
def text_(  # noqa: PLR0912, PLR0913, PLR0915
    self,
    textfiles: PathLike | TableLike | None = None,
    x=None,
    y=None,
    position: AnchorCode | None = None,
    text: str | StringArrayTypes | None = None,
    angle=None,
    font=None,
    justify: bool | None | AnchorCode | Sequence[AnchorCode] = None,
    no_clip: bool = False,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | Sequence[float] | bool | None = None,
    **kwargs,
):
    r"""
    Plot or typeset text.

    Must provide at least one of the following combinations as input:

    - ``textfiles``
    - ``x``/``y``, and ``text``
    - ``position`` and ``text``

    The text strings passed via the ``text`` parameter can contain ASCII characters and
    non-ASCII characters defined in the Adobe ISOLatin1+, Adobe Symbol, Adobe
    ZapfDingbats and ISO-8859-x (x can be 1-11, 13-16) encodings. Refer to
    :doc:`/techref/encodings` for the full list of supported non-ASCII characters.

    Full GMT docs at :gmt-docs:`text.html`.

    {aliases}
       - F = **+a**: angle, **+c**: position, **+j**: justify, **+f**: font
       - J = projection
       - N = no_clip
       - R = region
       - V = verbose
       - c = panel
       - t = transparency

    Parameters
    ----------
    textfiles : str or list
        A file name or a list of file names containing one or more records.
        Each record has the following columns:

        * *x*: X coordinate or longitude
        * *y*: Y coordinate or latitude
        * *angle*: Angle in degrees counter-clockwise from horizontal
        * *font*: Text size, font, and color
        * *justify*:
          :doc:`2-character justification code </techref/justification_codes>`
        * *text*: The text string to typeset

        The *angle*, *font*, and *justify* columns are optional and can be set
        by using the ``angle``, ``font``, and ``justify`` parameters,
        respectively. If these parameters are set to ``True``, then the
        corresponding columns must be present in the input file(s) and the
        columns must be in the order mentioned above.
    x/y : float or 1-D arrays
        The x and y coordinates, or an array of x and y coordinates to plot
        the text.
    position
        Set reference point on the map for the text by using x, y
        coordinates extracted from ``region`` instead of providing them
        through ``x``/``y``. Specify with a
        :doc:`2-character justification code </techref/justification_codes>`.
        For example, ``position="TL"`` plots the text at the Top Left corner
        of the map.
    text
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
    justify
        Set the alignment which refers to the part of the text string that
        will be mapped onto the (x, y) point. Choose a
        :doc:`2-character justification code </techref/justification_codes>`,
        e.g., **BL** for Bottom Left. If no justification is explicitly given
        (i.e. ``justify=True``), then the input to ``textfiles`` must have
        this as a column.
    {projection}
    {region}
        *Required if this is the first plot command.*
    clearance : str
        [*dx/dy*][**+to**\|\ **O**\|\ **c**\|\ **C**].
        Adjust the clearance between the text and the surrounding box
        [Default is 15% of the font size]. Only used if ``pen`` or ``fill``
        are specified. Append the unit you want (**c** for centimeters,
        **i** for inches, or **p** for points; if not given we consult
        :gmt-term:`PROJ_LENGTH_UNIT`) or *%* for a percentage of the font
        size. Optionally, use modifier **+t** to set the shape of the text
        box when using ``fill`` and/or ``pen``. Append lowercase **o**
        to get a straight rectangle [Default is **o**]. Append uppercase
        **O** to get a rounded rectangle. In paragraph mode (*paragraph*)
        you can also append lowercase **c** to get a concave rectangle or
        append uppercase **C** to get a convex rectangle.
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
    no_clip
        Do **not** clip text at the frame boundaries [Default is ``False``].
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
        ``transparency`` can also be a 1-D array to set varying transparency for texts,
        but this option is only valid if using ``x``/``y`` and ``text``.
    {wrap}
    """
    self._activate_figure()

    # Ensure inputs are either textfiles, x/y/text, or position/text
    if (
        (textfiles is not None)
        + (position is not None)
        + (x is not None or y is not None)
    ) != 1:
        msg = "Provide either 'textfiles', 'x'/'y'/'text', or 'position'/'text'."
        raise GMTInvalidInput(msg)

    data_is_required = position is None
    kind = data_kind(textfiles, required=data_is_required)

    if position is not None:
        if text is None:
            msg = "'text' can't be None when 'position' is given."
            raise GMTInvalidInput(msg)
        if is_nonstr_iter(text):
            raise GMTTypeError(
                type(text),
                reason="Parameter 'text' can't be a sequence when 'position' is given.",
            )

    if textfiles is not None and text is not None:
        msg = "'text' can't be specified when 'textfiles' is given."
        raise GMTInvalidInput(msg)
    if kind == "empty" and text is None:
        msg = "Must provide text with x/y pairs."
        raise GMTInvalidInput(msg)

    # Arguments that can accept arrays.
    array_args = [
        (angle, "+a", "angle"),
        (font, "+f", "font"),
        (justify, "+j", "justify"),
    ]

    # Build the -F option.
    if kwargs.get("F") is None and any(
        v is not None for v in (position, angle, font, justify)
    ):
        kwargs.update({"F": ""})

    for arg, flag, _ in array_args:
        if arg is True:
            kwargs["F"] += flag
        elif isinstance(arg, int | float | str):
            kwargs["F"] += f"{flag}{arg}"

    confdict = {}
    data = None
    if kind == "empty":
        data = {"x": x, "y": y}

        for arg, flag, name in array_args:
            if is_nonstr_iter(arg):
                kwargs["F"] += flag
                # angle is numeric type and font/justify are str type.
                if name == "angle":
                    data["angle"] = arg
                else:
                    data[name] = np.asarray(arg, dtype=np.str_)

        # If an array of transparency is given, GMT will read it from the last numerical
        # column per data record.
        if is_nonstr_iter(transparency):
            data["transparency"] = transparency
            transparency = True

        # Append text to the last column. Text must be passed in as str type.
        text = np.asarray(text, dtype=np.str_)
        if (encoding := _check_encoding("".join(text.flatten()))) != "ascii":
            text = np.vectorize(non_ascii_to_octal, excluded="encoding")(
                text, encoding=encoding
            )
            confdict["PS_CHAR_ENCODING"] = encoding
        data["text"] = text
    else:
        if isinstance(position, str):
            kwargs["F"] += f"+c{position}+t{text}"

        for arg, _, name in [*array_args, (transparency, "", "transparency")]:
            if is_nonstr_iter(arg):
                raise GMTTypeError(
                    type(arg),
                    reason=f"Parameter {name!r} expects a single value or True.",
                )

    aliasdict = AliasSystem(
        N=Alias(no_clip, name="no_clip"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with lib.virtualfile_in(
            check_kind="vector", data=textfiles or data, required=data_is_required
        ) as vintbl:
            lib.call_module(
                module="text",
                args=build_arg_list(aliasdict, infile=vintbl, confdict=confdict),
            )
