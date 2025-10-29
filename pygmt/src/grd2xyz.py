"""
grd2xyz - Convert grid to data table.
"""

from collections.abc import Sequence
from typing import Literal

import numpy as np
import pandas as pd
import xarray as xr
from pygmt._typing import PathLike
from pygmt.alias import AliasSystem
from pygmt.clib import Session
from pygmt.exceptions import GMTValueError
from pygmt.helpers import (
    build_arg_list,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
    validate_output_table_type,
)

__doctest_skip__ = ["grd2xyz"]


@fmt_docstring
@use_alias(
    C="cstyle",
    W="weight",
    Z="convention",
    b="binary",
    d="nodata",
    f="coltypes",
    h="header",
    o="outcols",
    s="skiprows",
)
@kwargs_to_strings(o="sequence_comma")
def grd2xyz(
    grid: PathLike | xr.DataArray,
    output_type: Literal["pandas", "numpy", "file"] = "pandas",
    outfile: PathLike | None = None,
    region: Sequence[float | str] | str | None = None,
    verbose: Literal["quiet", "error", "warning", "timing", "info", "compat", "debug"]
    | bool = False,
    **kwargs,
) -> pd.DataFrame | np.ndarray | None:
    r"""
    Convert grid to data table.

    Read a grid and output xyz-triplets as a :class:`numpy.ndarray`,
    :class:`pandas.DataFrame`, or ASCII file.

    Full GMT docs at :gmt-docs:`grd2xyz.html`.

    {aliases}
       - R = region
       - V = verbose

    Parameters
    ----------
    {grid}
    {output_type}
    {outfile}
    cstyle : str
        [**f**\|\ **i**].
        Replace the x- and y-coordinates on output with the corresponding
        column and row numbers. These start at 0 (C-style counting); append
        **f** to start at 1 (Fortran-style counting). Alternatively, append
        **i** to write just the two columns *index* and *z*, where *index*
        is the 1-D indexing that GMT uses when referring to grid nodes.
    {region}
        Adding ``region`` will select a subsection of the grid. If this
        subsection exceeds the boundaries of the grid, only the common region
        will be output.
    weight : str
        [**a**\ [**+u**\ *unit*]\|\ *weight*].
        Write out *x,y,z,w*\ , where *w* is the supplied *weight* (or 1 if not
        supplied) [Default writes *x,y,z* only].  Choose **a** to compute
        weights equal to the area each node represents.  For Cartesian grids
        this is simply the product of the *x* and *y* increments (except for
        gridline-registered grids at all sides [half] and corners [quarter]).
        For geographic grids we default to a length unit of **k**. Change
        this by appending **+u**\ *unit*. For such grids, the area
        varies with latitude and also sees special cases for
        gridline-registered layouts at sides, corners, and poles.
    {verbose}
    convention : str
        [*flags*].
        Write a 1-column ASCII [or binary] table. Output will be organized
        according to the specified ordering convention contained in *flags*.
        If data should be written by rows, make *flags* start with
        **T** (op) if first row is y = ymax or
        **B** (ottom) if first row is y = ymin. Then,
        append **L** or **R** to indicate that first element should start at
        left or right end of row. Likewise for column formats: start with
        **L** or **R** to position first column, and then append **T** or
        **B** to position first element in a row. For gridline registered
        grids: If grid is periodic in x but the written data should not
        contain the (redundant) column at x = xmax, append **x**. For grid
        periodic in y, skip writing the redundant row at y = ymax by
        appending **y**. If the byte-order needs to be swapped, append
        **w**. Select one of several data types (all binary except **a**):

        - **a**: ASCII representation of a single item per record
        - **c**: int8_t, signed 1-byte character
        - **u**: uint8_t, unsigned 1-byte character
        - **h**: int16_t, short 2-byte integer
        - **H**: uint16_t, unsigned short 2-byte integer
        - **i**: int32_t, 4-byte integer
        - **I**: uint32_t, unsigned 4-byte integer
        - **l**: int64_t, long (8-byte) integer
        - **L**: uint64_t, unsigned long (8-byte) integer
        - **f**: 4-byte floating point single precision
        - **d**: 8-byte floating point double precision

        Default format is scanline orientation of ASCII numbers: **TLa**.
    {binary}
    {nodata}
    {coltypes}
    {header}
    {outcols}
    {skiprows}

    Returns
    -------
    ret
        Return type depends on ``outfile`` and ``output_type``:

        - ``None`` if ``outfile`` is set (output will be stored in the file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is not set
          (depends on ``output_type``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with a longitude range of
    >>> # 10° E to 30° E, and a latitude range of 15° N to 25° N
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a pandas.DataFrame with the xyz data from an input grid
    >>> xyz_dataframe = pygmt.grd2xyz(grid=grid, output_type="pandas")
    >>> xyz_dataframe.head(n=2)
        lon   lat          z
    0  10.0  25.0      965.5
    1  10.5  25.0      876.5
    """
    output_type = validate_output_table_type(output_type, outfile=outfile)

    if kwargs.get("o") is not None and output_type == "pandas":
        raise GMTValueError(
            output_type,
            description="value for parameter 'output_type'",
            reason="Expected one of: 'numpy', 'file' if 'outcols' is specified.",
        )
    # Set the default column names for the pandas DataFrame header.
    column_names: list[str] = ["x", "y", "z"]
    # Let output pandas column names match input DataArray dimension names
    if output_type == "pandas" and isinstance(grid, xr.DataArray):
        # Reverse the dims because it is rows, columns ordered.
        column_names = [str(grid.dims[1]), str(grid.dims[0]), str(grid.name)]

    aliasdict = AliasSystem().add_common(
        R=region,
        V=verbose,
    )
    aliasdict.merge(kwargs)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="dataset", fname=outfile) as vouttbl,
        ):
            lib.call_module(
                module="grd2xyz",
                args=build_arg_list(aliasdict, infile=vingrd, outfile=vouttbl),
            )
            return lib.virtualfile_to_dataset(
                vfname=vouttbl, output_type=output_type, column_names=column_names
            )
