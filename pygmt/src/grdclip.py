"""
grdclip - Change the range and extremes of grid values.
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

__doctest_skip__ = ["grdclip"]


@fmt_docstring
@use_alias(
    G="outgrid",
    R="region",
    Sa="above",
    Sb="below",
    Si="between",
    Sr="new",
    V="verbose",
)
@kwargs_to_strings(
    R="sequence",
    Sa="sequence",
    Sb="sequence",
    Si="sequence",
    Sr="sequence",
)
def grdclip(grid, **kwargs):
    r"""
    Sets values in a grid that meet certain criteria to a new value.

    Produce a clipped ``outgrid`` or :class:`xarray.DataArray` version of the
    input ``grid`` file.

    The parameters ``above`` and ``below`` allow for a given value to be set
    for values above or below a set amount, respectively. This allows for
    extreme values in a grid, such as points below a certain depth when
    plotting Earth relief, to all be set to the same value.

    Full option list at :gmt-docs:`grdclip.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {region}
    above : str or list or tuple
        [*high*, *above*].
        Set all data[i] > *high* to *above*.
    below : str or list or tuple
        [*low*, *below*].
        Set all data[i] < *low* to *below*.
    between : str or list or tuple
        [*low*, *high*, *between*].
        Set all data[i] >= *low* and <= *high* to *between*.
    new : str or list or tuple
        [*old*, *new*].
        Set all data[i] == *old* to *new*. This is mostly useful when
        your data are known to be integer values.
    {verbose}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a grid of @earth_relief_30m data, with an x-range of 10 to 30,
    >>> # and a y-range of 15 to 25
    >>> grid = pygmt.datasets.load_earth_relief(
    ...     resolution="30m", region=[10, 30, 15, 25]
    ... )
    >>> # Report the minimum and maximum data values
    >>> [grid.data.min(), grid.data.max()]
    [170.0, 2275.5]
    >>> # Create a new grid from an input grid. Set all values below 1,000 to
    >>> # 0 and all values above 1,500 to 10,000
    >>> new_grid = pygmt.grdclip(
    ...     grid=grid, below=[1000, 0], above=[1500, 10000]
    ... )
    >>> # Report the minimum and maximum data values
    >>> [new_grid.data.min(), new_grid.data.max()]
    [0.0, 10000.0]
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="grdclip", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
