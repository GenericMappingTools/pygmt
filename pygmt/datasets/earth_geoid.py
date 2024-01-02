"""
Function to download the EGM2008 Earth Geoid dataset from the GMT data server, and load
as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from typing import Literal

from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_earth_geoid"]


@kwargs_to_strings(region="sequence")
def load_earth_geoid(
    resolution="01d",
    region=None,
    registration: Literal["gridline", "pixel"] = "gridline",
):
    r"""
    Load the EGM2008 Earth Geoid dataset in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_geoid.jpg
       :width: 80 %
       :align: center

       EGM2008 Earth Geoid dataset.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_geoid/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@earth_geoid**\_\ *res*\[_\ *reg*] to any grid processing function or
    plotting method. *res* is the grid resolution (see below), and *reg* is
    the grid registration type (**p** for pixel registration or **g** for
    gridline registration).

    Refer to :gmt-datasets:`earth-geoid.html` for more details about available
    datasets, including version information and references.

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

    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth geoid grid. Coordinates are latitude and
        longitude in degrees. Units are in meters.

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` grid can be accessed via the GMT accessors
    (i.e., ``grid.gmt.registration`` and ``grid.gmt.gtype`` respectively).
    However, these properties may be lost after specific grid operations (such
    as slicing) and will need to be manually set before passing the grid to any
    PyGMT data processing or plotting functions. Refer to
    :class:`pygmt.GMTDataArrayAccessor` for detailed explanations and
    workarounds.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_geoid
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_geoid()
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_geoid(resolution="30m", registration="gridline")
    >>> # load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_earth_geoid(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    """
    grid = _load_remote_dataset(
        dataset_name="earth_geoid",
        dataset_prefix="earth_geoid_",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
