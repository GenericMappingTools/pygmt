"""
Functions to download the Earth relief datasets from the GMT data server.
The grids are available in various resolutions.
"""
import xarray as xr

from .. import which
from ..exceptions import GMTInvalidInput


def load_earth_relief(resolution="60m"):
    """
    Load Earth relief grids (topography and bathymetry) in various resolutions.

    The grids are downloaded to a user data directory (usually ``~/.gmt/``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    ``'@earth_relief_XXm'`` or ``'@earth_relief_XXs'`` to any grid
    plotting/processing function.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``m`` and ``s`` stand for arc-minute
        and arc-second. It can be ``'60m'``, ``'30m'``, ``'10m'``, ``'05m'``,
        ``'02m'``, ``'01m'``, ``'30s'`` or ``'15s'``.

    Returns
    -------
    grid : xarray.DataArray
        The Earth relief grid. Coordinates are latitude and longitude in
        degrees. Relief is in meters.

    """
    _is_valid_resolution(resolution)
    fname = which("@earth_relief_{}".format(resolution), download="u")
    grid = xr.open_dataarray(fname)
    # Add some metadata to the grid
    grid.name = "elevation"
    grid.attrs["long_name"] = "elevation relative to the geoid"
    grid.attrs["units"] = "meters"
    grid.attrs["vertical_datum"] = "EMG96"
    grid.attrs["horizontal_datum"] = "WGS84"
    # Remove the actual range because it gets outdated when indexing the grid,
    # which causes problems when exporting it to netCDF for usage on the
    # command-line.
    grid.attrs.pop("actual_range")
    for coord in grid.coords:
        grid[coord].attrs.pop("actual_range")
    return grid


def _is_valid_resolution(resolution):
    """
    Check if a resolution is valid for the global Earth relief grid.

    Parameters
    ----------
    resolution : str
        Same as the input for load_earth_relief

    Raises
    ------
    GMTInvalidInput
        If given resolution is not valid.

    Examples
    --------

    >>> _is_valid_resolution("60m")
    >>> _is_valid_resolution("5m")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Invalid Earth relief resolution '5m'.
    >>> _is_valid_resolution("15s")
    >>> _is_valid_resolution("01s")
    Traceback (most recent call last):
        ...
    pygmt.exceptions.GMTInvalidInput: Invalid Earth relief resolution '01s'.

    """
    valid_resolutions = ["{:02d}m".format(res) for res in [60, 30, 10, 5, 2, 1]]
    valid_resolutions.extend(["{:02d}s".format(res) for res in [30, 15]])
    if resolution not in valid_resolutions:
        raise GMTInvalidInput(
            "Invalid Earth relief resolution '{}'.".format(resolution)
        )


def _shape_from_resolution(resolution):
    """
    Calculate the shape of the global Earth relief grid given a resolution.

    Parameters
    ----------
    resolution : str
        Same as the input for load_earth_relief

    Returns
    -------
    shape : (nlat, nlon)
        The calculated shape.

    Examples
    --------

    >>> _shape_from_resolution('60m')
    (181, 361)
    >>> _shape_from_resolution('30m')
    (361, 721)
    >>> _shape_from_resolution('10m')
    (1081, 2161)
    >>> _shape_from_resolution('30s')
    (21601, 43201)
    >>> _shape_from_resolution('15s')
    (43201, 86401)

    """
    _is_valid_resolution(resolution)
    unit = resolution[2]
    if unit == "m":
        seconds = int(resolution[:2]) * 60
    elif unit == "s":
        seconds = int(resolution[:2])
    nlat = 180 * 60 * 60 // seconds + 1
    nlon = 360 * 60 * 60 // seconds + 1
    return (nlat, nlon)
