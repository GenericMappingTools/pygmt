"""
Function to download the Earth seafloor age datasets from the GMT data server,
and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.datasets.load_earth_dataset import _load_earth_dataset
from pygmt.helpers import kwargs_to_strings


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
        arc-degree and arc-minute. It can be ``"01d"``, ``"30m"``,
        ``"20m"``, ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``, ``"04m"``,
        ``"03m"``, ``"02m"``, or ``"01m"``.

    region : str or list
        The subregion of the grid to load, in the forms of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for grids with resolutions higher than 5
        arc-minute (i.e., ``"05m"``).

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, where
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
    # resolutions only in one registration
    pixel_only_resolutions = None
    gridline_only_resolutions = ["01m"]

    # Choose earth age data prefix
    dataset_name = "Earth age"
    dataset_prefix = "earth_age_"

    grid = _load_earth_dataset(
        resolution=resolution,
        region=region,
        registration=registration,
        non_tiled_resolutions=non_tiled_resolutions,
        tiled_resolutions=tiled_resolutions,
        dataset_prefix=dataset_prefix,
        dataset_name=dataset_name,
        pixel_only_resolutions=pixel_only_resolutions,
        gridline_only_resolutions=gridline_only_resolutions,
    )

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
