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
    C="compute",
    E="empty",
    G="outgrid",
    I="spacing",
    N="normalize",
    R="region",
    S="search_radius",
    T="tiling",
    V="verbose",
    W="weight",
    a="colname",
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
    (2-4 columns) from standard input [or ``data``] and for each
    node in the specified grid layout determines which points are
    within the given radius.  These point are then used in the
    calculation of the specified statistic. The results may be
    presented as is or may be normalized by the circle area to
    perhaps give density estimates.  Alternatively, select
    hexagonal tiling instead or a rectangular grid layout.

    Full option list at :gmt-docs:`gmtbinstats.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in data with L, M, C[L,M], S[L,M] values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    compute : str
        **a**\|\ **d**\|\ **g**\|\ **i**\|\ **l**\|\ **L**\|\ **m**\|\ **n**
        \|\ **o**\|\ **p**\|\ **q**\ [*quant*]\|\ **r**\|\ **s**\|\ **u**
        \|\ **U**\|\ **z**.
        Choose the statistic that will be computed per node based on the
        points that are within *radius* distance of the node.  Select one of
        **a** for mean (average), **d** for median absolute deviation (MAD),
        **g** for full (max-min) range, **i** for 25-75% interquartile range,
        **l** for minimum (low), **L** for minimum of positive values only,
        **m** for median, **n** the number of values, **o** for LMS scale,
        **p** for mode (maximum likelihood), **q** for selected quantile
        (append desired quantile in 0-100% range [50]), **r** for the r.m.s.,
        **s** for standard deviation, **u** for maximum (upper),
        **U** for maximum of negative values only, or **z** for the sum.
    {I}
    {R}
    {V}
    {b}
    {h}
    {i}
    {r}
    {x}

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
                    module="binstats", 
                    args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
