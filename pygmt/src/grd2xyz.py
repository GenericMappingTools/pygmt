"""
grd2xyz - Convert grid to data table
"""
import warnings

import pandas as pd
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grd2xyz"]


@fmt_docstring
@use_alias(
    C="cstyle",
    R="region",
    V="verbose",
    W="weight",
    Z="convention",
    b="binary",
    d="nodata",
    f="coltypes",
    h="header",
    o="outcols",
    s="skiprows",
)
@kwargs_to_strings(R="sequence", o="sequence_comma")
def grd2xyz(grid, output_type="pandas", outfile=None, **kwargs):
    r"""
    Convert grid to data table.

    Read a grid and output xyz-triplets as a :class:`numpy.ndarray`,
    :class:`pandas.DataFrame`, or ASCII file.

    Full option list at :gmt-docs:`grd2xyz.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a
        :class:`xarray.DataArray`. This is the only required parameter.
    output_type : str
        Determine the format the xyz data will be returned in [Default is
        ``pandas``]:

            - ``numpy`` - :class:`numpy.ndarray`
            - ``pandas``- :class:`pandas.DataFrame`
            - ``file`` - ASCII file (requires ``outfile``)
    outfile : str
        The file name for the output ASCII file.
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

        * **a** ASCII representation of a single item per record
        * **c** int8_t, signed 1-byte character
        * **u** uint8_t, unsigned 1-byte character
        * **h** int16_t, short 2-byte integer
        * **H** uint16_t, unsigned short 2-byte integer
        * **i** int32_t, 4-byte integer
        * **I** uint32_t, unsigned 4-byte integer
        * **l** int64_t, long (8-byte) integer
        * **L** uint64_t, unsigned long (8-byte) integer
        * **f** 4-byte floating point single precision
        * **d** 8-byte floating point double precision

        Default format is scanline orientation of ASCII numbers: **TLa**.
    {binary}
    {nodata}
    {coltypes}
    {header}
    {outcols}
    {skiprows}

    Returns
    -------
    ret : pandas.DataFrame or numpy.ndarray or None
        Return type depends on ``outfile`` and ``output_type``:

        - None if ``outfile`` is set (output will be stored in file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is
          not set (depends on ``output_type``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with an x-range of 10 to 30,
    >>> # and a y-range of 15 to 25
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Create a pandas DataFrame with the xyz data from an input grid
    >>> xyz_dataframe = pygmt.grd2xyz(grid=grid, output_type="pandas")
    >>> xyz_dataframe.head(n=2)
        lon   lat  elevation
    0  10.0  25.0      863.0
    1  10.5  25.0      985.5
    """
    if output_type not in ["numpy", "pandas", "file"]:
        raise GMTInvalidInput(
            "Must specify 'output_type' either as 'numpy', 'pandas' or 'file'."
        )

    if outfile is not None and output_type != "file":
        msg = (
            f"Changing 'output_type' of grd2xyz from '{output_type}' to 'file' "
            "since 'outfile' parameter is set. Please use output_type='file' "
            "to silence this warning."
        )
        warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
        output_type = "file"
    elif outfile is None and output_type == "file":
        raise GMTInvalidInput("Must specify 'outfile' for ASCII output.")

    if kwargs.get("o") is not None and output_type == "pandas":
        raise GMTInvalidInput(
            "If 'outcols' is specified, 'output_type' must be either 'numpy'"
            "or 'file'."
        )

    # Set the default column names for the pandas dataframe header
    dataframe_header = ["x", "y", "z"]
    # Let output pandas column names match input DataArray dimension names
    if isinstance(grid, xr.DataArray) and output_type == "pandas":
        # Reverse the dims because it is rows, columns ordered.
        dataframe_header = [grid.dims[1], grid.dims[0], grid.name]

    with GMTTempFile() as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                lib.call_module(
                    module="grd2xyz",
                    args=build_arg_string(kwargs, infile=infile, outfile=outfile),
                )

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            result = pd.read_csv(
                tmpfile.name, sep="\t", names=dataframe_header, comment=">"
            )
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

        if output_type == "numpy":
            result = result.to_numpy()
    return result
