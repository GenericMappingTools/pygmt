"""
xyz2grd - Convert data table to a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["xyz2grd"]


@fmt_docstring
@use_alias(
    A="duplicate",
    I="spacing",
    J="projection",
    R="region",
    V="verbose",
    Z="convention",
    b="binary",
    d="nodata",
    e="find",
    f="coltypes",
    h="header",
    i="incols",
    r="registration",
    w="wrap",
)
@kwargs_to_strings(I="sequence", R="sequence")
def xyz2grd(
    data=None, x=None, y=None, z=None, outgrid: str | None = None, **kwargs
) -> xr.DataArray | None:
    r"""
    Create a grid file from table data.

    Reads one or more tables with *x, y, z* columns and creates a binary grid
    file. :func:`pygmt.xyz2grd` will report if some of the nodes are not filled
    in with data. Such unconstrained nodes are set to a value specified by the
    user [Default is NaN]. Nodes with more than one value will be set to the
    mean value.

    Full option list at :gmt-docs:`xyz2grd.html`

    {aliases}

    Parameters
    ----------
    data : str, {table-like}
        Pass in (x, y, z) or (longitude, latitude, elevation) values by
        providing a file name to an ASCII data table, a 2-D {table-classes}.
    x/y/z : 1-D arrays
        The arrays of x and y coordinates and z data points.
    {outgrid}
    duplicate : str
        [**d**\|\ **f**\|\ **l**\|\ **m**\|\ **n**\|\
        **r**\|\ **S**\|\ **s**\|\ **u**\|\ **z**].
        By default we will calculate mean values if multiple entries fall on
        the same node. Use ``duplicate`` to change this behavior, except it is
        ignored if ``convention`` is given. Append **f** or **s** to simply
        keep the first or last data point that was assigned to each node.
        Append **l** or **u** or **d** to find the lowest (minimum) or upper
        (maximum) value or the difference between the maximum and minimum
        values at each node, respectively. Append **m** or **r** or **S** to
        compute mean or RMS value or standard deviation at each node,
        respectively. Append **n** to simply count the number of data points
        that were assigned to each node (this only requires two input columns
        *x* and *y* as *z* is not consulted). Append **z** to sum multiple
        values that belong to the same node.
    {spacing}
    {projection}
    {region}
    {verbose}
    convention : str
        [*flags*].
        Read a 1-column ASCII [or binary] table. This assumes that all the
        nodes are present and sorted according to specified ordering
        convention contained in *flags*. If incoming data represents rows,
        make *flags* start with **T**\ (op) if first row is y
        = ymax or **B**\ (ottom) if first row is y = ymin.
        Then, append **L** or **R** to indicate that first element is at
        left or right end of row. Likewise for column formats: start with
        **L** or **R** to position first column, and then append **T** or
        **B** to position first element in a row. **Note**: These two
        row/column indicators are only required for grids; for other tables
        they do not apply. For gridline registered grids: If data are periodic
        in x but the incoming data do not contain the (redundant) column at
        x = xmax, append **x**. For data periodic in y without redundant row at
        y = ymax, append **y**. Append **s**\ *n* to skip the first *n* number
        of bytes (probably a header). If the byte-order or the words needs
        to be swapped, append **w**. Select one of several data types (all
        binary except **a**):

        - **A** ASCII representation of one or more floating point values per
          record
        - **a** ASCII representation of a single item per record
        - **c** int8_t, signed 1-byte character
        - **u** uint8_t, unsigned 1-byte character
        - **h** int16_t, signed 2-byte integer
        - **H** uint16_t, unsigned 2-byte integer
        - **i** int32_t, signed 4-byte integer
        - **I** uint32_t, unsigned 4-byte integer
        - **l** int64_t, long (8-byte) integer
        - **L** uint64_t, unsigned long (8-byte) integer
        - **f** 4-byte floating point single precision
        - **d** 8-byte floating point double precision

        [Default format is scanline orientation of ASCII numbers: **La**].
        The difference between **A** and **a** is that the latter can decode
        both *date*\ **T**\ *clock* and *ddd:mm:ss[.xx]* formats but expects
        each input record to have a single value, while the former can handle
        multiple values per record but can only parse regular floating point
        values. Translate incoming *z*-values via the ``incols`` parameter.
    {binary}
    {nodata}
    {find}
    {coltypes}
    {header}
    {incols}
    {registration}
    {wrap}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray`: if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import numpy as np
    >>> import pygmt
    >>> # generate a grid for z=x**2+y**2, with an x-range of 0 to 3,
    >>> # and a y-range of 10.5 to 12.5. The x- and y-spacings are 1.0 and 0.5.
    >>> x, y = np.meshgrid([0, 1, 2, 3], [10.5, 11.0, 11.5, 12.0, 12.5])
    >>> z = x**2 + y**2
    >>> xx, yy, zz = x.flatten(), y.flatten(), z.flatten()
    >>> grid = pygmt.xyz2grd(
    ...     x=xx, y=yy, z=zz, spacing=(1.0, 0.5), region=[0, 3, 10, 13]
    ... )
    """
    if kwargs.get("I") is None or kwargs.get("R") is None:
        raise GMTInvalidInput("Both 'region' and 'spacing' must be specified.")

    with Session() as lib:
        with (
            lib.virtualfile_in(
                check_kind="vector", data=data, x=x, y=y, z=z, required_z=True
            ) as vintbl,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="xyz2grd", args=build_arg_list(kwargs, infile=vintbl)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
