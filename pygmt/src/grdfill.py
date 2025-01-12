"""
grdfill - Interpolate across holes in a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, fmt_docstring, kwargs_to_strings, use_alias

__doctest_skip__ = ["grdfill"]


def _parse_mode_value(mode, value=None):
    """
    Parse the mode and value arguments.
    """
    if mode not in {"constant", "grid", "neighbor", "spline", "c", "g", "n", "s"}:
        msg = "Invalid mode. Valid modes are: 'constant', 'grid', 'neighbor', 'spline'."
        raise GMTInvalidInput(msg)
    return f"{mode[0]}{value}"


@fmt_docstring
@use_alias(
    A="mode",
    N="no_data",
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grdfill(
    grid,
    outgrid: str | None = None,
    mode: Literal["constant", "grid", "neighbor", "spline"] | None = None,
    value: float | None = None,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Interpolate across holes in a grid.

    Read a grid that presumably has unfilled holes that the user wants to fill in some
    fashion. Holes are identified by NaN values but this criteria can be changed via the
    ``no_data`` parameter. There are several different algorithms that can be used to
    replace the hole values. If no holes are found, the original unchanged grid is
    returned.

    Full option list at :gmt-docs:`grdfill.html`.

    {aliases}

    Parameters
    ----------
    {grid}
    {outgrid}
    mode/value
        The hole-filling algorithm to use. Valid values are:

        - ``"constant"``: Select a constant fill (and append the constant fill value).
        - ``"grid"``: Sample the (possibly coarser) grid arg at the nodes making up the
          holes.
        - ``"neighbor"``: Select nearest neighbor fill (and optionally append a search radius
          in pixels [default radius is :math:`r^2 = \sqrt{n^2 + m^2}`, where (n,m) are
          the node dimensions of the grid]).
        - ``"spline"``: Select bicubic spline (optionally append a tension parameter [no tension]).
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
        - ``None`` if ``outgrid`` is set (grid output will be stored in the file set by
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
        msg = "At least parameter 'mode' or 'L' must be specified."
        raise GMTInvalidInput(msg)

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
