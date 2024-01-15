"""
timestamp - Plot the GMT timestamp logo.
"""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from packaging.version import Version
from pygmt.alias import Alias, convert_aliases
from pygmt.clib import Session, __gmt_version__
from pygmt.helpers import build_arg_string, is_nonstr_iter

if TYPE_CHECKING:
    from collections.abc import Sequence


__doctest_skip__ = ["timestamp"]


def timestamp(
    self,
    text: str | None = None,
    label: str | None = None,
    justification: str = "BL",
    offset: float | str | Sequence[float | str] = ("-54p", "-54p"),
    font: str = "Helvetica,black",
    timefmt: str = "%Y %b %d %H:%M:%S",
) -> None:
    r"""
    Plot the GMT timestamp logo.

    Add the GMT timestamp logo with an optional label at the bottom-left corner of a
    plot with an offset of ``("-54p", "-54p")``. The timestamp will be in the locale set
    by the environment variable **TZ** (generally local time but can be changed via
    ``os.environ["TZ"]``) and its format is controlled by the ``timefmt`` parameter. It
    can also be replaced with any custom text string using the ``text`` parameter.

    Parameters
    ----------
    text
        If ``None``, the current UNIX timestamp is shown in the GMT timestamp logo. Set
        this parameter to replace the UNIX timestamp with a custom text string instead.
        The text must be no longer than 64 characters.
    label
        The text string shown after the GMT timestamp logo.
    justification
        Justification of the timestamp box relative to the plot's bottom-left corner
        (i.e., the plot origin). The *justification* is a two-character code that is a
        combination of a horizontal (**L**\ (eft), **C**\ (enter), or **R**\ (ight)) and
        a vertical (**T**\ (op), **M**\ (iddle), or **B**\ (ottom)) code. For example,
        ``justification="TL"`` means choosing the **T**\ op **L**\ eft point of the
        timestamp as the anchor point.
    offset
        *offset* or (*offset_x*, *offset_y*).
        Offset the anchor point of the timestamp box by *offset_x* and *offset_y*. If a
        single value *offset* is given, *offset_y* = *offset_x* = *offset*.
    font
        Font of the timestamp and the optional label. Since the GMT logo has a fixed
        height, the font sizes are fixed to be 8-point for the timestamp and 7-point for
        the label. The parameter can't change the font color for GMT<=6.4.0, only the
        font style.
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
    self._preprocess()

    # Aliases from PyGMT parameters to GMT options
    _aliases = [
        Alias("label", "U", "", ""),
        Alias("justification", "U", "+j", ""),
        Alias("offset", "U", "+o", "/"),
        Alias("text", "U", "+t", ""),
    ]

    # Giving a single offset doesn't work in GMT <= 6.4.0.
    # See https://github.com/GenericMappingTools/gmt/issues/7107.
    if (
        Version(__gmt_version__) <= Version("6.4.0")
        and not is_nonstr_iter(offset)
        and "/" not in str(offset)
    ):
        offset = (offset, offset)

    # The +t modifier was added in GMT 6.5.0.
    # See https://github.com/GenericMappingTools/gmt/pull/7127.
    if text is not None:
        if len(str(text)) > 64:
            msg = (
                "Argument of 'text' must be no longer than 64 characters. "
                "The given text string will be truncated to 64 characters."
            )
            warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
        if Version(__gmt_version__) <= Version("6.4.0"):
            # workaround for GMT<=6.4.0 by overriding the 'timefmt' parameter
            timefmt = text[:64]
            text = None  # reset 'text' to None

    # Build the options passed to the "plot" module
    options = convert_aliases()
    options["T"] = True

    with Session() as lib:
        lib.call_module(
            module="plot",
            args=build_arg_string(
                options, confdict={"FONT_LOGO": font, "FORMAT_TIME_STAMP": timefmt}
            ),
        )
