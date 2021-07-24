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
    table : ascii file (xyz tables)
    The file name of the input xyz file, with the extension: file.xyz

    {G}: str or None
    The name of the output netCDF file with extension .nc to store the grid
    in. If non is given, it will be the same name of the input file, just with
    different extensions.

    I : str
    xinc[unit][=|+][/yinc[unit][=|+]]
    x_inc [and optionally y_inc] is the grid spacing. Optionally, append a suffix modifier.
    Geographical (degrees) coordinates: Append m to indicate arc minutes or s to indicate arc
    seconds. If one of the units e, f, k, M, n or u is appended instead, the increment is
    assumed to be given in meter, foot, km, Mile, nautical mile or US survey foot,
    respectively, and will be converted to the equivalent degrees longitude at the middle
    latitude of the region (the conversion depends on PROJ_ELLIPSOID). If y_inc is given but
    set to 0 it will be reset equal to x_inc; otherwise it will be converted to degrees
    latitude. All coordinates: If = is appended then the corresponding max x (east) or y
    (north) may be slightly adjusted to fit exactly the given increment [by default the
    increment may be adjusted slightly to fit the given domain]. Finally, instead of giving an
    increment you may specify the number of nodes desired by appending + to the supplied
    integer argument; the increment is then recalculated from the number of nodes and
    the domain. The resulting increment value depends on whether you have selected a gri
    dline-registered or pixel-registered grid; see GMT File Formats for details. Note: if
    -Rgrdfile is used then the grid spacing has already been initialized; use -I to override
    the values.

    {R}: str
    [unit]xmin/xmax/ymin/ymax[r] (more ...)
    Specify the region of interest.

    Optional Arguments
    ------------------

    table
    One or more ASCII [or binary, see -bi] files holding z or (x,y,z) values.
    The xyz triplets do not have to be sorted.
    One-column z tables must be sorted and the -Z must be set.

    -A[f|l|m|n|r|s|u|z]
    By default we will calculate mean values if multiple entries fall on the same node.
    Use -A to change this behavior, except it is ignored if -Z is given. Append f or s
    to simply keep the first or last data point that was assigned to each node. Append
    l or u to find the lowest (minimum) or upper (maximum) value at each node, respectively.
    Append m or r to compute mean or RMS value at each node, respectively. Append n to
    simply count the number of data points that were assigned to each node (this only
    requires two input columns x and y as z is not consulted). Append z to sum multiple
    values that belong to the same node.

    -Dxname/yname/zname/scale/offset/invalid/title/remark
    Give values for xname, yname, zname (give the names of those variables and in square
    bracket their units, e.g., “distance [km]”), scale (to multiply grid values after read
    [normally 1]), offset (to add to grid after scaling [normally 0]), invalid (a value to
    represent missing data [NaN]), title (anything you like), and remark (anything you like).
    To leave some of these values untouched, leave field blank. Empty fields in the end may
    be skipped. Alternatively, to allow “/” to be part of one of the values, use any
    non-alphanumeric character (and not the equal sign) as separator by both starting and
    ending with it. For example: -D:xname:yname:zname:scale:offset:invalid:title:remark:
    Use quotes to group texts with more than one word. Note that for geographic grids (-fg)
    xname and yname are set automatically.

    -S[zfile]
    Swap the byte-order of the input only. No grid file is produced.
    You must also supply the -Z option. The output is written to zfile (or stdout if not supplied).

    -V[level] (more ...)
    Select verbosity level [c].

    -Z[flags]
    Read a 1-column ASCII [or binary] table. This assumes that all the nodes are present
    and sorted according to specified ordering convention contained in flags. If incoming
    data represents rows, make flags start with T(op) if first row is y = ymax or B(ottom)
    if first row is y = ymin. Then, append L or R to indicate that first element is at left
    or right end of row. Likewise for column formats: start with L or R to position first
    column, and then append T or B to position first element in a row. Note: These two
    row/column indicators are only required for grids; for other tables they do not apply.
    For gridline registered grids: If data are periodic in x but the incoming data do not
    contain the (redundant) column at x = xmax, append x. For data periodic in y without
    redundant row at y = ymax, append y. Append sn to skip the first n number of bytes
    (probably a header). If the byte-order or the words needs to be swapped, append w.
    Select one of several data types (all binary except a):

    A ASCII representation of one or more floating point values per record

    a ASCII representation of a single item per record

    c int8_t, signed 1-byte character

    u uint8_t, unsigned 1-byte character

    h int16_t, signed 2-byte integer

    H uint16_t, unsigned 2-byte integer

    i int32_t, signed 4-byte integer

    I uint32_t, unsigned 4-byte integer

    l int64_t, long (8-byte) integer

    L uint64_t, unsigned long (8-byte) integer

    f 4-byte floating point single precision

    d 8-byte floating point double precision

    Default format is scanline orientation of ASCII numbers: -ZTLa.
    Note that -Z only applies to 1-column input.
    The difference between A and a is that the latter can decode both dateTclock and
    ddd:mm:ss[.xx] formats while the former is strictly for regular floating point values.

    -bi[ncols][t] (more ...)
    Select native binary input. [Default is 3 input columns]. This option only applies
    to xyz input files; see -Z for z tables.

    -dinodata (more ...)
    Replace input columns that equal nodata with NaN. Also sets nodes with no input
    xyz triplet to this value [Default is NaN].

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

    Usage
    -------
    pygmt.xyz2grd('file.xyz',G='file.nc',I='res',R='g')
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
