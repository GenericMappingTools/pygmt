"""
Function to download the GSHHG Earth Mask dataset from the GMT data server, and load as
:class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from typing import Literal

from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_earth_mask"]


@kwargs_to_strings(region="sequence")
def load_earth_mask(
    resolution="01d",
    region=None,
    registration: Literal["gridline", "pixel"] = "gridline",
):
    r"""
    Load the GSHHG Earth Mask dataset in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_mask.jpg
       :width: 80 %
       :align: center

       GSHHG Earth Mask dataset.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_mask/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@earth_mask**\_\ *res*\[_\ *reg*] to any grid processing function or
    plotting method. *res* is the grid resolution (see below), and *reg* is
    the grid registration type (**p** for pixel registration or **g** for
    gridline registration).

    Refer to :gmt-datasets:`earth-mask.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d``, ``m``, and ``s`` stand for
        arc-degrees, arc-minutes, and arc-seconds. It can be ``"01d"``,
        ``"30m"``, ``"20m"``, ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``,
        ``"04m"``, ``"03m"``, ``"02m"``, ``"01m"``, ``"30s"``, or ``"15s"``.

    region : str or list
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.

    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration.

    Returns
    -------
    grid : :class:`xarray.DataArray`
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
    :class:`xarray.DataArray` grid can be accessed via the GMT accessors
    (i.e., ``grid.gmt.registration`` and ``grid.gmt.gtype`` respectively).
    However, these properties may be lost after specific grid operations (such
    as slicing) and will need to be manually set before passing the grid to any
    PyGMT data processing or plotting functions. Refer to
    :class:`pygmt.GMTDataArrayAccessor` for detailed explanations and
    workarounds.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_mask
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_mask()
    >>> # location (120°E, 50°N) is in land area (1)
    >>> grid.sel(lon=120, lat=50).values
    array(1, dtype=int8)
    >>> # location (170°E, 50°N) is in oceanic area (0)
    >>> grid.sel(lon=170, lat=50).values
    array(0, dtype=int8)
    """
    grid = _load_remote_dataset(
        dataset_name="earth_mask",
        dataset_prefix="earth_mask_",
        resolution=resolution,
        region=region,
        registration=registration,
    )
    # `return grid.astype("int8")` doesn't work because grid encoding is lost.
    # See https://github.com/GenericMappingTools/pygmt/issues/2629.
    grid.data = grid.data.astype("int8")
    return grid
