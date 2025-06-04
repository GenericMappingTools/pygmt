"""
paragraph - Typeset one or multiple paragraphs.
"""

import io
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    _check_encoding,
    build_arg_list,
    is_nonstr_iter,
    non_ascii_to_octal,
)


def _parse_font_angle_justify(
    font: float | str | None, angle: float | None, justify: AnchorCode | None
) -> str | None:
    """
    Parse the font, angle, and justification arguments and return the string to be
    appended to the module options.

    Examples
    --------
    >>> _parse_font_angle_justify(None, None, None)
    >>> _parse_font_angle_justify("10p", None, None)
    '+f10p'
    >>> _parse_font_angle_justify(None, 45, None)
    '+a45'
    >>> _parse_font_angle_justify(None, None, "CM")
    '+jCM'
    >>> _parse_font_angle_justify("10p", 45, None)
    '+f10p+a45'
    >>> _parse_font_angle_justify("10p,Helvetica-Bold", 45, "CM")
    '+f10p,Helvetica-Bold+a45+jCM'
    """
    args = {"+f": font, "+a": angle, "+j": justify}
    if all(arg is None for arg in args.values()):
        return None
    return "".join(f"{prefix}{arg}" for prefix, arg in args.items() if arg is not None)


def paragraph(
    self,
    x: float | str,
    y: float | str,
    text: str | Sequence[str],
    parwidth: float | str,
    linespacing: float | str,
    font: float | str | None = None,
    angle: float | None = None,
    justify: AnchorCode | None = None,
    alignment: Literal["left", "center", "right", "justified"] = "left",
):
    """
    Typeset one or multiple paragraphs.

    Parameters
    ----------
    x/y
        The x, y coordinates of the paragraph.
    text
        The paragraph text to typeset. If a sequence of strings is provided, each string
        is treated as a separate paragraph.
    parwidth
        The width of the paragraph.
    linespacing
        The spacing between lines.
    font
        The font of the text.
    angle
        The angle of the text.
    justify
        The justification of the block of text, relative to the given x, y position.
    alignment
        The alignment of the text. Valid values are ``"left"``, ``"center"``,
        ``"right"``, and ``"justified"``.
    """
    self._preprocess()

    # Validate 'alignment' argument.
    if alignment not in {"left", "center", "right", "justified"}:
        msg = (
            "Invalid value for 'alignment': {alignment}. "
            "Valid values are 'left', 'center', 'right', and 'justified'."
        )
        raise GMTInvalidInput(msg)

    confdict = {}
    # Prepare the keyword dictionary for the module options
    kwdict = {"M": True, "F": _parse_font_angle_justify(font, angle, justify)}
    # Prepare the text string that will be passed to an io.StringIO object.
    # Multiple paragraphs are separated by a blank line "\n\n".
    _textstr: str = "\n\n".join(text) if is_nonstr_iter(text) else str(text)
    # Check the encoding of the text string and convert it to octal if necessary.
    if (encoding := _check_encoding(_textstr)) != "ascii":
        _textstr = non_ascii_to_octal(_textstr, encoding=encoding)
        confdict["PS_CHAR_ENCODING"] = encoding

    with Session() as lib:
        with io.StringIO() as buffer:  # Prepare the StringIO input.
            buffer.write(f"> {x} {y} {linespacing} {parwidth} {alignment[0]}\n")
            buffer.write(_textstr)
            with lib.virtualfile_in(data=buffer) as vfile:
                lib.call_module(
                    "text", args=build_arg_list(kwdict, infile=vfile, confdict=confdict)
                )
