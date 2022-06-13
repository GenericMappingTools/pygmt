"""
earthtide - Compute grids or time-series of solid Earth tides.
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray

__doctest_skip__ = ["earthtide"]


@fmt_docstring
@use_alias(
    G="outgrid",
    I="spacing",
    L="location",
    R="region",
    S="sunmoon",
    T="time",
    V="verbose",
)
@kwargs_to_strings(I="sequence", L="sequence", R="sequence")
def earthtide(**kwargs):
    r"""
    Compute grids or time-series of solid Earth tides.

    Compute the three components of solid Earth tides as time-series or grids.
    Optionally compute also Sun and Moon position in lon,lat. The output can
    be either in the form of a grid or as a table printed to stdout. The
    format of the table data is: time north east vertical in units of meters.

    Full option list at :gmt-docs:`earthtide.html`

    {aliases}

    Parameters
    ----------
    sunmoon : bool
        Output position of Sun and Moon in geographical coordinates plus
        distance in meters. Output is a Mx7 matrix where M is the number of
        times (set by `time`) and columns are time, sun_lon, sun_lat, sun_dist
        moon_lon, moon_lat, moon_dist
    location : str or list
        [*lon/lat*\ ]
        Geographical coordinate of the location where to compute a
        time-series. Coordinates are geodetic (ellipsoidal) latitude and
        longitude. GRS80 ellipsoid is used. (Which can be considered
        equivalent to the WGS84 ellipsoid at the sub-millimeter level.)
    time : str
        [*min/max*\ /]\ *inc*\ [**+i**\|\ **n**] \|\ |-T|\ *file*\|\ *list*.
        Make evenly spaced time-steps from *min* to *max* by *inc*. Append
        **+i** to indicate the reciprocal increment was given, or append
        **+n** to indicate *inc* is the number of *t*-values to produce over
        the range instead. Append a valid time unit (**d**\|\ **h**\|\
        **m**\|\ **s**) to the increment. If only *min* is given then we use
        that date and time for the calculations.  If no `time`` is provided,
        get current time in UTC from the computer clock. If no `location` is
        provided then `time`` is interpreted to mean compute a time-series at
        the location specified. Dates may range from 1901 through 2099.
    {I}
    {R}
    {V}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Create a grid of Earth tide at 1200 UTC on June 18, 2018
    >>> grid = pygmt.earthtide(time="2018-06-18T12:00:00")
    """
    if kwargs.get("R") is not None and kwargs.get("I") is None:
        raise GMTInvalidInput("Must specify 'spacing' if 'region' is specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if (outgrid := kwargs.get("G")) is None:
                kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
            lib.call_module(module="earthtide", args=build_arg_string(kwargs))

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
