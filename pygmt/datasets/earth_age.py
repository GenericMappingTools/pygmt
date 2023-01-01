"""
Function to download the Earth seafloor age datasets from the GMT data server,
and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_earth_age"]


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
        arc-degrees and arc-minutes. It can be ``"01d"``, ``"30m"``,
        ``"20m"``, ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``, ``"04m"``,
        ``"03m"``, ``"02m"``, or ``"01m"``.

    region : str or list
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for grids with resolutions higher than 5
        arc-minutes (i.e., ``"05m"``).

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``"gridline"``.

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

    Examples
    --------

    >>> from pygmt.datasets import load_earth_age
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_age()
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_age(resolution="30m", registration="gridline")
    >>> # load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_earth_age(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    """
    dataset_prefix = "earth_age_"
    dataset_name = "earth_age"
    grid = _load_remote_dataset(
        dataset_name=dataset_name,
        dataset_prefix=dataset_prefix,
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
