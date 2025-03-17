"""
grdfill - Interpolate across holes in a grid.
"""

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    build_arg_list,
    deprecate_parameter,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)

__doctest_skip__ = ["grdfill"]


def _parse_fill_mode(
    constantfill=None, gridfill=None, neighborfill=None, splinefill=None
) -> str | None:
    """
    Parse the fill parameters and return the appropriate string for the -A option.

    >>> import numpy as np
    >>> import xarray as xr
    >>> _parse_fill_mode(constantfill=20.0)
    'c20.0'
    >>> _parse_fill_mode(gridfill="bggrid.nc")
    'g'
    >>> _parse_fill_mode(gridfill=xr.DataArray(np.zeros((10, 10))))
    'g'
    >>> _parse_fill_mode(neighborfill=20)
    'n20'
    >>> _parse_fill_mode(neighborfill=True)
    'n'
    >>> _parse_fill_mode(splinefill=0.5)
    's0.5'
    >>> _parse_fill_mode(splinefill=True)
    's'
    """
    fill_params = [constantfill, gridfill, neighborfill, splinefill]
    if sum(param is not None for param in fill_params) > 1:
        msg = (
            "The 'constantfill', 'gridfill', 'neighborfill', and 'splinefill' "
            "parameters are mutually exclusive."
        )
        raise GMTInvalidInput(msg)

    if constantfill is not None:
        return f"c{constantfill}"
    if gridfill is not None:
        return "g"  # Append grid file name later to support xarray.DataArray.
    if neighborfill is not None and neighborfill is not False:
        return "n" if neighborfill is True else f"n{neighborfill}"
    if splinefill is not None and splinefill is not False:
        return "s" if splinefill is True else f"s{splinefill}"
    return None


@fmt_docstring
# TODO(PyGMT>=0.19.0): Remove the deprecated 'no_data' parameter.
@deprecate_parameter("no_data", "hole", "v0.15.0", remove_version="v0.19.0")
@use_alias(A="mode", N="hole", R="region", V="verbose")
@kwargs_to_strings(R="sequence")
def grdfill(
    grid: str | xr.DataArray,
    outgrid: str | None = None,
    constantfill: float | None = None,
    gridfill: str | xr.DataArray | None = None,
    neighborfill: float | bool | None = None,
    splinefill: float | bool | None = None,
    **kwargs,
) -> xr.DataArray | None:
    r"""
    Interpolate across holes in a grid.

    Read a grid that presumably has unfilled holes that the user wants to fill in some
    fashion. Holes are identified by NaN values but this criteria can be changed via the
    ``hole`` parameter. There are several different algorithms that can be used to
    replace the hole values. If no holes are found the original unchanged grid is
    returned.

    Full option list at :gmt-docs:`grdfill.html`.

    {aliases}

    Parameters
    ----------
    {grid}
    {outgrid}
    constantfill
        Fill the holes with a constant value. Specify the constant value to use.
    gridfill
        Fill the holes with values sampled from another (possibly coarser) grid. Specify
        the grid (a file name or an :class:`xarray.DataArray`) to use for the fill.
    neighborfill
        Fill the holes with the nearest neighbor. Specify the search radius in pixels.
        If set to ``True``, the default search radius will be used
        (:math:`r^2 = \sqrt{{n^2 + m^2}}`, where (n,m) are the node dimensions of the
        grid).
    splinefill
        Fill the holes with a bicubic spline. Specify the tension value to use. If set
        to ``True``, no tension will be used.
    hole : float
        Set the node value used to identify a point as a member of a hole [Default is
        NaN].
    mode : str
        Specify the hole-filling algorithm to use. Choose from **c** for constant fill
        and append the constant value, **n** for nearest neighbor (and optionally append
        a search radius in pixels [default radius is :math:`r^2 = \sqrt{{ X^2 + Y^2 }}`,
        where (*X,Y*) are the node dimensions of the grid]), or **s** for bicubic spline
        (optionally append a *tension* parameter [Default is no tension]).

        .. deprecated:: v0.15.0
            The ``mode`` parameter is deprecated since v0.15.0 and will be removed in
            v0.19.0. Use ``constantfill/gridfill/neighborfill/splinefill`` instead.
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

    # Determine the -A option from the fill parameters.
    kwargs["A"] = _parse_fill_mode(constantfill, gridfill, neighborfill, splinefill)

    if kwargs.get("A") is None and kwargs.get("L") is None:
        msg = "At least parameter 'mode' or 'L' must be specified."
        raise GMTInvalidInput(msg)

    with Session() as lib:
        with (
            lib.virtualfile_in(check_kind="raster", data=grid) as vingrd,
            lib.virtualfile_in(
                check_kind="raster", data=gridfill, required_data=False
            ) as vbggrd,
            lib.virtualfile_out(kind="grid", fname=outgrid) as voutgrd,
        ):
            if gridfill is not None:
                # Fill by a grid. Append the actual or virtual grid file name.
                kwargs["A"] = f"g{vbggrd}"
            kwargs["G"] = voutgrd
            lib.call_module(
                module="grdfill", args=build_arg_list(kwargs, infile=vingrd)
            )
            return lib.virtualfile_to_raster(vfname=voutgrd, outgrid=outgrid)
