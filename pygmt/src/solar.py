"""
solar - Plot day-night terminators.
"""

import datetime

import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    R="region",
    J="projection",
    G="fill",
    B="frame",
    W="pen",
    U="timestamp",
    V="verbose",
    X="xshift",
    Y="yshift",
    p="perspective",
)
@kwargs_to_strings(R="sequence", p="sequence")
def solar(self, terminator="d", terminator_datetime="", **kwargs):
    r"""
    Plot day-light terminators.

    This function plots the day-night terminator. Additionally, it can
    plot the terminators for civil twilight, nautical twilight, and
    astronomical twilight.

    {aliases}

    Parameters
    ----------
    terminator : str
        Set the type of terminator displayed. The parameters are
        ``day_night``, ``civil``, ``nautical``, and ``astronomical``, which
        can be set with either the full name or the first letter of the name.
        [Default is ``day_night``]
    terminator_datetime : str or datetime object
        Set the UTC date and time of the displayed terminator. It can be
        passed as a string, using the format *YYYY-MM-DD HH:MM:SS*
        (e.g. 0600 on January 1, 2000 would be ``2000-01-01 06:00:00``). A
        datetime object can be passed as well.
        [Default is the current date and time]
    {R}
    {J}
    {B}
    fill : str
        Color or pattern for filling of terminators.
    pen : str
        Set pen attributes for lines. The default pen
        is ``default,black,solid``.
    {XY}
    {p}
    {U}
    {V}
    """

    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    if "T" not in kwargs:
        if terminator not in [
            "day_night",
            "nautical",
            "civil",
            "astronomical",
            "astro",
            "d",
            "n",
            "c",
            "a",
        ]:
            print(kwargs)
            raise GMTInvalidInput("""Unrecognized solar terminator type.""")
        term_string = terminator[0]
        if not terminator_datetime:
            terminator_datetime = datetime.datetime.now()
        try:
            terminator_timestamp = pd.to_datetime(terminator_datetime)
            datetime_string = terminator_timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise GMTInvalidInput("""Unrecognized datetime format.""")
        kwargs["T"] = term_string + "+d" + datetime_string
    with Session() as lib:
        lib.call_module("solar", build_arg_string(kwargs))
