"""
Functions to download the Earth relief datasets from the GMT data sever.
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
    ``'@earth_relief_XXm'`` to any grid plotting/processing function. Higher
    resolution SRTM grids can be accessed by using the ``'@earth_relief_XXs'``
    special file names but they cannot be loaded using this function.

    Parameters
    ----------
    resolution : str
        The grid resolution. The prefix ``m`` stands for arc-minute. It can be
        ``'60m'``, ``'30m'``, ``'10m'``, ``'05m'``, ``'02m'``, or ``'01m'``.

    Returns
    -------
    grid :  xarray.DataArray
        The Earth relief grid. Coordinates are latitude and longitude in
        degrees. Relief is in meters.

    """
    valid_resolutions = ["{:02d}m".format(res) for res in [60, 30, 10, 5, 2, 1]]
    if resolution not in valid_resolutions:
        raise GMTInvalidInput(
            "Invalid Earth relief resolution '{}'.".format(resolution)
        )
    fname = which("@earth_relief_{}".format(resolution), download="u")
    grid = xr.open_dataarray(fname)
    return grid


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

    """
    minutes = int(resolution[:2])
    nlat = 180 * 60 // minutes + 1
    nlon = 360 * 60 // minutes + 1
    return (nlat, nlon)
