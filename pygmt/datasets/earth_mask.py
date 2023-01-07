"""
Function to download the GSHHG Global Earth Mask from the GMT data server, and
load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_earth_mask"]


@kwargs_to_strings(region="sequence")
def load_earth_mask(resolution="01d", region=None, registration=None):
    r"""
    Load the GSHHG Global Earth Mask in various resolutions.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_mask/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@earth_mask**\_\ *res*\[_\ *reg*] to any grid plotting/processing
    function. *res* is the grid resolution (see below), and *reg* is grid
    registration type (**p** for pixel registration or **g** for gridline
    registration).

    Refer to :gmt-datasets:`earth-mask.html` for more details.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d`` and ``m`` stand for
        arc-degrees and arc-minutes. It can be ``"01d"``, ``"30m"``,
        ``"20m"``, ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``, ``"04m"``,
        ``"03m"``, ``"02m"``, ``"01m"``, ``"30s"``, or ``"15s"``.

    region : str or list
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``"gridline"``.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth mask grid. Coordinates are latitude and
        longitude in degrees. Units are in integers for the surface type:

        - 0: Ocean
        - 1: Land
        - 2: Lake
        - 3: Island
        - 4: Pond
    """
    grid = _load_remote_dataset(
        dataset_name="earth_mask",
        dataset_prefix="earth_mask_",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
