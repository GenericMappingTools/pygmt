"""
binstats - Bin spatial data and determine statistics per bin.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt._typing import PathLike, TableLike
from pygmt.alias import Alias, AliasSystem
from pygmt.clib import Session
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias


@fmt_docstring
@use_alias(
    E="empty",
    I="spacing",
    N="normalize",
    S="search_radius",
    W="weight",
    a="aspatial",
    b="binary",
    h="header",
    i="incols",
    r="registration",
)
@kwargs_to_strings(I="sequence", i="sequence_comma")
def binstats(
    data: PathLike | TableLike,
    outgrid: PathLike | None = None,
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
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
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

    Full GMT docs at :gmt-docs:`gmtbinstats.html`.

    {aliases}
       - C = statistic
       - R = region
       - V = verbose

    Parameters
    ----------
    data
        A file name of an ASCII data table or a 2-D {table-classes}.
    {outgrid}
    statistic
        Choose the statistic that will be computed per node based on the points that are
        within *radius* distance of the node. Select one of:

        - ``"mean"``: Mean (i.e., average).
        - ``"mad"``: Median absolute deviation (MAD).
        - ``"full"``: The full (max-min) range.
        - ``"interquartile"``: The 25-75% interquartile range.
        - ``"min"``: Minimum (lowest value).
        - ``"minpos"``: Minimum of positive values only.
        - ``"median"``: Median value.
        - ``"number"``: The number of values per bin.
        - ``"lms"``: Least median square (LMS) scale.
        - ``"mode"``: Mode (maximum likelihood estimate).
        - ``"quantile"``: Selected quantile. The quantile value is specified by the
          ``quantile_value`` parameter and is in the 0-100% range.
        - ``"rms"``: Root mean square (RMS).
        - ``"stddev"``: Standard deviation.
        - ``"max"``: Maximum (highest value).
        - ``"maxneg"``: Maximum of negative values only.
        - ``"sum"``: The sum of the values.
    quantile_value
        The quantile value if ``statistic="quantile"``.
    empty : float
        Set the value assigned to empty nodes [Default is NaN].
    normalize : bool
        Normalize the resulting grid values by the area represented by the
        search *radius* [Default is no normalization].
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
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
          ``outgrid``)
    """
    aliasdict = AliasSystem(
        C=Alias(
            statistic,
            name="statistic",
            mapping={
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
            },
        ),
    ).add_common(
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)
    if statistic == "quantile":
        aliasdict["C"] += f"{quantile_value}"

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="vector", data=data) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            aliasdict["G"] = voutgrd
            lib.call_module(
                module="binstats", args=build_arg_list(aliasdict, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
