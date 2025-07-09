"""
Function to download the Earth relief datasets from the GMT data server, and load as
:class:`xarray.DataArray`.

The grids are available in various resolutions.
"""

from collections.abc import Sequence
from typing import Literal

import xarray as xr
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.exceptions import GMTValueError

__doctest_skip__ = ["load_earth_relief"]


def load_earth_relief(
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
        "03s",
        "01s",
    ] = "01d",
    region: Sequence[float] | str | None = None,
    registration: Literal["gridline", "pixel", None] = None,
    data_source: Literal["igpp", "gebco", "gebcosi", "synbath"] = "igpp",
    use_srtm: bool = False,
) -> xr.DataArray:
    r"""
    Load the Earth relief datasets (topography and bathymetry) in various resolutions.

    .. figure:: https://www.generic-mapping-tools.org/remote-datasets/_images/GMT_earth_gebco.jpg
       :width: 80 %
       :align: center

       Earth relief datasets (topography and bathymetry).


    This function downloads the dataset from the GMT data server, caches it in a user
    data directory (usually ``~/.gmt/server/earth/earth_relief``,
    ``~/.gmt/server/earth/earth_gebco``, ``~/.gmt/server/earth/earth_gebcosi``,
    ``~/.gmt/server/earth/earth_synbath``), and load the dataset as an
    :class:`xarray.DataArray`. An internet connection is required the first time around,
    but subsequent calls will load the dataset from the local data directory.

    The dataset can also be accessed by specifying a file name in any grid processing
    function or plotting method, using the following file name format:
    **@**\ *earth_relief_type*\_\ *res*\_\ *reg*. *earth_relief_type* is the GMT name
    for the dataset. The available options are **earth_relief**\, **earth_gebco**\,
    **earth_gebcosi**\, and **earth_synbath**\. *res* is the grid resolution; *reg* is
    the grid registration type (**p** for pixel registration, **g** for gridline
    registration). If *reg* is omitted (e.g., ``@earth_relief_01d``), the
    gridline-registered grid will be loaded for grid processing functions and the
    pixel-registered grid willcbe loaded for plotting functions. If *res* is also
    omitted (i.e., ``@earth_relief``), GMT automatically selects a suitable resolution
    based on the current region and projection settings.

    This dataset comes with a color palette table (CPT) file, ``geo``. To use the
    dataset-specific CPT when plotting the dataset, explicitly set ``cmap="geo"``,
    otherwise GMT's default CPT (*turbo*) will be used. If the dataset is referenced by
    the file name in a grid plotting method, the dataset-specific CPT file is used
    automatically unless another CPT is specified.

    Refer to :gmt-datasets:`earth-relief.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution
        The grid resolution. The suffix ``d``, ``m`` and ``s`` stand for arc-degrees,
        arc-minutes, and arc-seconds.
    region
        The subregion of the grid to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*] or an ISO country code. Required for grids with resolutions
        higher than 5 arc-minutes (i.e., ``"05m"``).
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, which means
        ``"gridline"`` for all resolutions except ``"15s"`` which is ``"pixel"``
        only.
    data_source
        Select the source for the Earth relief data. Available options are:

        - ``"igpp"``: IGPP Earth Relief. See
          :gmt-datasets:`earth-relief.html`.
        - ``"synbath"``: IGPP Earth Relief dataset that uses stastical
          properties of young seafloor to provide a more realistic relief
          of young areas with small seamounts.
        - ``"gebco"``: GEBCO Earth Relief with only observed relief and
          inferred relief via altimetric gravity. See
          :gmt-datasets:`earth-gebco.html`.
        - ``"gebcosi"``: GEBCO Earth Relief that gives sub-ice (si) elevations.
    use_srtm
        By default, the land-only SRTM tiles from NASA are used to generate the
        ``"03s"`` and ``"01s"`` grids, and the missing ocean values are filled
        by up-sampling the SRTM15 tiles which have a resolution of 15
        arc-seconds (i.e., ``"15s"``). If True, will only load the original
        land-only SRTM tiles. Only works when ``data_source="igpp"``.

    Returns
    -------
    grid
        The Earth relief grid. Coordinates are latitude and longitude in
        degrees. Relief is in meters.

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` grid can be accessed via the *gmt* accessor. Refer to
    :class:`pygmt.GMTDataArrayAccessor` for detailed explanations and limitations.

    Examples
    --------

    >>> from pygmt.datasets import load_earth_relief
    >>> # Load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_relief()
    >>> # Load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_relief(resolution="30m", registration="gridline")
    >>> # Load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_earth_relief(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    >>> # Load the original 3 arc-seconds land-only SRTM tiles from NASA
    >>> grid = load_earth_relief(
    ...     resolution="03s",
    ...     region=[135, 136, 35, 36],
    ...     registration="gridline",
    ...     use_srtm=True,
    ... )
    """
    # resolutions of original land-only SRTM tiles from NASA
    land_only_srtm_resolutions = ["03s", "01s"]

    # Map data source to prefix
    prefix = {
        "igpp": "earth_relief",
        "gebco": "earth_gebco",
        "gebcosi": "earth_gebcosi",
        "synbath": "earth_synbath",
    }.get(data_source)
    if prefix is None:
        raise GMTValueError(
            data_source,
            description="earth relief data source",
            choices=["igpp", "gebco", "gebcosi", "synbath"],
        )
    # Use SRTM or not.
    if use_srtm and resolution in land_only_srtm_resolutions:
        if data_source != "igpp":
            raise GMTValueError(
                data_source,
                description="data source",
                reason=(
                    "Option 'use_srtm=True' doesn't work with data source "
                    f"{data_source!r}. Please set 'data_source' to 'igpp'."
                ),
            )
        prefix = "srtm_relief"
    # Choose earth relief dataset
    match data_source:
        case "igpp" | "synbath":
            name = "earth_igpp"
        case "gebco" | "gebcosi":
            name = "earth_gebco"
    grid = _load_remote_dataset(
        name=name,
        prefix=prefix,
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
