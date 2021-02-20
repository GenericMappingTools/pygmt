"""
solar - Plot day-night terminators.
"""

import datetime

import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    args_in_kwargs,
    build_arg_string,
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

    kwargs = self._preprocess(**kwargs)
    if "T" not in kwargs:
        term_string = get_terminator_type(terminator=terminator)
        if not terminator_datetime:
            terminator_datetime = datetime.datetime.now()
        datetime_string = get_datetime_string(terminator_datetime=terminator_datetime)
        kwargs["T"] = term_string + "+d" + datetime_string
    print(kwargs["T"])
    with Session() as lib:
        lib.call_module("solar", build_arg_string(kwargs))


def get_terminator_type(terminator):
    if terminator in ["day_night", "d"]:
        return "d"
    elif terminator in ["nautical", "n"]:
        return "n"
    elif terminator in ["civil", "c"]:
        return "c"
    elif terminator in ["astro", "a", "astronomical"]:
        return "a"
    else:
        raise GMTInvalidInput("""Unrecognized solar terminator type.""")


def get_datetime_string(terminator_datetime):
    if type(terminator_datetime) == datetime.datetime:
        return terminator_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    elif type(terminator_datetime) == str:
        try:
            terminator_timestamp = pd.to_datetime(terminator_datetime)
            return terminator_timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise GMTInvalidInput("""Unrecognized datetime string format.""")
    else:
        raise GMTInvalidInput(
            """Accepted types for terminator_datetime are string and datetime object."""
        )
