"""
Function to download the NASA Blue Marble image datasets from the GMT data
server, and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_blue_marble"]


@kwargs_to_strings(region="sequence")
def load_blue_marble(resolution="01d", region=None):
    r"""
    Load NASA Blue Marble images in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_daynight.jpg
       :width: 80%
       :align: center

       Earth day/night dataset.

    The images are downloaded to a user data directory (usually
    ``~/.gmt/server/earth/earth_day/``) the first time you invoke this function.
    Afterwards, it will load the image from the data directory. So you'll need an
    internet connection the first time around.

    These images can also be accessed by passing in the file name
    **@earth_day**\_\ *res* to any image processing function or plotting method. *res*
    is the image resolution (see below).

    Refer to :gmt-datasets:`earth-daynight.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution : str
        The image resolution. The suffix ``d``, ``m``, and ``s`` stand for arc-degree,
        arc-minute, and arc-second. It can be ``"01d"``, ``"30m"``, ``"20m"``,
        ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``, ``"04m"``, ``"03m"``, ``"02m"``,
        ``"01m"``, or ``"30s"``.

    region : str or list
        The subregion of the image to load, in the form of a list [*xmin*, *xmax*,
        *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*. Required for images with
        resolutions higher than 5 arc-minutes (i.e., ``"05m"``).

    Returns
    -------
    image : :class:`xarray.DataArray`
        The NASA Blue Marble image. Coordinates are latitude and longitude in degrees.

    Examples
    --------

    >>> from pygmt.datasets import load_blue_marble
    >>> # load the default image (pixel-registered 1 arc-degree image)
    >>> image = load_blue_marble()
    """
    image = _load_remote_dataset(
        dataset_name="earth_day",
        dataset_prefix="earth_day_",
        resolution=resolution,
        region=region,
        registration="pixel",
    )
    return image
