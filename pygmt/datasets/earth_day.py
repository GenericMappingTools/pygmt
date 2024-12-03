"""
Function to download the NASA Blue Marble image datasets from the GMT data server, and
load as :class:`xarray.DataArray`.

The images are available in various resolutions.
"""

import contextlib
from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset

with contextlib.suppress(ImportError):
    # rioxarray is needed to register the rio accessor
    import rioxarray  # noqa: F401

__doctest_skip__ = ["load_blue_marble"]


def load_blue_marble(
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
    resolution
        The image resolution. The suffix ``d``, ``m``, and ``s`` stand for arc-degrees,
        arc-minutes, and arc-seconds.
    region
        The subregion of the image to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*].

    Returns
    -------
    image
        The NASA Blue Marble image. Coordinates are latitude and longitude in degrees.

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` image can be accessed via the GMT accessors (i.e.,
    ``image.gmt.registration`` and ``image.gmt.gtype`` respectively). However, these
    properties may be lost after specific image operations (such as slicing) and will
    need to be manually set before passing the image to any PyGMT data processing or
    plotting functions. Refer to :class:`pygmt.GMTDataArrayAccessor` for detailed
    explanations and workarounds.

    Examples
    --------

    >>> from pygmt.datasets import load_blue_marble
    >>> # load the default image (pixel-registered 1 arc-degree image)
    >>> image = load_blue_marble()
    """
    image = _load_remote_dataset(
        name="earth_day",
        prefix="earth_day",
        resolution=resolution,
        region=region,
        registration="pixel",
    )
    # If rioxarray is installed, set the coordinate reference system
    if hasattr(image, "rio"):
        image = image.rio.write_crs(input_crs="OGC:CRS84")
    return image
