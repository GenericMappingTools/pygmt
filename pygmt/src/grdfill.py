"""
grdfill - Fill blank areas from a grid.
"""

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray

__doctest_skip__ = ["grdfill"]


@fmt_docstring
@use_alias(
    A="mode",
    G="outgrid",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grdfill(grid, **kwargs):
    r"""
    Fill blank areas from a grid file.

    Read a grid that presumably has unfilled holes that the user
    wants to fill in some fashion. Holes are identified by NaN values but
    this criteria can be changed. There are several different algorithms that
    can be used to replace the hole values.

    Full option list at :gmt-docs:`grdfill.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a DataArray.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    mode : str
        Specify the hole-filling algorithm to use.  Choose from **c** for
        constant fill and append the constant value, **n** for nearest
        neighbor (and optionally append a search radius in
        pixels [default radius is :math:`r^2 = \sqrt{{ X^2 + Y^2 }}`,
        where (*X,Y*) are the node dimensions of the grid]), or
        **s** for bicubic spline (optionally append a *tension*
        parameter [Default is no tension]).

    {region}
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
    >>> # Load a bathymetric grid with missing data
    >>> earth_relief_holes = pygmt.datasets.load_sample_data(
    ...     name="earth_relief_holes"
    ... )
    >>> # Perform grid filling operations on the sample grid
    >>> # Set all empty values to "20"
    >>> filled_grid = pygmt.grdfill(grid=earth_relief_holes, mode="c20")
    """
    if kwargs.get("A") is None and kwargs.get("L") is None:
        raise GMTInvalidInput("At least parameter 'mode' or 'L' must be specified.")
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if (outgrid := kwargs.get("G")) is None:
                    kwargs["G"] = outgrid = tmpfile.name  # output to tmpfile
                lib.call_module(
                    module="grdfill", args=build_arg_string(kwargs, infile=infile)
                )

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
