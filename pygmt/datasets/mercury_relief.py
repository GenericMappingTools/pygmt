"""
Function to download the Mercury relief dataset from the GMT data server, and load as
:class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from typing import Literal

from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_mercury_relief"]


@kwargs_to_strings(region="sequence")
def load_mercury_relief(
    resolution="01d",
    region=None,
    registration: Literal["gridline", "pixel", None] = None,
):
    r"""
    Load the Mercury relief dataset in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_mercury_relief.jpg
       :width: 80%
       :align: center

       Mercury relief dataset.

    The grids are downloaded to a user data directory (usually
    ``~/.gmt/server/mercury/mercury_relief/``) the first time you invoke this function.
    Afterwards, it will load the grid from the data directory. So you'll need an
    internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@mercury_relief**\_\ *res*\[_\ *reg*] to any grid processing function or plotting
    method. *res* is the grid resolution (see below), and *reg* is the grid registration
    type (**p** for pixel registration or **g** for gridline registration).

    The default color palette table (CPT) for this dataset is *@mercury_relief.cpt*.
    It's implicitly used when passing in the file name of the dataset to any grid
    plotting method if no CPT is explicitly specified. When the dataset is loaded and
    plotted as an :class:`xarray.DataArray` object, the default CPT is ignored, and
    GMT's default CPT (*turbo*) is used. To use the dataset-specific CPT, you need to
    explicitly set ``cmap="@mercury_relief.cpt"``.

    Refer to :gmt-datasets:`mercury-relief.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d``, ``m`` and ``s`` stand for arc-degrees,
        arc-minutes and arc-seconds. It can be ``"01d"``, ``"30m"``, ``"20m"``,
        ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``, ``"04m"``, ``"03m"``, ``"02m"``,
        ``"01m"``, and ``"56s"``.
    region : str or list
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*. Required for
        grids with resolutions higher than 5 arc-minutes (i.e., ``"05m"``).
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, means
        ``"gridline"`` for all resolutions except for ``"56s"`` which is ``"pixel"``
        only.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Mercury relief grid. Coordinates are latitude and longitude in degrees.
        Relief is in meters.

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
    >>> from pygmt.datasets import load_mercury_relief
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_mercury_relief()
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_mercury_relief(resolution="30m", registration="gridline")
    >>> # load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_mercury_relief(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    """
    grid = _load_remote_dataset(
        name="mercury_relief",
        prefix="mercury_relief",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
