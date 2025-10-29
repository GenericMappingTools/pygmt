"""
solar - Plot day-night terminators and other sunlight parameters.
"""

from collections.abc import Sequence
from typing import Literal

import pandas as pd
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["solar"]


@fmt_docstring
@use_alias(B="frame", p="perspective")
@kwargs_to_strings(p="sequence")
def solar(
    self,
    terminator: Literal["astronomical", "civil", "day_night", "nautical"] = "day_night",
    terminator_datetime=None,
    fill: str | None = None,
    pen: str | None = None,
    projection: str | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    panel: int | tuple[int, int] | bool = False,
    transparency: float | None = None,
    **kwargs,
):
    r"""
    Plot day-night terminators and other sunlight parameters.

    This method plots the day-night terminator. Alternatively, it can plot the
    terminators for civil twilight, nautical twilight, or astronomical twilight.

    Full GMT docs at :gmt-docs:`solar.html`.

    {aliases}
       - G = fill
       - J = projection
       - R = region
       - T = terminator, **+d**/**+z**: terminator_datetime
       - V = verbose
       - W = pen
       - c = panel
       - t = transparency

    Parameters
    ----------
    terminator
        Set the type of terminator. Choose one of the following:

        - ``"astronomical"``: Astronomical twilight
        - ``"civil"``: Civil twilight
        - ``"day_night"``: Day-night terminator
        - ``"nautical"``: Nautical twilight

        Refer to https://en.wikipedia.org/wiki/Twilight for the definitions of different
        types of twilight.
    terminator_datetime : str or datetime object
        Set the date and time for the terminator calculation. It can be provided as a
        string or any datetime-like object recognized by :func:`pandas.to_datetime`. The
        time can be specified in UTC or using a UTC offset. The offset must be an
        integer number of hours (e.g., -8 or +5); fractional hours are truncated
        towards zero (e.g., -8.5 becomes -8 and +5.5 becomes +5). [Default is the
        current UTC date and time].
    {region}
    {projection}
    {frame}
    fill
        Set color or pattern for filling terminators [Default is no fill].
    pen
        Set pen attributes for lines [Default is ``"0.25p,black,solid"``].
    {verbose}
    {panel}
    {perspective}
    {transparency}

    Example
    -------
    >>> # import the Python module "datetime"
    >>> import datetime
    >>> import pygmt
    >>> # create a datetime object at 8:52:18 on June 24, 1997 (time in UTC)
    >>> date = datetime.datetime(
    ...     year=1997, month=6, day=24, hour=8, minute=52, second=18
    ... )
    >>> # create a new plot with pygmt.Figure()
    >>> fig = pygmt.Figure()
    >>> # create a map of the Earth with the coast method
    >>> fig.coast(land="darkgreen", water="lightblue", projection="W10c", region="d")
    >>> fig.solar(
    ...     # set the terminator to "day_night"
    ...     terminator="day_night",
    ...     # pass the datetime object
    ...     terminator_datetime=date,
    ...     # fill the night-section with navyblue at 75% transparency
    ...     fill="navyblue@75",
    ...     # draw the terminator with a 1-point black line
    ...     pen="1p,black",
    ... )
    >>> # show the plot
    >>> fig.show()
    """
    self._activate_figure()

    datetime_string, datetime_timezone = None, None
    if terminator_datetime:
        try:
            _datetime = pd.to_datetime(terminator_datetime)
            datetime_string = _datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
            # GMT's solar module uses the C 'atoi' function to parse the timezone
            # offset. Ensure the offset is an integer number of hours (e.g., -8 or +5).
            # Fractional hours (e.g., -8.5 or +5.5) are truncated towards zero.
            if utcoffset := _datetime.utcoffset():
                datetime_timezone = int(utcoffset.total_seconds() / 3600)
        except ValueError as verr:
            raise GMTValueError(terminator_datetime, description="datetime") from verr

    aliasdict = AliasSystem(
        G=Alias(fill, name="fill"),
        T=[
            Alias(
                terminator,
                name="terminator",
                mapping={
                    "day_night": "d",
                    "civil": "c",
                    "nautical": "n",
                    "astronomical": "a",
                },
            ),
            Alias(datetime_string, name="terminator_datetime", prefix="+d"),
            Alias(datetime_timezone, name="terminator_timezone", prefix="+z"),
        ],
        W=Alias(pen, name="pen"),
    ).add_common(
        J=projection,
        R=region,
        V=verbose,
        c=panel,
        t=transparency,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        lib.call_module(module="solar", args=build_arg_list(aliasdict))
