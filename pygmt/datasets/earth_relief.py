"""
Function to download the Earth relief datasets from the GMT data server, and
load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
import xarray as xr
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import kwargs_to_strings
from pygmt.src import grdcut, which


@kwargs_to_strings(region="sequence")
def load_earth_relief(resolution="01d", region=None, registration=None, use_srtm=False):
    r"""
    Load Earth relief grids (topography and bathymetry) in various resolutions.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_relief/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@earth_relief**\_\ *res*\[_\ *reg*] to any grid plotting/processing
    function. *res* is the grid resolution (see below), and *reg* is grid
    registration type (**p** for pixel registration or **g** for gridline
    registration).

    Refer to :gmt-docs:`datasets/remote-data.html#global-earth-relief-grids`
    for more details.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d``, ``m`` and ``s`` stand for
        arc-degree, arc-minute and arc-second. It can be ``'01d'``, ``'30m'``,
        ``'20m'``, ``'15m'``, ``'10m'``, ``'06m'``, ``'05m'``, ``'04m'``,
        ``'03m'``, ``'02m'``, ``'01m'``, ``'30s'``, ``'15s'``, ``'03s'``,
        or ``'01s'``.

    region : str or list
        The subregion of the grid to load, in the forms of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for Earth relief grids with resolutions higher than 5
        arc-minute (i.e., ``05m``).

    registration : str
        Grid registration type. Either ``pixel`` for pixel registration or
        ``gridline`` for gridline registration. Default is ``None``, where
        a pixel-registered grid is returned unless only the
        gridline-registered grid is available.

    use_srtm : bool
        By default, the land-only SRTM tiles from NASA are used to generate the
        ``'03s'`` and ``'01s'`` grids, and the missing ocean values are filled
        by up-sampling the SRTM15+V2.1 tiles which have a resolution of 15
        arc-second (i.e., ``'15s'``). If True, will only load the original
        land-only SRTM tiles.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth relief grid. Coordinates are latitude and longitude in
        degrees. Relief is in meters.

    Notes
    -----
    The :class:`xarray.DataArray` grid doesn't support slice operation, for
    Earth relief data with resolutions higher than "05m", which are stored as
    smaller tiles.

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
    >>> # load the original 3 arc-second land-only SRTM tiles from NASA
    >>> grid = load_earth_relief(
    ...     "03s",
    ...     region=[135, 136, 35, 36],
    ...     registration="gridline",
    ...     use_srtm=True,
    ... )
    """

    # earth relief data stored as single grids for low resolutions
    non_tiled_resolutions = ["01d", "30m", "20m", "15m", "10m", "06m"]
    # earth relief data stored as tiles for high resolutions
    tiled_resolutions = ["05m", "04m", "03m", "02m", "01m", "30s", "15s", "03s", "01s"]
    # resolutions of original land-only SRTM tiles from NASA
    land_only_srtm_resolutions = ["03s", "01s"]

    if registration in ("pixel", "gridline", None):
        # If None, let GMT decide on Pixel/Gridline type
        reg = f"_{registration[0]}" if registration else ""
    else:
        raise GMTInvalidInput(
            f"Invalid grid registration: '{registration}', should be either "
            "'pixel', 'gridline' or None. Default is None, where a "
            "pixel-registered grid is returned unless only the "
            "gridline-registered grid is available."
        )

    if resolution not in non_tiled_resolutions + tiled_resolutions:
        raise GMTInvalidInput(f"Invalid Earth relief resolution '{resolution}'.")

    # Check combination of resolution and registration.
    if (resolution == "15s" and registration == "gridline") or (
        resolution in ("03s", "01s") and registration == "pixel"
    ):
        raise GMTInvalidInput(
            f"{registration}-registered Earth relief data for "
            f"resolution '{resolution}' is not supported."
        )

    # Choose earth relief data prefix
    earth_relief_prefix = "earth_relief_"
    if use_srtm and resolution in land_only_srtm_resolutions:
        earth_relief_prefix = "srtm_relief_"

    # different ways to load tiled and non-tiled earth relief data
    # Known issue: tiled grids don't support slice operation
    # See https://github.com/GenericMappingTools/pygmt/issues/524
    if region is None:
        if resolution not in non_tiled_resolutions:
            raise GMTInvalidInput(
                f"'region' is required for Earth relief resolution '{resolution}'."
            )
        fname = which(f"@earth_relief_{resolution}{reg}", download="a")
        with xr.open_dataarray(fname, engine="netcdf4") as dataarray:
            grid = dataarray.load()
            _ = grid.gmt  # load GMTDataArray accessor information
    else:
        grid = grdcut(f"@{earth_relief_prefix}{resolution}{reg}", region=region)

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
