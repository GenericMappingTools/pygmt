"""
Internal function to load GMT remote datasets.
"""
from typing import Dict, NamedTuple

from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import kwargs_to_strings
from pygmt.io import load_dataarray
from pygmt.src import grdcut, which


class Resolution(NamedTuple):
    """
    The available grid registrations for a given resolution and whether it is a
    tiled grid.

    Attributes
    ----------
    registrations : list
        A list of the accepted registrations for a given resolution.
        Can be either "pixel" or "gridline".

    tiled : bool
        States if the given resolution is tiled, which requires an
        argument for ``region``."
    """

    registrations: list
    tiled: bool


class GMTRemoteDataset(NamedTuple):
    """
    Standard information about a dataset and grid metadata.

    Attributes
    ----------
    title : str
        The title of the dataset, used in error messages.

    name : str
        The name assigned as an attribute to the DataArray.

    long_name : str
        The long name assigned as an attribute to the DataArray.

    units : str
        The units of the values in the DataArray.

    resolutions : dict
        Dictionary of available resolution as keys and the values are
        Resolution objects.

    extra_attributes : dict
        A dictionary of extra or unique attributes of the dataset.
    """

    title: str
    name: str
    long_name: str
    units: str
    resolutions: Dict[str, Resolution]
    extra_attributes: dict


datasets = {
    "earth_age": GMTRemoteDataset(
        title="seafloor age",
        name="seafloor_age",
        long_name="age of seafloor crust",
        units="Myr",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["gridline", "pixel"], False),
            "30m": Resolution(["gridline", "pixel"], False),
            "20m": Resolution(["gridline", "pixel"], False),
            "15m": Resolution(["gridline", "pixel"], False),
            "10m": Resolution(["gridline", "pixel"], False),
            "06m": Resolution(["gridline", "pixel"], False),
            "05m": Resolution(["gridline", "pixel"], True),
            "04m": Resolution(["gridline", "pixel"], True),
            "03m": Resolution(["gridline", "pixel"], True),
            "02m": Resolution(["gridline", "pixel"], True),
            "01m": Resolution(["gridline"], True),
        },
    ),
    "earth_free_air_anomaly": GMTRemoteDataset(
        title="free air anomaly",
        name="free_air_anomaly",
        long_name="IGPP Global Earth Free-Air Anomaly",
        units="mGal",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["gridline", "pixel"], False),
            "30m": Resolution(["gridline", "pixel"], False),
            "20m": Resolution(["gridline", "pixel"], False),
            "15m": Resolution(["gridline", "pixel"], False),
            "10m": Resolution(["gridline", "pixel"], False),
            "06m": Resolution(["gridline", "pixel"], False),
            "05m": Resolution(["gridline", "pixel"], True),
            "04m": Resolution(["gridline", "pixel"], True),
            "03m": Resolution(["gridline", "pixel"], True),
            "02m": Resolution(["gridline", "pixel"], True),
            "01m": Resolution(["pixel"], True),
        },
    ),
    "earth_geoid": GMTRemoteDataset(
        title="Earth geoid",
        name="earth_geoid",
        long_name="EGM2008 Global Earth Geoid",
        units="m",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["gridline", "pixel"], False),
            "30m": Resolution(["gridline", "pixel"], False),
            "20m": Resolution(["gridline", "pixel"], False),
            "15m": Resolution(["gridline", "pixel"], False),
            "10m": Resolution(["gridline", "pixel"], False),
            "06m": Resolution(["gridline", "pixel"], False),
            "05m": Resolution(["gridline", "pixel"], True),
            "04m": Resolution(["gridline", "pixel"], True),
            "03m": Resolution(["gridline", "pixel"], True),
            "02m": Resolution(["gridline", "pixel"], True),
            "01m": Resolution(["gridline"], True),
        },
    ),
    "earth_magnetic_anomaly": GMTRemoteDataset(
        title="Earth magnetic anomaly",
        name="magnetic_anomaly",
        long_name="Earth magnetic anomaly",
        units="nT",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["gridline", "pixel"], False),
            "30m": Resolution(["gridline", "pixel"], False),
            "20m": Resolution(["gridline", "pixel"], False),
            "15m": Resolution(["gridline", "pixel"], False),
            "10m": Resolution(["gridline", "pixel"], False),
            "06m": Resolution(["gridline", "pixel"], False),
            "05m": Resolution(["gridline", "pixel"], True),
            "04m": Resolution(["gridline", "pixel"], True),
            "03m": Resolution(["gridline", "pixel"], True),
            "02m": Resolution(["pixel"], True),
        },
    ),
    "earth_relief": GMTRemoteDataset(
        title="Earth relief",
        name="elevation",
        long_name="Earth elevation relative to the geoid",
        units="meters",
        extra_attributes={"vertical_datum": "EGM96", "horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["gridline", "pixel"], False),
            "30m": Resolution(["gridline", "pixel"], False),
            "20m": Resolution(["gridline", "pixel"], False),
            "15m": Resolution(["gridline", "pixel"], False),
            "10m": Resolution(["gridline", "pixel"], False),
            "06m": Resolution(["gridline", "pixel"], False),
            "05m": Resolution(["gridline", "pixel"], True),
            "04m": Resolution(["gridline", "pixel"], True),
            "03m": Resolution(["gridline", "pixel"], True),
            "02m": Resolution(["gridline", "pixel"], True),
            "01m": Resolution(["gridline", "pixel"], True),
            "30s": Resolution(["gridline", "pixel"], True),
            "15s": Resolution(["pixel"], True),
            "03s": Resolution(["gridline"], True),
            "01s": Resolution(["gridline"], True),
        },
    ),
    "earth_vgg": GMTRemoteDataset(
        title="Earth vertical gravity gradient",
        name="earth_vgg",
        long_name="IGPP Global Earth Vertical Gravity Gradient",
        units="Eotvos",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["gridline", "pixel"], False),
            "30m": Resolution(["gridline", "pixel"], False),
            "20m": Resolution(["gridline", "pixel"], False),
            "15m": Resolution(["gridline", "pixel"], False),
            "10m": Resolution(["gridline", "pixel"], False),
            "06m": Resolution(["gridline", "pixel"], False),
            "05m": Resolution(["gridline", "pixel"], True),
            "04m": Resolution(["gridline", "pixel"], True),
            "03m": Resolution(["gridline", "pixel"], True),
            "02m": Resolution(["gridline", "pixel"], True),
            "01m": Resolution(["pixel"], True),
        },
    ),
    "earth_wdmam": GMTRemoteDataset(
        title="WDMAM magnetic anomaly",
        name="wdmam",
        long_name="World Digital Magnetic Anomaly Map",
        units="nT",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["gridline", "pixel"], False),
            "30m": Resolution(["gridline", "pixel"], False),
            "20m": Resolution(["gridline", "pixel"], False),
            "15m": Resolution(["gridline", "pixel"], False),
            "10m": Resolution(["gridline", "pixel"], False),
            "06m": Resolution(["gridline", "pixel"], False),
            "05m": Resolution(["gridline", "pixel"], True),
            "04m": Resolution(["gridline", "pixel"], True),
            "03m": Resolution(["gridline"], True),
        },
    ),
}


