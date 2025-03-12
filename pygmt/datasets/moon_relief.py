"""
Function to download the Moon relief dataset from the GMT data server, and load as
:class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset

__doctest_skip__ = ["load_moon_relief"]


def load_moon_relief(
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
        "14s",
    ] = "01d",
    region: Sequence[float] | str | None = None,
    registration: Literal["gridline", "pixel", None] = None,
) -> xr.DataArray:
    r"""
    Load the Moon relief dataset in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_moon_relief.jpg
       :width: 80%
       :align: center

       Moon relief dataset.

    This function downloads the dataset from the GMT data server, caches it in a user
    data directory (usually ``~/.gmt/server/moon/moon_relief/``), and load the dataset
    as an :class:`xarray.DataArray`. An internet connection is required the first time
    around, but subsequent calls will load the dataset from the local data directory.

    The dataset can also be accessed by specifying a file name in any grid processing
    function or plotting method, using the following file name format:
    **@moon_relief**\_\ *res*\_\ *reg*. *res* is the grid resolution; *reg* is the grid
    registration type (**p** for pixel registration, **g** for gridline registration).
    If *reg* is omitted (e.g., ``@moon_relief_01d``), the gridline-registered grid will
    be loaded for grid processing functions and the pixel-registered grid will be
    loaded for plotting functions. If *res* is also omitted (i.e., ``@moon_relief``),
    GMT automatically selects a suitable resolution based on the current region and
    projection settings.

    This dataset comes with a color palette table (CPT) file, ``@moon_relief.cpt``. To
    use the dataset-specific CPT when plotting the dataset, explicitly set
    ``cmap="@moon_relief.cpt"``, otherwise GMT's default CPT (*turbo*) will be used. If
    the dataset is referenced by the file name in a grid plotting method, the
    dataset-specific CPT file is used automatically unless another CPT is specified.

    Refer to :gmt-datasets:`moon-relief.html` for more details about available datasets,
    including version information and references.

    Parameters
    ----------
    resolution
        The grid resolution. The suffix ``d``, ``m`` and ``s`` stand for arc-degrees,
        arc-minutes and arc-seconds. Note that ``"14s"`` refers to a resolution of
        14.0625 arc-seconds.
    region
        The subregion of the grid to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*] or an ISO country code. Required for grids with resolutions
        higher than 5 arc-minutes (i.e., ``"05m"``).
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, which means
        ``"gridline"`` for all resolutions except for ``"14s"`` which is ``"pixel"``
        only.

    Returns
    -------
    grid
        The Moon relief grid. Coordinates are latitude and longitude in degrees. Relief
        is in meters.

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` grid can be accessed via the GMT accessors (i.e.,
    ``grid.gmt.registration`` and ``grid.gmt.gtype`` respectively). However, these
    properties may be lost after specific grid operations (such as slicing) and will
    need to be manually set before passing the grid to any PyGMT data processing or
    plotting functions. Refer to :class:`pygmt.GMTDataArrayAccessor` for detailed
    explanations and workarounds.

    Examples
    --------
    >>> from pygmt.datasets import load_moon_relief
    >>> # Load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_moon_relief()
    >>> # Load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_moon_relief(resolution="30m", registration="gridline")
    >>> # Load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_moon_relief(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    """
    grid = _load_remote_dataset(
        name="moon_relief",
        prefix="moon_relief",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
