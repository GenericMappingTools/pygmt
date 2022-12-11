"""
solar - Plot day-night terminators and twilight.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_string, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["solar"]


@fmt_docstring
@use_alias(
    B="frame",
    G="fill",
    J="projection",
    R="region",
    U="timestamp",
    V="verbose",
    W="pen",
    c="panel",
    p="perspective",
    t="transparency",
)
@kwargs_to_strings(R="sequence", c="sequence_comma", p="sequence")
def solar(self, terminator="d", terminator_datetime=None, **kwargs):
    r"""
    Plot day-light terminators or twilights.

    This function plots the day-night terminator. Alternatively, it can plot
    the terminators for civil twilight, nautical twilight, or astronomical
    twilight.

    Full option list at :gmt-docs:`solar.html`

    {aliases}

    Parameters
    ----------
    terminator : str
        Set the type of terminator displayed. Valid arguments are
        **day_night**, **civil**, **nautical**, and **astronomical**, which
        can be set with either the full name or the first letter of the name
        [Default is **day_night**].

        Refer to https://en.wikipedia.org/wiki/Twilight for the definitions of
        different types of twilight.
    terminator_datetime : str or datetime object
        Set the UTC date and time of the displayed terminator
        [Default is the current UTC date and time]. It can be
        passed as a string or Python datetime object.
    {region}
    {projection}
    {frame}
    fill : str
        Color or pattern for filling of terminators.
    pen : str
        Set pen attributes for lines [Default is ``"0.25p,black,solid"``].
    {timestamp}
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
    >>> fig.coast(
    ...     land="lightgreen", water="lightblue", projection="W10c", region="d"
    ... )
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

    kwargs = self._preprocess(**kwargs)  # pylint: disable=protected-access
    if kwargs.get("T") is not None:
        raise GMTInvalidInput(
            "Use 'terminator' and 'terminator_datetime' instead of 'T'."
        )
    if terminator not in [
        "day_night",
        "civil",
        "nautical",
        "astronomical",
        "d",
        "c",
        "n",
        "a",
    ]:
        raise GMTInvalidInput(
            f"Unrecognized solar terminator type '{terminator}'. Valid values "
            "are 'day_night', 'civil', 'nautical', and 'astronomical'."
        )
    kwargs["T"] = terminator[0]
    if terminator_datetime:
        try:
            datetime_string = pd.to_datetime(terminator_datetime).strftime(
                "%Y-%m-%dT%H:%M:%S.%f"
            )
        except ValueError as verr:
            raise GMTInvalidInput("Unrecognized datetime format.") from verr
        kwargs["T"] += f"+d{datetime_string}"
    with Session() as lib:
        lib.call_module(module="solar", args=build_arg_string(kwargs))
