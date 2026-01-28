"""
timestamp - Plot the GMT timestamp logo.
"""

import warnings
from collections.abc import Sequence

from pygmt._typing import AnchorCode
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list

__doctest_skip__ = ["timestamp"]


def timestamp(
    self,
    text: str | None = None,
    label: str | None = None,
    justify: AnchorCode = "BL",
    offset: float | str | Sequence[float | str] = ("-54p", "-54p"),
    font: str = "Helvetica,black",
    timefmt: str = "%Y %b %d %H:%M:%S",
):
    r"""
    Plot the GMT timestamp logo.

    Add the GMT timestamp logo with an optional label at the bottom-left corner relative
    to the current plot origin, with an offset of ``("-54p", "-54p")``. The timestamp
    will be in the locale set by the environment variable :term:`TZ` (generally local
    time but can be changed via ``os.environ["TZ"]``) and its format is controlled by
    the ``timefmt`` parameter. It can also be replaced with any custom text string using
    the ``text`` parameter.

    Parameters
    ----------
    text
        If ``None``, the current UNIX timestamp is shown in the GMT timestamp logo. Set
        this parameter to replace the UNIX timestamp with a custom text string instead.
        The text must be no longer than 64 characters.
    label
        The text string shown after the GMT timestamp logo.
    justify
        Specify a :doc:`2-character justification code </techref/justification_codes>`
        for the timestamp box relative to the current plot origin. The default is the
        Bottom Left (``"BL"``) corner.
    offset
        *offset* or (*offset_x*, *offset_y*).
        Offset the anchor point of the timestamp box by *offset_x* and *offset_y*. If a
        single value *offset* is given, *offset_y* = *offset_x* = *offset*.
    font
        Font of the timestamp and the optional label. Since the GMT logo has a fixed
        height, the font sizes are fixed to be 8-point for the timestamp and 7-point for
        the label.
    timefmt
        Format string for the UNIX timestamp. The format string is parsed by the C
        function ``strftime``, so that virtually any text can be used (even not
        containing any time information).

    Examples
    --------
    Plot the GMT timestamp logo.

    >>> import pygmt
    >>> fig = pygmt.Figure()
    >>> fig.timestamp()
    >>> fig.show()

    Plot the GMT timestamp logo with a custom label.

    >>> fig = pygmt.Figure()
    >>> fig.timestamp(label="Powered by PyGMT")
    >>> fig.show()
    """
    self._activate_figure()

    if text is not None and len(str(text)) > 64:
        msg = (
            "Parameter 'text' expects a string no longer than 64 characters. "
            "The given text string will be truncated to 64 characters."
        )
        warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
        text = str(text)[:64]

    aliasdict = AliasSystem(
        U=[
            Alias(label, name="label"),
            Alias(justify, name="justify", prefix="+j"),
            Alias(offset, name="offset", prefix="+o", sep="/", size=2),
            Alias(text, name="text", prefix="+t"),
        ]
    )
    aliasdict["T"] = ""  # Add '-T' to the "plot" module.

    with Session() as lib:
        lib.call_module(
            module="plot",
            args=build_arg_list(
                aliasdict, confdict={"FONT_LOGO": font, "FORMAT_TIME_STAMP": timefmt}
            ),
        )
