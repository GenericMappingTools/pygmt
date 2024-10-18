"""
grdfill - Fill blank areas from a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["grdfill"]


@fmt_docstring
@use_alias(
    A="mode",
    N="no_data",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grdfill(grid, outgrid: str | None = None, **kwargs) -> xr.DataArray | None:
    r"""
    Fill blank areas from a grid file.

    Read a grid that presumably has unfilled holes that the user wants to
    fill in some fashion. Holes are identified by NaN values but this
    criteria can be changed via the ``no_data`` parameter. There are several
    different algorithms that can be used to replace the hole values.

    Full option list at :gmt-docs:`grdfill.html`

    {aliases}

    Parameters
    ----------
    {grid}
    {outgrid}
    mode : str
        Specify the hole-filling algorithm to use.  Choose from **c** for
        constant fill and append the constant value, **n** for nearest
        neighbor (and optionally append a search radius in
        pixels [default radius is :math:`r^2 = \sqrt{{ X^2 + Y^2 }}`,
        where (*X,Y*) are the node dimensions of the grid]), or
        **s** for bicubic spline (optionally append a *tension*
        parameter [Default is no tension]).
    no_data : float
        Set the node value used to identify a point as a member of a hole
        [Default is NaN].

    {region}
    {verbose}

    Returns
    -------
    ret
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)

    Example
    -------
    >>> import pygmt
    >>> # Load a bathymetric grid with missing data
    >>> earth_relief_holes = pygmt.datasets.load_sample_data(name="earth_relief_holes")
    >>> # Perform grid filling operations on the sample grid
    >>> # Set all empty values to "20"
    >>> filled_grid = pygmt.grdfill(grid=earth_relief_holes, mode="c20")
    """
    if kwargs.get("A") is None and kwargs.get("L") is None:
        raise GMTInvalidInput("At least parameter 'mode' or 'L' must be specified.")

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            kwargs["G"] = voutgrd
            lib.call_module(
                module="grdfill", args=build_arg_list(kwargs, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
