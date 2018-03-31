"""
Functions to download the Earth relief datasets from the GMT data sever.
The grids are available in various resolutions.
"""
import xarray as xr

from .. import which


def load_earth_relief(resolution='60m'):
    """
    Load Earth relief grids (topography and bathimetry) in various resolutions.

    The grids are downloaded to a user data directory (usually ``~/.gmt/``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    ``'@earth_relief_XXm'`` to any grid plotting/processing function.
    Lower resolutions SRTM grids can be accessed by using '@earth_relief_XXs'
    but they cannot be loaded using this function.

    Parameters
    ----------
    resolution : str
        The grid resolution. The prefix ``m`` stands for arc-minute. It can be
        ``'60m'``, ``'30m'``, ``'10m'``, ``'05m'``, ``'02m'``, or ``'01m'``.

    Returns
    -------
    grid :  xarray.DataArray
        The Earth relief grid.

    """
    valid_resolutions = ['{:02d}m'.format(res)
                         for res in [60, 30, 10, 5, 2, 1]]
    if resolution not in valid_resolutions:
        raise
    fname = which('@earth_relief_{}'.format(resolution), download='u')
    return fname
