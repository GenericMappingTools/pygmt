"""
Function to download the Earth relief datasets from the GMT data server,
and load as DataArray. The grids are available in various resolutions.
"""
import xarray as xr

from .. import grdcut, which
from ..exceptions import GMTInvalidInput
from ..helpers import kwargs_to_strings


@kwargs_to_strings(region="sequence")
def load_earth_relief(resolution="01d", region=None, registration=None):
    """
    Load Earth relief grids (topography and bathymetry) in various resolutions.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_relief/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    ``'@earth_relief_rru[_reg]'`` to any grid plotting/processing function.
    Refer to :gmt-docs:`datasets/remote-data.html` for more details.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d``, ``m`` and ``s`` stand for
        arc-degree, arc-minute and arc-second. It can be ``'01d'``, ``'30m'``,
        ``'20m'``, ``'15m'``, ``'10m'``, ``'06m'``, ``'05m'``, ``'04m'``,
        ``'03m'``, ``'02m'``, ``'01m'``, ``'30s'``, ``'15s'``, ``'03s'``,
        or ``'01s'``.

    region : str or list
        The subregion of the grid to load. Required for Earth relief grids with
        resolutions <= 05m.

    registration : str
        Grid registration type. Either ``pixel`` for pixel registration or
        ``gridline`` for gridline registration. Default is ``None``, where
        a pixel-registered grid is returned unless only the
        gridline-registered grid is available.

    Returns
    -------
    grid : xarray.DataArray
        The Earth relief grid. Coordinates are latitude and longitude in
        degrees. Relief is in meters.

    Notes
    -----
    The DataArray doesn's support slice operation, for Earth relief data with
    resolutions higher than "05m", which are stored as smaller tiles.

    Examples
    --------

    >>> # load the default grid (pixel-registered 01d grid)
    >>> grid = load_earth_relief()
    >>> # load the 30m grid with "gridline" registration
    >>> grid = load_earth_relief("30m", registration="gridline")
    >>> # load high-resolution grid for a specific region
    >>> grid = load_earth_relief(
    ...     "05m", region=[120, 160, 30, 60], registration="gridline"
    ... )

    """

    # earth relief data stored as single grids for low resolutions
    non_tiled_resolutions = ["01d", "30m", "20m", "15m", "10m", "06m"]
    # earth relief data stored as tiles for high resolutions
    tiled_resolutions = ["05m", "04m", "03m", "02m", "01m", "30s", "15s", "03s", "01s"]

    if registration in ("pixel", "gridline", None):
        # If None, let GMT decide on Pixel/Gridline type
        reg = f"_{registration[0]}" if registration else ""
    else:
        raise GMTInvalidInput(
            f"Invalid grid registration: {registration}, should be either "
            "'pixel', 'gridline' or None. Default is None, where a "
            "pixel-registered grid is returned unless only the "
            "gridline-registered grid is available."
        )

    # different ways to load tiled and non-tiled earth relief data
    if resolution in non_tiled_resolutions:
        if region is not None:
            raise NotImplementedError(
                f"'region' is not supported for Earth relief resolution '{resolution}'"
            )
        fname = which(f"@earth_relief_{resolution}{reg}", download="a")
        with xr.open_dataarray(fname) as dataarray:
            grid = dataarray.load()
            _ = grid.gmt  # load GMTDataArray accessor information
    elif resolution in tiled_resolutions:
        # Titled grid can't be sliced.
        # See https://github.com/GenericMappingTools/pygmt/issues/524
        if region is None:
            raise GMTInvalidInput(
                f"'region' is required for Earth relief resolution '{resolution}'"
            )
        grid = grdcut(f"@earth_relief_{resolution}{reg}", region=region)
    else:
        raise GMTInvalidInput(f'Invalid Earth relief resolution "{resolution}"')

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
