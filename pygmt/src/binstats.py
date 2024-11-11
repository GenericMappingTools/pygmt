"""
binstats - Bin spatial data and determine statistics per bin
"""

from typing import Literal

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    E="empty",
    I="spacing",
    N="normalize",
    R="region",
    S="search_radius",
    V="verbose",
    W="weight",
    a="aspatial",
    b="binary",
    h="header",
    i="incols",
    r="registration",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma")
def binstats(
    data,
    outgrid: str | None = None,
    statistic: Literal[
        "mean",
        "mad",
        "full",
        "interquartile",
        "min",
        "minpos",
        "median",
        "number",
        "lms",
        "mode",
        "quantile",
        "rms",
        "stddev",
        "max",
        "maxneg",
        "sum",
    ] = "number",
    quantile_value: float = 50,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Bin spatial data and determine statistics per bin.

    Reads arbitrarily located (x,y[,z][,w]) points
    (2-4 columns) from ``data`` and for each
    node in the specified grid layout determines which points are
    within the given radius. These points are then used in the
    calculation of the specified statistic. The results may be
    presented as is or may be normalized by the circle area to
    perhaps give density estimates.

    Full option list at :gmt-docs:`gmtbinstats.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        A file name of an ASCII data table or a 2-D
        {table-classes}.
    {outgrid}
    statistic
        Choose the statistic that will be computed per node based on the points that are
        within *radius* distance of the node. Select one of:

        - **mean**: Compute the mean value (average).
        - **mad**: Compute the median absolute deviation (MAD).
        - **full**: Compute the full (max-min) range.
        - **interquartile**: Compute the 25-75% interquartile range.
        - **min**: Compute the minimum value.
        - **minpos**: Compute the minimum of positive values only.
        - **median**: Compute the median value.
        - **number**: Compute the number of values.
        - **lms**: Compute the LMS scale.
        - **mode**: Compute the mode (maximum likelihood).
        - **quantile**: Compute the selected quantile. The quantile value is in 0-100%
          range and is specified by the ``quantile_value`` parameter.
        - **rms**: Compute the root mean square (RMS).
        - **stddev**: Compute the standard deviation.
        - **max**: Compute the maximum value.
        - **maxneg**: Compute the maximum of negative values only.
        - **sum**: Compute the sum of values.
    quantile_value
        The quantile value if ``statistic="quantile"``.
    empty : float
        Set the value assigned to empty nodes [Default is NaN].
    normalize : bool
        Normalize the resulting grid values by the area represented by the
        search *radius* [no normalization].
    search_radius : float or str
        Set the *search_radius* that determines which data points are
        considered close to a node. Append the distance unit.
        Not compatible with ``tiling``.
    weight : str
        Input data have an extra column containing observation point weight.
        If weights are given then weighted statistical quantities will be
        computed while the count will be the sum of the weights instead of
        number of points. If the weights are actually uncertainties
        (one sigma) then append **+s** and weight = 1/sigma.
    {spacing}
    {region}
    {verbose}
    {aspatial}
    {binary}
    {header}
    {incols}
    {registration}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    # The 'statistic' parameter is alised to the C option.
    lookup_statistic = {
        "mean": "a",
        "mad": "d",
        "full": "g",
        "interquartile": "i",
        "min": "l",
        "minpos": "L",
        "median": "m",
        "number": "n",
        "lms": "o",
        "mode": "p",
        "quantile": "q",
        "rms": "r",
        "stddev": "s",
        "max": "u",
        "maxneg": "U",
        "sum": "z",
    }
    if statistic not in {*lookup_statistic.keys(), *lookup_statistic.values()}:
        raise GMTInvalidInput(f"Unknown 'statistic' method: {statistic}.")
    kwargs["C"] = lookup_statistic.get(statistic, statistic)
    if statistic == "quantile":
        kwargs["C"] += f"{quantile_value}"

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="binstats", args=build_arg_list(kwargs, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
