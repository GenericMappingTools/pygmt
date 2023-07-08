"""
Function to download the Earth relief datasets from the GMT data server, and
load as :class:`xarray.DataArray`.

The grids are available in various resolutions.
"""
from pygmt.datasets.load_remote_dataset import _load_remote_dataset
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import kwargs_to_strings

__doctest_skip__ = ["load_earth_relief"]


@kwargs_to_strings(region="sequence")
def load_earth_relief(
    resolution="01d",
    region=None,
    registration=None,
    data_source="igpp",
    use_srtm=False,
):
    r"""
    Load Earth relief grids (topography and bathymetry) in various resolutions.

    The grids are downloaded to a user data directory
    (usually ``~/.gmt/server/earth/earth_relief``,
    ``~/.gmt/server/earth/earth_gebco``, ``~/.gmt/server/earth/earth_gebcosi``,
    or ``~/.gmt/server/earth/earth_synbath``) the first time you
    invoke this function. Afterwards, it will load the grid from the data
    directory. So you'll need an internet connection the first time around.

    This module downloads the grids that can also be accessed by
    passing in the file name **@**\ *earth_relief_type*\_\ *res*\[_\ *reg*] to
    any grid plotting/processing function. *earth_relief_type* is the GMT name
    for the dataset. The available options are **earth_relief**\,
    **earth_gebco**\, **earth_gebcosi**\, and **earth_synbath**\. *res* is the
    grid resolution (see below), and *reg* is grid registration type
    (**p** for pixel registration or **g** for gridline registration).

    The default color palette table (CPT) for this dataset is *geo*.
    It's implicitly used when passing in the file name of the dataset to any
    grid plotting method if no CPT is explicitly specified. When the dataset
    is loaded and plotted as an :class:`xarray.DataArray` object, the default
    CPT is ignored and GMT's default CPT (*turbo*) is used. To use the
    dataset-specific CPT, you need to explicitly set ``cmap="geo"``.

    Refer to :gmt-datasets:`earth-relief.html` for more details about available
    datasets, including version information and references.

    Parameters
    ----------
    resolution : str
        The grid resolution. The suffix ``d``, ``m`` and ``s`` stand for
        arc-degrees, arc-minutes, and arc-seconds. It can be ``"01d"``,
        ``"30m"``, ``"20m"``, ``"15m"``, ``"10m"``, ``"06m"``, ``"05m"``,
        ``"04m"``, ``"03m"``, ``"02m"``, ``"01m"``, ``"30s"``, ``"15s"``,
        ``"03s"``, or ``"01s"``.

    region : str or list
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for Earth relief grids with resolutions higher than 5
        arc-minutes (i.e., ``"05m"``).

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``"gridline"``
        for all resolutions except ``"15s"`` which is ``"pixel"`` only.

    data_source : str
        Select the source for the Earth relief data. Available options are:

        - ``"igpp"``: IGPP Global Earth Relief [Default option]. See
          :gmt-datasets:`earth-relief.html`.

        - ``"synbath"``: IGPP Global Earth Relief dataset that uses
          stastical properties of young seafloor to provide a more realistic
          relief of young areas with small seamounts.

        - ``"gebco"``: GEBCO Global Earth Relief with only observed relief and
          inferred relief via altimetric gravity. See
          :gmt-datasets:`earth-gebco.html`.

        - ``"gebcosi"``: GEBCO Global Earth Relief that gives sub-ice (si)
          elevations.

    use_srtm : bool
        By default, the land-only SRTM tiles from NASA are used to generate the
        ``"03s"`` and ``"01s"`` grids, and the missing ocean values are filled
        by up-sampling the SRTM15 tiles which have a resolution of 15
        arc-seconds (i.e., ``"15s"``). If True, will only load the original
        land-only SRTM tiles. Only works when ``data_source="igpp"``.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth relief grid. Coordinates are latitude and longitude in
        degrees. Relief is in meters.

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

    >>> from pygmt.datasets import load_earth_relief
    >>> # load the default grid (gridline-registered 1 arc-degree grid)
    >>> grid = load_earth_relief()
    >>> # load the 30 arc-minutes grid with "gridline" registration
    >>> grid = load_earth_relief(resolution="30m", registration="gridline")
    >>> # load high-resolution (5 arc-minutes) grid for a specific region
    >>> grid = load_earth_relief(
    ...     resolution="05m",
    ...     region=[120, 160, 30, 60],
    ...     registration="gridline",
    ... )
    >>> # load the original 3 arc-seconds land-only SRTM tiles from NASA
    >>> grid = load_earth_relief(
    ...     resolution="03s",
    ...     region=[135, 136, 35, 36],
    ...     registration="gridline",
    ...     use_srtm=True,
    ... )
    """
    # resolutions of original land-only SRTM tiles from NASA
    land_only_srtm_resolutions = ["03s", "01s"]

    earth_relief_sources = {
        "igpp": "earth_relief_",
        "gebco": "earth_gebco_",
        "gebcosi": "earth_gebcosi_",
        "synbath": "earth_synbath_",
    }
    if data_source not in earth_relief_sources:
        raise GMTInvalidInput(
            f"Invalid earth relief data source '{data_source}'. "
            "Valid values are 'igpp', 'gebco', 'gebcosi' and 'synbath'."
        )
    # Choose earth relief data prefix
    if use_srtm and resolution in land_only_srtm_resolutions:
        if data_source == "igpp":
            dataset_prefix = "srtm_relief_"
        else:
            raise GMTInvalidInput(
                f"Option 'use_srtm=True' doesn't work with data source '{data_source}'."
                " Please set 'data_source' to 'igpp'."
            )
    else:
        dataset_prefix = earth_relief_sources[data_source]

    grid = _load_remote_dataset(
        dataset_name="earth_relief",
        dataset_prefix=dataset_prefix,
        resolution=resolution,
        region=region,
        registration=registration,
    )
    return grid
