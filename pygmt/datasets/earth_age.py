"""
Function to download the Earth seafloor age datasets from the GMT data server,
and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import kwargs_to_strings
from pygmt.io import load_dataarray
from pygmt.src import grdcut, which


@kwargs_to_strings(region="sequence")
def load_earth_age(resolution="01d", region=None, registration=None):
    r"""
    Load Earth seafloor crustal ages in various resolutions.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_age/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@earth_age**\_\ *res*\[_\ *reg*] to any grid plotting/processing
    function. *res* is the grid resolution (see below), and *reg* is grid
    registration type (**p** for pixel registration or **g** for gridline
    registration).

    Refer to :gmt-datasets:`earth-age.html` for more details.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d`` and ``m`` stand for
        arc-degree, arc-minute and arc-second. It can be ``'01d'``, ``'30m'``,
        ``'20m'``, ``'15m'``, ``'10m'``, ``'06m'``, ``'05m'``, ``'04m'``,
        ``'03m'``, ``'02m'``, or ``'01m'``.

    region : str or list
        The subregion of the grid to load, in the forms of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for grids with resolutions higher than 5
        arc-minute (i.e., ``05m``).

    registration : str
        Grid registration type. Either ``pixel`` for pixel registration or
        ``gridline`` for gridline registration. Default is ``None``, where
        a pixel-registered grid is returned unless only the
        gridline-registered grid is available.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth seafloor crustal age grid. Coordinates are latitude and
        longitude in degrees. Age is in millions of years (Myr).

    Note
    ----
    The :class:`xarray.DataArray` grid doesn't support slice operation, for
    Earth seafloor crustal age with resolutions of 5 arc-minutes or higher,
    which are stored as smaller tiles.
    """

    # earth seafloor crust age data stored as single grids for low resolutions
    non_tiled_resolutions = ["01d", "30m", "20m", "15m", "10m", "06m"]
    # earth seafloor crust age data stored as tiles for high resolutions
    tiled_resolutions = ["05m", "04m", "03m", "02m", "01m"]

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

    # Choose earth relief data prefix
    earth_age_prefix = "earth_age_"

    # different ways to load tiled and non-tiled earth relief data
    # Known issue: tiled grids don't support slice operation
    # See https://github.com/GenericMappingTools/pygmt/issues/524
    if region is None:
        if resolution not in non_tiled_resolutions:
            raise GMTInvalidInput(
                f"'region' is required for Earth age resolution '{resolution}'."
            )
        fname = which(f"@earth_age_{resolution}{reg}", download="a")
        grid = load_dataarray(fname, engine="netcdf4")
    else:
        grid = grdcut(f"@{earth_age_prefix}{resolution}{reg}", region=region)

    # Add some metadata to the grid
    grid.name = "seafloor_age"
    grid.attrs["long_name"] = "age of seafloor crust"
    grid.attrs["units"] = "Myr"
    grid.attrs["vertical_datum"] = "EMG96"
    grid.attrs["horizontal_datum"] = "WGS84"
    # Remove the actual range because it gets outdated when indexing the grid,
    # which causes problems when exporting it to netCDF for usage on the
    # command-line.
    grid.attrs.pop("actual_range")
    for coord in grid.coords:
        grid[coord].attrs.pop("actual_range")
    return grid
