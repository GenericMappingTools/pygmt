"""
solar - Plot day-night terminators and other sunlight parameters.
"""

from typing import Literal

import pandas as pd
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput, GMTValueError
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["solar"]


@fmt_docstring
@use_alias(
    B="frame",
    G="fill",
    R="region",
    T="terminator/terminator_datetime-",
    V="verbose",
    W="pen",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def solar(
    self,
    terminator: Literal["astronomical", "civil", "day_night", "nautical"] = "day_night",
    terminator_datetime=None,
    projection=None,
    **kwargs,
):
    r"""
    Plot day-night terminators and other sunlight parameters.

    This function plots the day-night terminator. Alternatively, it can plot the
    terminators for civil twilight, nautical twilight, or astronomical twilight.

    Full GMT docs at :gmt-docs:`solar.html`.

    {aliases}
       - J=projection

    Parameters
    ----------
    terminator
        Set the type of terminator displayed, which can be set with either the full name
        or the first letter of the name. Available options are:

        - ``"astronomical"``: Astronomical twilight
        - ``"civil"``: Civil twilight
        - ``"day_night"``: Day-night terminator
        - ``"nautical"``: Nautical twilight

        Refer to https://en.wikipedia.org/wiki/Twilight for the definitions of different
        types of twilight.
    terminator_datetime : str or datetime object
        Set the UTC date and time of the displayed terminator [Default is the current
        UTC date and time]. It can be passed as a string or Python datetime object.
    {region}
    {projection}
    {frame}
    fill : str
        Set color or pattern for filling terminators [Default is no fill].
    pen : str
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
    if kwargs.get("T") is not None:
        msg = "Use 'terminator' and 'terminator_datetime' instead of 'T'."
        raise GMTInvalidInput(msg)

    valid_terminators = ["day_night", "civil", "nautical", "astronomical"]
    if terminator not in valid_terminators and terminator not in "dcna":
        raise GMTValueError(
            terminator, description="solar terminator type", choices=valid_terminators
        )
    kwargs["T"] = terminator[0]
    if terminator_datetime:
        try:
            datetime_string = pd.to_datetime(terminator_datetime).strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )
        except ValueError as verr:
            msg = "Unrecognized datetime format."
            raise GMTInvalidInput(msg) from verr
        kwargs["T"] += f"+d{datetime_string}"

    aliasdict = AliasSystem(
        J=Alias(projection, name="projection"),
    ).merge(kwargs)

    with Session() as lib:
        lib.call_module(module="solar", args=build_arg_list(aliasdict))
