"""
Function to download the Earth magnetic anomaly datasets from the GMT data server, and
load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.exceptions import GMTInvalidInput

__doctest_skip__ = ["load_earth_magnetic_anomaly"]


def load_earth_magnetic_anomaly(
    resolution: Literal[
        "01d", "30m", "20m", "15m", "10m", "06m", "05m", "04m", "03m", "02m"
    ] = "01d",
    region: Sequence[float] | str | None = None,
    registration: Literal["gridline", "pixel", None] = None,
    data_source: Literal["emag2", "emag2_4km", "wdmam"] = "emag2",
) -> xr.DataArray:
    r"""
    Load the Earth magnetic anomaly datasets in various resolutions.

    .. list-table::
       :widths: 50 50
       :header-rows: 1

       * - Earth Magnetic Anomaly Model (EMAG2)
         - World Digital Magnetic Anomaly Map (WDMAM)
       * - .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_mag.jpg
         - .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_wdmam.jpg

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_mag/``,
    ``~/.gmt/server/earth/earth_mag4km/``,
    or ``~/.gmt/server/earth/earth_wdmam/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@**\ *earth_mag_type*\_\ *res*\[_\ *reg*] to any grid processing
    function or plotting method. *earth_mag_type* is the GMT name
    for the dataset. The available options are **earth_mag**,
    **earth_mag4km**, and **earth_wdmam**. *res* is the grid resolution
    (see below), and *reg* is the grid registration type (**p** for pixel
    registration or **g** for gridline registration).

    The default color palette tables (CPTs) for this dataset are
    *@earth_mag.cpt* for ``data_source="emag2"`` and
    ``data_source="emag2_4km"``, and *@earth_wdmam.cpt* for
    ``data_source="wdmam"``. The dataset-specific CPT is implicitly used when
    passing in the file name of the dataset to any grid plotting method if no
    CPT is explicitly specified. When the dataset is loaded and plotted as an
    :class:`xarray.DataArray` object, the default CPT is ignored, and GMT's
    default CPT (*turbo*) is used. To use the dataset-specific CPT, you need to
    explicitly set ``cmap="@earth_mag.cpt"`` or ``cmap="@earth_wdmam.cpt"``.

    Refer to :gmt-datasets:`earth-mag.html`
    and :gmt-datasets:`earth-wdmam.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution
        The grid resolution. The suffix ``d`` and ``m`` stand for arc-degrees and
        arc-minutes. The resolution ``"02m"`` is not available for
        ``data_source="wdmam"``.
    region
        The subregion of the grid to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*] or an ISO country code. Required for grids with resolutions
        higher than 5 arc-minutes (i.e., ``"05m"``).
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, means
        ``"gridline"`` for all resolutions except ``"02m"`` for
        ``data_source="emag2"`` or ``data_source="emag2_4km"``, which are
        ``"pixel"`` only.
    data_source
        Select the source of the magnetic anomaly data. Available options are:

        - ``"emag2"``: EMAG2 Earth Magnetic Anomaly Model. It only includes
          data observed at sea level over oceanic regions.
          See :gmt-datasets:`earth-mag.html`.
        - ``"emag2_4km"``: Use a version of EMAG2 where all observations
          are relative to an altitude of 4 km above the geoid and include
          data over land.
        - ``"wdmam"``: World Digital Magnetic Anomaly Map (WDMAM).
          See :gmt-datasets:`earth-wdmam.html`.

    Returns
    -------
    grid
        The Earth magnetic anomaly grid. Coordinates are latitude and
        longitude in degrees. Units are in nano Tesla (nT).

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

    >>> from pygmt.datasets import load_earth_magnetic_anomaly
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_magnetic_anomaly()
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_magnetic_anomaly(resolution="30m", registration="gridline")
    >>> # load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_earth_magnetic_anomaly(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    >>> # load the 20 arc-minutes grid of the emag2_4km dataset
    >>> grid = load_earth_magnetic_anomaly(
    ...     resolution="20m", registration="gridline", data_source="emag2_4km"
    ... )
    >>> # load the 20 arc-minutes grid of the WDMAM dataset
    >>> grid = load_earth_magnetic_anomaly(
    ...     resolution="20m", registration="gridline", data_source="wdmam"
    ... )
    """
    # Map data source to prefix
    prefix = {
        "emag2": "earth_mag",
        "emag2_4km": "earth_mag4km",
        "wdmam": "earth_wdmam",
    }.get(data_source)
    if prefix is None:
        raise GMTInvalidInput(
            f"Invalid earth magnetic anomaly data source '{data_source}'. "
            "Valid values are 'emag2', 'emag2_4km', and 'wdmam'."
        )
    grid = _load_remote_dataset(
        name="earth_wdmam" if data_source == "wdmam" else "earth_mag",
        prefix=prefix,
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
