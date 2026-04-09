"""
Function to download the NASA Black Marble image datasets from the GMT data server, and
load as :class:`xarray.DataArray`.

The images are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset

__doctest_skip__ = ["load_black_marble"]


def load_black_marble(
    resolution: Literal[
        "01d",
        "30m",
        "20m",
        "15m",
        "10m",
        "06m",
        "05m",
        "04m",
        "03m",
        "02m",
        "01m",
        "30s",
    ] = "01d",
    region: Sequence[float] | str | None = None,
) -> xr.DataArray:
    r"""
    Load NASA Black Marble images in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_daynight.jpg
       :width: 80%
       :align: center

       Earth day/night dataset.

    This function downloads the dataset from the GMT data server, caches it in a user
    data directory (usually ``~/.gmt/server/earth/earth_night/``), and load the dataset
    as an :class:`xarray.DataArray`. An internet connection is required the first time
    around, but subsequent calls will load the dataset from the local data directory.

    The dataset can also be accessed by specifying a file name in any grid processing
    function or plotting method, using the following file name format:
    **@earth_night**\_\ *res*. *res* is the grid resolution. If *res* is omitted (i.e.,
    ``@earth_night``), GMT automatically selects a suitable resolution based on the
    current region and projection settings.

    Refer to :gmt-datasets:`earth-daynight.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution
        The image resolution. The suffix ``d``, ``m``, and ``s`` stand for arc-degrees,
        arc-minutes, and arc-seconds.
    region
        The subregion of the image to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*].

    Returns
    -------
    image
        The NASA Black Marble image. Coordinates are latitude and longitude in degrees.

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` image can be accessed via the *gmt* accessor. Refer to
    :class:`pygmt.GMTDataArrayAccessor` for detailed explanations and limitations.

    Examples
    --------

    >>> from pygmt.datasets import load_black_marble
    >>> # Load the default image (pixel-registered 1 arc-degree image)
    >>> image = load_black_marble()
    """
    image = _load_remote_dataset(
        name="earth_night",
        prefix="earth_night",
        resolution=resolution,
        region=region,
        registration="pixel",
    )
    return image
