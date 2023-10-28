"""
blockm - Block average (x, y, z) data tables by mean, median, or mode
estimation.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.helpers import (
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    return_table,
    use_alias,
    validate_output_type,
)

__doctest_skip__ = ["blockmean", "blockmedian", "blockmode"]


def _blockm(block_method, data, x, y, z, output_type, outfile, **kwargs):
    r"""
    Block average (x, y, z) data tables by mean, median, or mode estimation.

    Reads arbitrarily located (x, y, z) triplets [or optionally weighted
    quadruplets (x, y, z, w)] from a table and writes to the output a mean,
    median, or mode (depending on ``block_method``) position and value for
    every non-empty block in a grid region defined by the ``region`` and
    ``spacing`` parameters.

    Parameters
    ----------
    block_method : str
        Name of the GMT module to call. Must be "blockmean", "blockmedian" or
        "blockmode".

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``)
    """
    output_type = validate_output_type(output_type, outfile=outfile)

    with Session() as lib:
        with lib.virtualfile_from_data(
            check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
        ) as vintbl, lib.virtualfile_to_data(kind="dataset", fname=outfile) as vouttbl:
            lib.call_module(
                module=block_method,
                args=build_arg_string(kwargs, infile=vintbl, outfile=vouttbl),
            )

        column_names = (
            data.columns.to_list() if isinstance(data, pd.DataFrame) else None
        )

        return return_table(
            session=lib,
            output_type=output_type,
            vfile=vouttbl,
            colnames=column_names,
        )


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    S="summary",
    V="verbose",
    a="aspatial",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    o="outcols",
    r="registration",
    w="wrap",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma", o="sequence_comma")
def blockmean(
    data=None, x=None, y=None, z=None, output_type="pandas", outfile=None, **kwargs
):
    r"""
    Block average (x, y, z) data tables by mean estimation.

    Reads arbitrarily located (x, y, z) triplets [or optionally weighted
    quadruplets (x, y, z, w)] and writes to the output a mean position and
    value for every non-empty block in a grid region defined by the ``region``
    and ``spacing`` parameters.

    Takes a matrix, (x, y, z) triplets, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`blockmean.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.

    {spacing}

    summary : str
        [**m**\|\ **n**\|\ **s**\|\ **w**].
        Type of summary values calculated by blockmean.

        - **m** - reports mean value [Default]
        - **n** - report the number of input points inside each block
        - **s** - report the sum of all z-values inside a block
        - **w** - report the sum of weights

    {region}

    outfile : str
        The file name for the output ASCII file.

    {verbose}
    {aspatial}
    {binary}
    {nodata}
    {find}
    {incols}
    {coltypes}
    {header}
    {outcols}
    {registration}
    {wrap}

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set.
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``).

    Example
    -------
    >>> import pygmt
    >>> # Load a table of ship observations of bathymetry off Baja California
    >>> data = pygmt.datasets.load_sample_data(name="bathymetry")
    >>> # Calculate block mean values within 5 by 5 arc-minute bins
    >>> data_bmean = pygmt.blockmean(
    ...     data=data, region=[245, 255, 20, 30], spacing="5m"
    ... )
    """
    return _blockm(
        block_method="blockmean",
        data=data,
        x=x,
        y=y,
        z=z,
        output_type=output_type,
        outfile=outfile,
        **kwargs,
    )


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    V="verbose",
    a="aspatial",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    o="outcols",
    r="registration",
    w="wrap",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma", o="sequence_comma")
def blockmedian(
    data=None, x=None, y=None, z=None, output_type="pandas", outfile=None, **kwargs
):
    r"""
    Block average (x, y, z) data tables by median estimation.

    Reads arbitrarily located (x, y, z) triplets [or optionally weighted
    quadruplets (x, y, z, w)] and writes to the output a median position and
    value for every non-empty block in a grid region defined by the ``region``
    and ``spacing`` parameters.

    Takes a matrix, (x, y, z) triplets, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`blockmedian.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.

    {spacing}

    {region}

    outfile : str
        The file name for the output ASCII file.

    {verbose}
    {aspatial}
    {binary}
    {nodata}
    {find}
    {coltypes}
    {header}
    {incols}
    {outcols}
    {registration}
    {wrap}

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set.
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``).

    Example
    -------
    >>> import pygmt
    >>> # Load a table of ship observations of bathymetry off Baja California
    >>> data = pygmt.datasets.load_sample_data(name="bathymetry")
    >>> # Calculate block median values within 5 by 5 arc-minute bins
    >>> data_bmedian = pygmt.blockmedian(
    ...     data=data, region=[245, 255, 20, 30], spacing="5m"
    ... )
    """
    return _blockm(
        block_method="blockmedian",
        data=data,
        x=x,
        y=y,
        z=z,
        output_type=output_type,
        outfile=outfile,
        **kwargs,
    )


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    V="verbose",
    a="aspatial",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    o="outcols",
    r="registration",
    w="wrap",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma", o="sequence_comma")
def blockmode(
    data=None, x=None, y=None, z=None, output_type="pandas", outfile=None, **kwargs
):
    r"""
    Block average (x, y, z) data tables by mode estimation.

    Reads arbitrarily located (x, y, z) triplets [or optionally weighted
    quadruplets (x, y, z, w)] and writes to the output a mode position and
    value for every non-empty block in a grid region defined by the ``region``
    and ``spacing`` parameters.

    Takes a matrix, (x, y, z) triplets, or a file name as input.

    Must provide either ``data`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`blockmode.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D
        {table-classes}.
    x/y/z : 1-D arrays
        Arrays of x and y coordinates and values z of the data points.

    {spacing}

    {region}

    outfile : str
        The file name for the output ASCII file.

    {verbose}
    {aspatial}
    {binary}
    {nodata}
    {find}
    {coltypes}
    {header}
    {incols}
    {outcols}
    {registration}
    {wrap}

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set.
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``).

    Example
    -------
    >>> import pygmt
    >>> # Load a table of ship observations of bathymetry off Baja California
    >>> data = pygmt.datasets.load_sample_data(name="bathymetry")
    >>> # Calculate block mode values within 5 by 5 arc-minute bins
    >>> data_bmode = pygmt.blockmode(
    ...     data=data, region=[245, 255, 20, 30], spacing="5m"
    ... )
    """
    return _blockm(
        block_method="blockmode",
        data=data,
        x=x,
        y=y,
        z=z,
        output_type=output_type,
        outfile=outfile,
        **kwargs,
    )
