"""
paragraph - Typeset one or multiple paragraphs.
"""

import io
import re
from collections.abc import Sequence
from typing import Literal

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import (
    _check_encoding,
    build_arg_list,
    fmt_docstring,
    is_nonstr_iter,
    non_ascii_to_octal,
)

__doctest_skip__ = ["paragraph"]


@fmt_docstring
def paragraph(
    self,
    x: float | str,
    y: float | str,
    text: str | Sequence[str],
    parwidth: float | str,
    linespacing: float | str,
    font: str | None = None,
    angle: float | None = None,
    justify: AnchorCode | None = None,
    fill: str | None = None,
    pen: str | None = None,
    alignment: Literal["left", "center", "right", "justified"] = "left",
    tab_width: int = 4,
    blank_line: bool = False,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | Sequence[int] | bool = False,
    transparency: float | Sequence[float] | bool | None = None,
):
    r"""
    Typeset one or multiple paragraphs.

    This method typesets one or multiple paragraphs of text at a given position. The
    text is flowed within a given paragraph width and with a specified line spacing, and
    can be aligned left, center, right, or justified.

    Multiple paragraphs can be provided as a sequence of strings, where each string
    represents a separate paragraph, or as a single string with a blank line (``\n\n``)
    separating the paragraphs.

    The text string is typeset following the What You Type Is What You Get principle,
    meaning that the text is rendered exactly as it appears in the input string. This
    allows for precise control over the formatting of the text, including the use of
    multiple spaces and tabs. By default, a tab is replaced with four spaces, but this
    can be changed by setting the ``tab_width``.

    Full GMT docs at :gmt-docs:`text.html`.

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
        Set the alignment of the block of text, relative to the given x, y position.
        Choose a :doc:`2-character justification code </techref/justification_codes>`.
    alignment
        Set the alignment of the text. Valid values are ``"left"``, ``"center"``,
        ``"right"``, and ``"justified"``.
    fill
        Set color for filling the paragraph box [Default is no fill].
    pen
        Set the pen for the paragraph box [Default is ``"0.25p,black,solid"``].
    tab_width
        Number of spaces used to expand tab characters in ``text`` when typesetting.
        Must be a non-negative integer. Use ``0`` to remove tab characters instead of
        replacing them with spaces.
    blank_line
        If ``True``, use a blank line between paragraphs. [Default is ``False``, i.e.,
        no blank line between paragraphs.]
    $verbose
    $panel
    $transparency

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

    _valid_alignments = ("left", "center", "right", "justified")
    if alignment not in _valid_alignments:
        raise GMTValueError(
            alignment,
            description="value for parameter 'alignment'",
            choices=_valid_alignments,
        )
    if tab_width < 0:
        raise GMTValueError(
            tab_width,
            description="value for parameter 'tab_width'",
            reason="Must be a non-negative integer.",
        )

    aliasdict = AliasSystem(
        F=[
            Alias(font, name="font", prefix="+f"),
            Alias(angle, name="angle", prefix="+a"),
            Alias(justify, name="justify", prefix="+j"),
        ],
        G=Alias(fill, name="fill"),
        W=Alias(pen, name="pen"),
    ).add_common(
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge({"M": True})

    # Prepare the text string that will be passed to an io.StringIO object.
    # Separator for multiple paragraphs.
    # "\n\n": the default separator, which results in no blank line between paragraphs.
    # " \n\n": add a blank line between paragraphs.
    sep = " \n\n" if blank_line else "\n\n"
    # Convert a single string into a list of paragraphs for consistent handling.
    # Split the single string on blank lines, allowing for whitespaces in between.
    if not is_nonstr_iter(text):
        text = re.split(r"\n\s*\n", text)  # type: ignore[arg-type]
    # Join multiple paragraphs with a blank line. Remove trailing whitespaces and
    # newlines in each paragraph, but keep leading whitespaces and tabs for now.
    # _textstr = sep.join(t.rstrip().replace("\n", "") for t in text)
    _textstr = sep.join(t.rstrip().replace("\n", "") for t in text)
    # Replace two or more consecutive spaces with \040 (octal for space), and replace
    # tabs with the appropriate number of \040.
    _textstr = re.sub(r" {2,}", lambda m: r"\040" * len(m.group()), _textstr)
    _textstr = _textstr.replace("\t", r"\040" * tab_width)
    if _textstr == "":
        raise GMTValueError(
            text,
            description="text",
            reason="'text' must be a non-empty string or sequence of strings.",
        )

    confdict = {}
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
