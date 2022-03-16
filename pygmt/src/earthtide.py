"""
earthtide - Compute grids or time-series of solid Earth tides.
"""
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    args_in_kwargs,
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
    if "R" in kwargs and "I" not in kwargs:
        raise GMTInvalidInput("Must specify 'spacing' if 'region' is specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            if "G" not in kwargs:  # if outgrid is unset, output to tempfile
                kwargs.update({"G": tmpfile.name})
            outgrid = kwargs["G"]
            arg_str = build_arg_string(kwargs)
            lib.call_module("earthtide", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
