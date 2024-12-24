"""
paragraph - Typeset one or multiple paragraphs.
"""

import io
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.clib import Session
from pygmt.helpers import (
    _check_encoding,
    build_arg_list,
    is_nonstr_iter,
    non_ascii_to_octal,
)


def _parse_option_f_upper(
    font: float | str | None, angle: float | None, justify: AnchorCode | None
) -> str | None:
    """
    Parse the font, angle, and justification arguments and return the string to be
    appened to the module options.

    Examples
    --------
    >>> _parse_font_angle_justify(None, None, None)
    >>> _parse_font_angle_justify("10p", None, None)
    '+f10p'
    >>> _parse_font_angle_justify(None, 45, None)
    '+a45'
    >>> _parse_font_angle_justify(None, None, "CM")
    '+jCM'
    >>> _parse_font_angle_justify("10p,Helvetica-Bold", 45, "CM")
    '+f10p,Helvetica-Bold+a45+jCM'
    """
    args = ((font, "+f"), (angle, "+a"), (justify, "+j"))
    if all(arg is None for arg, _ in args):
        return None
    return "".join(f"{flag}{arg}" for arg, flag in args if arg is not None)


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
        The paragraph text to typeset.
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

    # Initialize a stringio object for storing the data input.
    stringio = io.StringIO()
    # The header line.
    stringio.write(f"> {x} {y} {linespacing} {parwidth} {alignment[0]}\n")
    # The text. Multiple paragraphs are separated by a blank line.
    text_in_stringio = "\n\n".join(text) if is_nonstr_iter(text) else text
    encoding = _check_encoding(text_in_stringio)
    stringio.write(non_ascii_to_octal(text_in_stringio, encoding=encoding))

    confdict = {}
    if encoding not in {"ascii", "ISOLatin1+"}:
        confdict["PS_CHAR_ENCODING"] = encoding

    # Prepare the keyword dictionary for the module options
    kwdict = {"M": True, "F": _parse_option_f_upper(font, angle, justify)}

    with Session() as lib:
        with lib.virtualfile_from_stringio(stringio) as vfile:
            lib.call_module(
                "text", args=build_arg_list(kwdict, infile=vfile, confdict=confdict)
            )
