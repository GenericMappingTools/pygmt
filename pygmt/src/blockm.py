"""
blockm - Block average (x,y,z) data tables by mean or median estimation.
"""
import pandas as pd
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


def _blockm(block_method, table, outfile, x, y, z, **kwargs):
    r"""
    Block average (x,y,z) data tables by mean or median estimation.

    Reads arbitrarily located (x,y,z) triples [or optionally weighted
    quadruples (x,y,z,w)] from a table and writes to the output a mean or
    median (depending on ``block_method``) position and value for every
    non-empty block in a grid region defined by the ``region`` and ``spacing``
    parameters.

    Parameters
    ----------
    block_method : str
        Name of the GMT module to call. Must be "blockmean" or "blockmedian".

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``)
    """

    with GMTTempFile(suffix=".csv") as tmpfile:
        with Session() as lib:
            # Choose how data will be passed into the module
            table_context = lib.virtualfile_from_data(
                check_kind="vector", data=table, x=x, y=y, z=z
            )
            # Run blockm* on data table
            with table_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([infile, build_arg_string(kwargs), "->" + outfile])
                lib.call_module(module=block_method, args=arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            try:
                column_names = table.columns.to_list()
                result = pd.read_csv(tmpfile.name, sep="\t", names=column_names)
            except AttributeError:  # 'str' object has no attribute 'columns'
                result = pd.read_csv(tmpfile.name, sep="\t", header=None, comment=">")
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

    return result


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    V="verbose",
    a="aspatial",
    f="coltypes",
    i="incols",
    o="outcols",
    r="registration",
    s="skiprows",
    w="wrap",
)
@kwargs_to_strings(R="sequence")
def blockmean(table=None, outfile=None, *, x=None, y=None, z=None, **kwargs):
    r"""
    Block average (x,y,z) data tables by mean estimation.

    Reads arbitrarily located (x,y,z) triples [or optionally weighted
    quadruples (x,y,z,w)] and writes to the output a mean position and value
    for every non-empty block in a grid region defined by the ``region`` and
    ``spacing`` parameters.

    Takes a matrix, xyz triplets, or a file name as input.

    Must provide either ``table`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`blockmean.html`

    {aliases}

    Parameters
    ----------
    table : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.

    {I}

    {R}

    outfile : str
        The file name for the output ASCII file.

    {V}
    {a}
    {i}
    {f}
    {o}
    {r}
    {s}
    {w}

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set.
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``).
    """
    return _blockm(
        block_method="blockmean", table=table, outfile=outfile, x=x, y=y, z=z, **kwargs
    )


@fmt_docstring
@use_alias(
    I="spacing",
    R="region",
    V="verbose",
    a="aspatial",
    f="coltypes",
    i="incols",
    o="outcols",
    r="registration",
    s="skiprows",
    w="wrap",
)
@kwargs_to_strings(R="sequence")
def blockmedian(table=None, outfile=None, *, x=None, y=None, z=None, **kwargs):
    r"""
    Block average (x,y,z) data tables by median estimation.

    Reads arbitrarily located (x,y,z) triples [or optionally weighted
    quadruples (x,y,z,w)] and writes to the output a median position and value
    for every non-empty block in a grid region defined by the ``region`` and
    ``spacing`` parameters.

    Takes a matrix, xyz triplets, or a file name as input.

    Must provide either ``table`` or ``x``, ``y``, and ``z``.

    Full option list at :gmt-docs:`blockmedian.html`

    {aliases}

    Parameters
    ----------
    table : str or {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    x/y/z : 1d arrays
        Arrays of x and y coordinates and values z of the data points.

    {I}

    {R}

    outfile : str
        The file name for the output ASCII file.

    {V}
    {a}
    {f}
    {i}
    {o}
    {r}
    {s}
    {w}

    Returns
    -------
    output : pandas.DataFrame or None
        Return type depends on whether the ``outfile`` parameter is set:

        - :class:`pandas.DataFrame` table with (x, y, z) columns if ``outfile``
          is not set.
        - None if ``outfile`` is set (filtered output will be stored in file
          set by ``outfile``).
    """
    return _blockm(
        block_method="blockmedian",
        table=table,
        outfile=outfile,
        x=x,
        y=y,
        z=z,
        **kwargs
    )
