"""
paragraph - Typeset one or multiple paragraphs.
"""

import io
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import (
    _check_encoding,
    build_arg_list,
    is_nonstr_iter,
    non_ascii_to_octal,
)

__doctest_skip__ = ["paragraph"]


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

    Examples
    --------
    >>> import pygmt
    >>>
    >>> fig = pygmt.Figure()
    >>> fig.basemap(region=[0, 10, 0, 10], projection="X10c/10c", frame=True)
    >>> fig.paragraph(
    ...     x=4,
    ...     y=4,
    ...     text="This is a long paragraph. " * 10,
    ...     parwidth="5c",
    ...     linespacing="12p",
    ...     font="12p",
    ... )
    >>> fig.show()
    """
    self._activate_figure()

    _valid_alignments = {"left", "center", "right", "justified"}
    if alignment not in _valid_alignments:
        raise GMTValueError(
            alignment,
            description="value for parameter 'alignment'",
            choices=_valid_alignments,
        )

    aliasdict = AliasSystem(
        F=[
            Alias(font, name="font", prefix="+f"),
            Alias(angle, name="angle", prefix="+a"),
            Alias(justify, name="justify", prefix="+j"),
        ]
    )
    aliasdict.merge({"M": True})

    confdict = {}
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
                    "text",
                    args=build_arg_list(aliasdict, infile=vfile, confdict=confdict),
                )
