"""
solar - Plot day-night terminators.
"""

from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_string,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    G="fill",
    B="frame",
    Td="day_night",
    Tc="civil_twilight",
    Tn="nautical_twilight",
    Ta="astronomical_twilight",
    W="pen",
    U="timestamp",
    V="verbose",
    X="xshift",
    Y="yshift",
    p="perspective",
)
@kwargs_to_strings(R="sequence", p="sequence")
def solar(self, **kwargs):
    r"""
    A plotting function the day-night terminator. Additionally, it can
    plot the terminators for civil twilight, nautical twilight, and
    astronomical twilight.

    {aliases}

    Parameters
    ----------
    {R}
    {J}
    {B}
    fill : str
        *fill color*\ [**@**\ *transparency*]
        The fill color for the night-area plotted. The optional
        transparency parameter can be appended after the color
        using **@** after the color.
    day_night : bool or str
        [**+d**\ *date*\ ]
        Plots the day/night terminator. If the argument is ``True``, the
        current day-night terminator is plotted. Optionally, **+d** can be
        added, along with the date and time, to see the day/night
        terminator at a specific time. The date is added in ISO format,
        e.g. 12:15 UTC on April 25, 2000 is ``2000-04-25T12:15:00``.
    civil_twilight" : bool or str
        [**+d**\ *date*\ ]
        Plots the civil twilight terminator. If the argument is
        ``True``, the current civil twilight terminator is plotted.
        Optionally, **+d** can be added, along with the date and time, to
        see the day/night terminator at a specific time. The date is added
        in ISO format,
        e.g. 12:15 UTC on April 25, 2000 is ``2000-04-25T12:15:00``.
    nautical_twilight : bool or str
        [**+d**\ *date*\ ]
        Plots the nautical twilight terminator. If the argument is
        ``True``, the current nautical twilight terminator is plotted.
        Optionally, **+d** can be added, along with the date and time, to
        see the day/night terminator at a specific time. The date is added
        in ISO format,
        e.g. 12:15 UTC on April 25, 2000 is ``2000-04-25T12:15:00``.
    astronomical_twilight : bool or str
        [**+d**\ *date*\ ]
        Plots the astronomical twilight terminator. If the argument is
        ``True``, the current astronomical twilight terminator is
        plotted. Optionally, **+d** can be added, along with the date and
        time, to see the day/night terminator at a specific time. The date
        is added in ISO format,
        e.g. 12:15 UTC on April 25, 2000 is ``2000-04-25T12:15:00``.
    pen : str
        Set pen attributes for lines or the outline of symbols
        [Defaults: width = default, color = black, style = solid].
    {XY}
    {p}
    {U}
    {V}
    """
    kwargs = self._preprocess(**kwargs)
    with Session() as lib:
        lib.call_module("solar", build_arg_string(kwargs))
