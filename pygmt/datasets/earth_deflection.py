"""
Function to download the IGPP Earth east-west and north-south deflection datasets from
the GMT data server, and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset

__doctest_skip__ = ["load_earth_deflection"]


def load_earth_deflection(
    resolution: Literal[
        "01d", "30m", "20m", "15m", "10m", "06m", "05m", "04m", "03m", "02m", "01m"
    ] = "01d",
    region: Sequence[float] | str | None = None,
    registration: Literal["gridline", "pixel", None] = None,
    component: Literal["east", "north"] = "east",
) -> xr.DataArray:
    r"""
    Load the IGPP Earth east-west and north-south deflection datasets in various
    resolutions.

    .. list-table::
       :widths: 50 50
       :header-rows: 1

       * - IGPP Earth east-west deflection
         - IGPP Earth north-south deflection
       * - .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_edefl.jpg
         - .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_ndefl.jpg


    This function downloads the dataset from the GMT data server, caches it in a user
    data directory (usually ``~/.gmt/server/earth/earth_edefl/`` and
    ``~/.gmt/server/earth/earth_ndefl/``), and load the dataset as an
    :class:`xarray.DataArray`. An internet connection is required the first time around,
    but subsequent calls will load the dataset from the local data directory.

    The datasets can also be accessed by specifying a file name in any grid processing
    function or plotting method, using the following file name format:
    **@**\ *earth_defl_type*\_\ *res*\_\ *reg*. *earth_defl_type* is the GMT name for
    the dataset. The available options are **earth_edefl** and **earth_ndefl**; *res* is
    the grid resolution; *reg* is the grid registration type (**p** for pixel
    registration, **g** for gridline registration). If *reg* is omitted (e.g.,
    ``@earth_edefl_01d``), the gridline-registered grid will be loaded for grid
    processing functions and the pixel-registered grid will be loaded for plotting
    functions. If *res* is also omitted (i.e., ``@earth_edefl``), GMT automatically
    selects a suitable resolution based on the current region and projection settings.

    This dataset comes with a color palette table (CPT) file, ``@earth_defl.cpt``. To
    use the dataset-specific CPT when plotting the dataset, explicitly set
    ``cmap="@earth_defl.cpt"``, otherwise GMT's default CPT (*turbo*) will be used. If
    the dataset is referenced by the file name in a grid plotting method, the
    dataset-specific CPT file is used automatically unless another CPT is specified.

    Refer to :gmt-datasets:`earth-edefl.html` and :gmt-datasets:`earth-ndefl.html` for
    more details about available datasets, including version information and references.

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
        ``"gridline"`` for all resolutions except ``"01m"`` which is ``"pixel"`` only.
    component
        By default, the east-west deflection (``component="east"``) is returned,
       set  ``component="north"`` to return the north-south deflection.

    Returns
    -------
    grid
        The Earth east-west or north-south deflection grid. Coordinates are latitude
        and longitude in degrees. Deflection values are in micro-radians, where
        positive (negative) values indicate a deflection to the east or north (west
        or south).

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` grid can be accessed via the *gmt* accessor. Refer to
    :class:`pygmt.GMTDataArrayAccessor` for detailed explanations and limitations.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_deflection
    >>> # Load the default grid for east-west deflection (gridline-registered
    >>> # 1 arc-degree grid)
    >>> grid = load_earth_deflection()
    >>> # Load the default grid for north-south deflection
    >>> grid = load_earth_deflection(component="north")
    >>> # Load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_deflection(resolution="30m", registration="gridline")
    >>> # Load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_earth_deflection(
    ...     resolution="05m", region=[120, 160, 30, 60], registration="gridline"
    ... )
    """
    prefix = "earth_ndefl" if component == "north" else "earth_edefl"
    grid = _load_remote_dataset(
        name=prefix,
        prefix=prefix,
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
