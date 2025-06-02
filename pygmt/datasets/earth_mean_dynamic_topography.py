"""
Function to download the CNES Earth mean dynamic topography dataset from the GMT data
server, and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset

__doctest_skip__ = ["load_earth_mean_dynamic_topography"]


def load_earth_mean_dynamic_topography(
    resolution: Literal["01d", "30m", "20m", "15m", "10m", "07m"] = "01d",
    region: Sequence[float] | str | None = None,
    registration: Literal["gridline", "pixel"] = "gridline",
) -> xr.DataArray:
    r"""
    Load the CNES Earth mean dynamic topography dataset in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_mdt.jpg
       :width: 80 %
       :align: center

       CNES Earth mean dynamic topography dataset.

    This function downloads the dataset from the GMT data server, caches it in a user
    data directory (usually ``~/.gmt/server/earth/earth_mdt/``), and load the dataset as
    an :class:`xarray.DataArray`. An internet connection is required the first time
    around, but subsequent calls will load the dataset from the local data directory.

    The dataset can also be accessed by specifying a file name in any grid processing
    function or plotting method, using the following file name format:
    **@earth_mdt**\_\ *res*\_\ *reg*. *res* is the grid resolution; *reg* is the grid
    registration type (**p** for pixel registration, **g** for gridline registration).
    If *reg* is omitted (e.g., ``@earth_mdt_01d``), the gridline-registered grid will be
    loaded for grid processing functions and the pixel-registered grid will be loaded
    for plotting functions. If *res* is also omitted (i.e., ``@earth_mdt``), GMT
    automatically selects a suitable resolution based on the current region and
    projection settings.

    This dataset comes with a color palette table (CPT) file, ``@earth_mdt.cpt``. To use
    the dataset-specific CPT when plotting the dataset, explicitly set
    ``cmap="@earth_mdt.cpt"``, otherwise GMT's default CPT (*turbo*) will be used. If
    the dataset is referenced by the file name in a grid plotting method, the
    dataset-specific CPT file is used automatically unless another CPT is specified.

    Refer to :gmt-datasets:`earth-mdt.html` for more details about available datasets,
    including version information and references.

    Parameters
    ----------
    resolution
        The grid resolution. The suffix ``d`` and ``m`` stand for arc-degrees and
        arc-minutes. Note that ``"07m"`` refers to a resolution of 7.5 arc-minutes.
    region
        The subregion of the grid to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*] or an ISO country code.
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration.

    Returns
    -------
    grid
        The CNES Earth mean dynamic topography grid. Coordinates are latitude and
        longitude in degrees. Values are in meters.

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` grid can be accessed via the *gmt* accessor. Refer to
    :class:`pygmt.GMTDataArrayAccessor` for detailed explanations and limitations.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_mean_dynamic_topography
    >>> # Load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_mean_dynamic_topography()
    >>> # Load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_mean_dynamic_topography(
    ...     resolution="30m", registration="gridline"
    ... )
    >>> # Load high-resolution (7 arc-minutes) grid for a specific region
    >>> grid = load_earth_mean_dynamic_topography(
    ...     resolution="07m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    """
    grid = _load_remote_dataset(
        name="earth_mdt",
        prefix="earth_mdt",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
