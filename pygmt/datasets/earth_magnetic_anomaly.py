"""
Function to download the Earth magnetic anomaly datasets from the GMT data
server, and load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_earth_magnetic_anomaly"]


@kwargs_to_strings(region="sequence")
def load_earth_magnetic_anomaly(
    resolution="01d", region=None, registration=None, data_source="emag2"
):
    r"""
    Load an Earth magnetic anomaly grid in various resolutions.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_mag/``,
    ``~/.gmt/server/earth/earth_mag4km/``,
    or ``~/.gmt/server/earth/earth_wdmam/``) the first time you invoke
    this function. Afterwards, it will load the grid from the data directory.
    So you'll need an internet connection the first time around.

    These grids can also be accessed by passing in the file name
    **@**\ *earth_mag_type*\_\ *res*\[_\ *reg*] to any grid plotting/processing
    function. *earth_mag_type* is the GMT name
    for the dataset. The available options are **earth_mag**,
    **earth_mag4km**, and **earth_wdmam**. *res* is the grid resolution
    (see below), and *reg* is grid registration type (**p** for pixel
    registration or **g** for gridline registration).

    Refer to :gmt-datasets:`earth-mag.html`
    and :gmt-datasets:`earth-wdmam.html` for more details.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d`` and ``m`` stand for
        arc-degrees and arc-minutes. It can be ``"01d"``, ``"30m"``,
        ``"20m"``, ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``, ``"04m"``,
        ``"03m"``, or ``"02m"``.

    region : str or list
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for grids with resolutions higher than 5
        arc-minutes (i.e., ``"05m"``).

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``"gridline"``
        for all resolutions except ``"02m"`` which is ``"pixel"`` only.

    data_source : str
        Select the source of the magnetic anomaly data.

        Available options:

        - **emag2** : EMAG2 Global Earth Magnetic Anomaly Model [Default
          option]. Only includes data is observed from sea level over
          oceanic regions. See :gmt-datasets:`earth-mag.html`.

        - **emag2_4km** : Use a version of EMAG2 where all observations
          are relative to an altitude of 4 km above the geoid and include
          data over land.

        - **wdmam** : World Digital Magnetic Anomaly Map (WDMAM).
          See :gmt-datasets:`earth-wdmam.html`

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth magnetic anomaly grid. Coordinates are latitude and
        longitude in degrees. Units are in nano Teslas (nT).

    Note
    ----
    The :class:`xarray.DataArray` grid doesn't support slice operation, for
    Earth magnetic anomaly with resolutions of 5 arc-minutes or higher,
    which are stored as smaller tiles.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_magnetic_anomaly
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_magnetic_anomaly()
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_magnetic_anomaly(
    ...     resolution="30m", registration="gridline"
    ... )
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
    magnetic_anomaly_sources = {
        "emag2": "earth_mag_",
        "emag2_4km": "earth_mag4km_",
        "wdmam": "earth_wdmam_",
    }
    if data_source not in magnetic_anomaly_sources:
        raise GMTInvalidInput(
            f"Invalid earth magnetic anomaly 'data_source' {data_source}, "
            "valid values are 'emag2', 'emag2_4km', and 'wdmam'."
        )
    dataset_prefix = magnetic_anomaly_sources[data_source]
    if data_source == "wdmam":
        dataset_name = "earth_wdmam"
    else:
        dataset_name = "earth_magnetic_anomaly"
    grid = _load_remote_dataset(
        dataset_name=dataset_name,
        dataset_prefix=dataset_prefix,
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