@kwargs_to_strings(region="sequence")
def _load_remote_dataset(
    dataset_name, dataset_prefix, resolution, region, registration
):
    r"""
    Load GMT remote datasets.

    Parameters
    ----------
    dataset_name : str
        The name for the dataset in the 'datasets' dictionary.

    dataset_prefix : str
        The prefix for the dataset that will be passed to the GMT C API.

    resolution : str
        The grid resolution. The suffix ``d``, ``m``, and ``s`` stand for
        arc-degrees, arc-minutes, and arc-seconds, respectively.

    region : str or list
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for tiled grids.

    registration : str
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, where
        a pixel-registered grid is returned unless only the
        gridline-registered grid is available.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The GMT remote dataset grid.

    Note
    ----
    The returned :class:`xarray.DataArray` doesn't support slice operation for
    tiled grids.
    """
    dataset = datasets[dataset_name]
    if resolution not in dataset.resolutions.keys():
        raise GMTInvalidInput(f"Invalid resolution '{resolution}'.")
    if registration is None:
        # Check if "gridline" is an available registration for the resolution
        if "gridline" in dataset.resolutions[resolution].registrations:
            # Use default of gridline registration if available
            registration = "gridline"
        else:
            registration = "pixel"
    if registration in ("pixel", "gridline"):
        reg = f"_{registration[0]}"
    else:
        raise GMTInvalidInput(
            f"Invalid grid registration: '{registration}', should be either "
            "'pixel', 'gridline' or None. Default is None, where a "
            "gridline-registered grid is returned unless only the "
            "pixel-registered grid is available."
        )

    if registration and (
        registration not in dataset.resolutions[resolution].registrations
    ):
        raise GMTInvalidInput(
            f"{registration} registration is not available for the "
            f"{resolution} {dataset.title} dataset. Only "
            f"{dataset.resolutions[resolution].registrations[0]}"
            " registration is available."
        )

    # different ways to load tiled and non-tiled grids.
    # Known issue: tiled grids don't support slice operation
    # See https://github.com/GenericMappingTools/pygmt/issues/524
    if region is None:
        if dataset.resolutions[resolution].tiled:
            raise GMTInvalidInput(
                f"'region' is required for {dataset.title}"
                f"resolution '{resolution}'."
            )
        fname = which(f"@{dataset_prefix}{resolution}{reg}", download="a")
        grid = load_dataarray(fname, engine="netcdf4")
    else:
        grid = grdcut(f"@{dataset_prefix}{resolution}{reg}", region=region)

    # Add some metadata to the grid
    grid.name = dataset.name
    grid.attrs["long_name"] = dataset.long_name
    grid.attrs["units"] = dataset.units
    for key, value in dataset.extra_attributes.items():
        grid.attrs[key] = value
    # Remove the actual range because it gets outdated when indexing the grid,
    # which causes problems when exporting it to netCDF for usage on the
    # command-line.
    grid.attrs.pop("actual_range")
    for coord in grid.coords:
        grid[coord].attrs.pop("actual_range")
    return grid
