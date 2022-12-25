"""
binstats - Bin spatial data and determine statistics per bin
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@use_alias(
    C="statistic",
    E="empty",
    G="outgrid",
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
def binstats(data, **kwargs):
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
    data : str or {table-like}
        A file name of an ASCII data table or a 2-D
        {table-classes}.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    statistic : str
        **a**\|\ **d**\|\ **g**\|\ **i**\|\ **l**\|\ **L**\|\ **m**\|\ **n**\
        \|\ **o**\|\ **p**\|\ **q**\ [*quant*]\|\ **r**\|\ **s**\|\ **u**\
        \|\ **U**\|\ **z**.
        Choose the statistic that will be computed per node based on the
        points that are within *radius* distance of the node.  Select one of:

        - **a** for mean (average)
        - **d** for median absolute deviation (MAD)
        - **g** for full (max-min) range
        - **i** for 25-75% interquartile range
        - **l** for minimum (low)
        - **L** for minimum of positive values only
        - **m** for median
        - **n** the number of values
        - **o** for LMS scale
        - **p** for mode (maximum likelihood)
        - **q** for selected quantile (append desired quantile in
          0-100% range [50])
        - **r** for the r.m.s.
        - **s** for standard deviation
        - **u** for maximum (upper)
        - **U** for maximum of negative values only
        - **z** for the sum
    empty : float or int
        Set the value assigned to empty nodes [Default is NaN].
    normalize : bool
        Normalize the resulting grid values by the area represented by the
        search *radius* [no normalization].
    search_radius : float or str
        Sets the *search_radius* that determines which data points are
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
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="binstats", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
