"""
Function to download the IGPP Earth free-air anomaly dataset from the GMT data server,
and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset

__doctest_skip__ = ["load_earth_free_air_anomaly"]


def load_earth_free_air_anomaly(
    resolution: Literal[
        "01d", "30m", "20m", "15m", "10m", "06m", "05m", "04m", "03m", "02m", "01m"
    ] = "01d",
    region: Sequence[float] | str | None = None,
    registration: Literal["gridline", "pixel", None] = None,
) -> xr.DataArray:
    r"""
    Load the IGPP Earth free-air anomaly dataset in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_faa.jpg
       :width: 80 %
       :align: center

       IGPP Earth free-air anomaly dataset.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_faa/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@earth_faa**\_\ *res*\[_\ *reg*] to any grid processing function or
    plotting method. *res* is the grid resolution (see below), and *reg* is
    the grid registration type (**p** for pixel registration or **g** for
    gridline registration).

    The default color palette table (CPT) for this dataset is *@earth_faa.cpt*.
    It's implicitly used when passing in the file name of the dataset to any
    grid plotting method if no CPT is explicitly specified. When the dataset
    is loaded and plotted as an :class:`xarray.DataArray` object, the default
    CPT is ignored, and GMT's default CPT (*turbo*) is used. To use the
    dataset-specific CPT, you need to explicitly set ``cmap="@earth_faa.cpt"``.

    Refer to :gmt-datasets:`earth-faa.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution
        The grid resolution. The suffix ``d`` and ``m`` stand for arc-degrees and
        arc-minutes.
    region
        The subregion of the grid to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*] or an ISO country code. Required for grids with resolutions
        higher than 5 arc-minutes (i.e., ``"05m"``).
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, which means
        ``"gridline"`` for all resolutions except ``"01m"`` which is ``"pixel"``
        only.

    Returns
    -------
    grid
        The Earth free-air anomaly grid. Coordinates are latitude and
        longitude in degrees. Units are in mGal.

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

    >>> from pygmt.datasets import load_earth_free_air_anomaly
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_free_air_anomaly()
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_free_air_anomaly(resolution="30m", registration="gridline")
    >>> # load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_earth_free_air_anomaly(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    """
    grid = _load_remote_dataset(
        name="earth_faa",
        prefix="earth_faa",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
