"""
Function to download the GSHHG Earth Mask dataset from the GMT data server, and load as
:class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset

__doctest_skip__ = ["load_earth_mask"]


def load_earth_mask(
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
        "15s",
    ] = "01d",
    region: Sequence[float] | str | None = None,
    registration: Literal["gridline", "pixel"] = "gridline",
) -> xr.DataArray:
    r"""
    Load the GSHHG Earth mask dataset in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_mask.jpg
       :width: 80 %
       :align: center

       GSHHG Earth mask dataset.

    This function downloads the dataset from the GMT data server, caches it in a user
    data directory (usually ``~/.gmt/server/earth/earth_mask/``), and load the dataset
    as an :class:`xarray.DataArray`. An internet connection is required the first time
    around, but subsequent calls will load the dataset from the local data directory.

    The dataset can also be accessed by specifying a file name in any grid processing
    function or plotting method, using the following file name format:
    **@earth_mask**\_\ *res*\_\ *reg*. *res* is the grid resolution; *reg* is the grid
    registration type (**p** for pixel registration, **g** for gridline registration).
    If *reg* is omitted (e.g., ``@earth_mask_01d``), the gridline-registered grid will
    be loaded for grid processing functions and the pixel-registered grid will be
    loaded for plotting functions. If *res* is also omitted (i.e., ``@earth_mask``), GMT
    automatically selects a suitable resolution based on the current region and
    projection settings.

    Refer to :gmt-datasets:`earth-mask.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution
        The grid resolution. The suffix ``d``, ``m``, and ``s`` stand for arc-degrees,
        arc-minutes, and arc-seconds.
    region
        The subregion of the grid to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*] or an ISO country code.
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration.

    Returns
    -------
    grid
        The Earth mask grid. Coordinates are latitude and
        longitude in degrees. The node values in the mask grids are all in
        the 0-4 range and reflect different surface types:

        - 0: Oceanic areas beyond the shoreline
        - 1: Land areas inside the shoreline
        - 2: Lakes inside the land areas
        - 3: Islands in lakes in the land areas
        - 4: Smaller lakes in islands that are found within lakes
          inside the land area

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` grid can be accessed via the *gmt* accessor. Refer to
    :class:`pygmt.GMTDataArrayAccessor` for detailed explanations and limitations.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_mask
    >>> # Load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_mask()
    >>> # location (120°E, 50°N) is in land area (1)
    >>> grid.sel(lon=120, lat=50).values
    array(1, dtype=int8)
    >>> # location (170°E, 50°N) is in oceanic area (0)
    >>> grid.sel(lon=170, lat=50).values
    array(0, dtype=int8)
    """
    grid = _load_remote_dataset(
        name="earth_mask",
        prefix="earth_mask",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    # `return grid.astype("int8")` doesn't work because grid encoding is lost.
    # See https://github.com/GenericMappingTools/pygmt/issues/2629.
    grid.data = grid.data.astype("int8")
    return grid
