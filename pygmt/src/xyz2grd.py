"""
xyz2grd - Convert data table to a grid.
"""
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    data_kind,
    dummy_context,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    G="outgrid",
    I="spacing",
    R="region",
    S="zfile",
    V="level",
    Z="single_column",
    bi="binary",
    di="nodata",
    f="flags",
    h="headers",
    i="select_column",
)
@kwargs_to_strings(R="sequence")
def xyz2grd(table, **kwargs):
    """
    Create a grid file from table data.

    xyz2grd reads one or more z or xyz tables and creates a binary grid file.
    xyz2grd will report if some of the nodes are not filled in with data. Such
    unconstrained nodes are set to a value specified by the user [Default is
    NaN]. Nodes with more than one value will be set to the mean value. As an
    option (using -Z), a 1-column z-table may be read assuming all nodes are
    present (z-tables can be in organized in a number of formats, see -Z
    below.)

    Full option list at :gmt-docs:`xyz2grd.html`


    Parameters
    ----------
    table : str or {table-like}
        Pass in either a file name to an ASCII data table, a 1D/2D
        {table-classes}.

    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {I}
    {R}
    -A[f|l|m|n|r|s|u|z]
    By default we will calculate mean values if multiple entries fall on
    the same node. Use **-A** to change this behavior, except it is
    ignored if **-Z** is given. Append **f** or **s** to simply keep the
    first or last data point that was assigned to each node. Append
    **l** or **u** or **d** to find the lowest (minimum) or upper (maximum)
    value or the difference between the maximum and miminum value at each
    node, respectively. Append **m** or **r** or **S** to compute mean or
    RMS value or standard deviation at each node, respectively. Append **n**
    to simply count the number of data points that were assigned to each node
    (this only requires two input columns *x* and *y* as *z* is not consulted).
    Append **z** to sum multiple values that belong to the same node.

    -Dxname/yname/zname/scale/offset/invalid/title/remark
    Give values for xname, yname, zname (give the names of those variables and
    in square bracket their units, e.g., “distance [km]”), scale (to multiply
    grid values after read [normally 1]), offset (to add to grid after
    scaling [normally 0]), invalid (a value to represent missing data [NaN]),
    title (anything you like), and remark (anything you like). To leave some
    of these values untouched, leave field blank. Empty fields in the end may
    be skipped. Alternatively, to allow “/” to be part of one of the values,
    use any non-alphanumeric character (and not the equal sign) as separator
    by both starting and ending with it.

    -S[zfile]
    Swap the byte-order of the input only. No grid file is produced.
    You must also supply the -Z option. The output is written to zfile
    (or stdout if not supplied).
    {V}

    -Z[flags]
    Read a 1-column ASCII [or binary] table. This assumes that all the
    nodes are present and sorted according to specified ordering
    convention contained in *flags*. If incoming data represents rows,
    make *flags* start with **T**\ (op) if first row is y
    = ymax or **B**\ (ottom) if first row is y = ymin.
    Then, append **L** or **R** to indicate that first element is at
    left or right end of row. Likewise for column formats: start with
    **L** or **R** to position first column, and then append **T** or
    **B** to position first element in a row. **Note**: These two row/column
    indicators are only required for grids; for other tables they do not
    apply. For gridline registered grids: If data are periodic in x but
    the incoming data do not contain the (redundant) column at x = xmax,
    append **x**. For data periodic in y without redundant row at y =
    ymax, append **y**. Append **s**\ *n* to skip the first *n* number
    of bytes (probably a header). If the byte-order or the words needs
    to be swapped, append **w**. Select one of several data types (all
    binary except **a**):

    **A** ASCII representation of one or more floating point values per record

    **a** ASCII representation of a single item per record

    **c** int8_t, signed 1-byte character

    **u** uint8_t, unsigned 1-byte character

    **h** int16_t, signed 2-byte integer

    **H** uint16_t, unsigned 2-byte integer

    **i** int32_t, signed 4-byte integer

    **I** uint32_t, unsigned 4-byte integer

    **l** int64_t, long (8-byte) integer

    **L** uint64_t, unsigned long (8-byte) integer

    **f** 4-byte floating point single precision

    **d** 8-byte floating point double precision

    Default format is scanline orientation of ASCII numbers: **TLa**.
    The difference between **A** and **a** is that the latter can decode both
    *date*\ **T**\ *clock* and *ddd:mm:ss[.xx]* formats but expects each
    input record to have a single value, while the former can handle multiple
    values per record but can only parse regular floating point values.
    Translate incoming *z*-values via the **-i**\ 0 option and needed
    modifiers.

    -bi[ncols][t] (more ...)
    Select native binary input. [Default is 3 input columns]. This option only
    applies to xyz input files.

    -dinodata (more ...)
    Replace input columns that equal nodata with NaN. Also sets nodes with no
    input xyz triplet to this value [Default is NaN].

    -f[i|o]colinfo (more ...)
    Specify data types of input and/or output columns.

    -h[i|o][n][+c][+d][+rremark][+rtitle] (more ...)
    Skip or produce header record(s). Not used with binary data.

    -icols[l][sscale][ooffset][,...] (more ...)
    Select input columns (0 is first column).

    -r (more ...)
    Set pixel node registration [gridline].

    Returns
    -------
    ret: xarray.DataArray or None
    Return type depends on whether the *outgrid* parameter is set:
    - xarray.DataArray if *outgrid* is not set
    - None if *outgrid* is set (grid output will be stored in *outgrid*)
    """
    kind = data_kind(table)

    with GMTTempFile(suffix=".xyz") as tmpfile:
        with Session() as lib:
            if kind == "file":
                file_context = dummy_context(table)
            elif kind == "matrix":
                file_context = lib.virtualfile_from_matrix(matrix=table)
            else:
                raise GMTInvalidInput("Unrecognized data type: {}".format(type(table)))

            with file_context as infile:
                if "G" not in kwargs.keys():  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = build_arg_string(kwargs)
                arg_str = " ".join([infile, arg_str])
                lib.call_module("xyz2grd", arg_str)

        if outgrid == tmpfile.name:  # if user did not set outgrid, return DataArray
            with xr.open_dataarray(outgrid) as dataarray:
                result = dataarray.load()
                _ = result.gmt  # load GMTDataArray accessor information
        else:
            result = None  # if user sets an outgrid, return None

        return result
