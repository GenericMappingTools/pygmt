"""
Internal function to load GMT remote datasets.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, NamedTuple

from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import kwargs_to_strings
from pygmt.io import load_dataarray
from pygmt.src import grdcut, which

if TYPE_CHECKING:
    import xarray as xr


class Resolution(NamedTuple):
    """
    Resolution code, the available grid registrations and whether it is tiled.

    Attributes
    ----------
    code : str
        The resolution code. E.g., "01d", "30m", "01s".
    registrations : list
        A list of the accepted registrations for a given resolution. Can be either
        "pixel" or "gridline".
    tiled : bool
        States if the grid is tiled, which requires an argument for ``region``.
    """

    code: str
    registrations: ClassVar[list] = ["gridline", "pixel"]
    tiled: bool = False


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
        Dictionary of available resolution as keys and Resolution objects as values.
    extra_attributes : dict
        A dictionary of extra or unique attributes of the dataset.
    """

    title: str
    name: str
    long_name: str
    units: str | None
    resolutions: dict[str, Resolution]
    extra_attributes: dict


datasets = {
    "earth_age": GMTRemoteDataset(
        title="seafloor age",
        name="seafloor_age",
        long_name="age of seafloor crust",
        units="Myr",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", registrations=["gridline"], tiled=True),
        },
    ),
    "earth_free_air_anomaly": GMTRemoteDataset(
        title="free air anomaly",
        name="free_air_anomaly",
        long_name="IGPP Earth Free-Air Anomaly",
        units="mGal",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", registrations=["pixel"], tiled=True),
        },
    ),
    "earth_geoid": GMTRemoteDataset(
        title="Earth geoid",
        name="earth_geoid",
        long_name="EGM2008 Earth Geoid",
        units="m",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", registrations=["gridline"], tiled=True),
        },
    ),
    "earth_magnetic_anomaly": GMTRemoteDataset(
        title="Earth magnetic anomaly",
        name="magnetic_anomaly",
        long_name="Earth magnetic anomaly",
        units="nT",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", registrations=["pixel"], tiled=True),
        },
    ),
    "earth_mask": GMTRemoteDataset(
        title="Earth mask",
        name="earth_mask",
        long_name="Mask of land and water features",
        units=None,
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m"),
            "04m": Resolution("04m"),
            "03m": Resolution("03m"),
            "02m": Resolution("02m"),
            "01m": Resolution("01m"),
            "30s": Resolution("30s"),
            "15s": Resolution("15s"),
        },
    ),
    "earth_relief": GMTRemoteDataset(
        title="Earth relief",
        name="elevation",
        long_name="Earth elevation relative to the geoid",
        units="meters",
        extra_attributes={"vertical_datum": "EGM96", "horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", tiled=True),
            "30s": Resolution("30s", tiled=True),
            "15s": Resolution("15s", registrations=["pixel"], tiled=True),
            "03s": Resolution("03s", registrations=["gridline"], tiled=True),
            "01s": Resolution("01s", registrations=["gridline"], tiled=True),
        },
    ),
    "earth_vgg": GMTRemoteDataset(
        title="Earth vertical gravity gradient",
        name="earth_vgg",
        long_name="IGPP Earth Vertical Gravity Gradient",
        units="Eotvos",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", registrations=["pixel"], tiled=True),
        },
    ),
    "earth_wdmam": GMTRemoteDataset(
        title="WDMAM magnetic anomaly",
        name="wdmam",
        long_name="World Digital Magnetic Anomaly Map",
        units="nT",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", registrations=["gridline"], tiled=True),
        },
    ),
    "mars_relief": GMTRemoteDataset(
        title="Mars relief",
        name="mars_relief",
        long_name="NASA Mars (MOLA) relief",
        units="meters",
        extra_attributes={},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", tiled=True),
            "30s": Resolution("30s", tiled=True),
            "15s": Resolution("15s", tiled=True),
            "12s": Resolution("12s", registrations=["pixel"], tiled=True),
        },
    ),
    "moon_relief": GMTRemoteDataset(
        title="Moon relief",
        name="moon_relief",
        long_name="USGS Moon (LOLA) relief",
        units="meters",
        extra_attributes={},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", tiled=True),
            "30s": Resolution("30s", tiled=True),
            "15s": Resolution("15s", tiled=True),
            "14s": Resolution("14s", registrations=["pixel"], tiled=True),
        },
    ),
    "mercury_relief": GMTRemoteDataset(
        title="Mercury relief",
        name="mercury_relief",
        long_name="USGS Mercury relief",
        units="meters",
        extra_attributes={},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", tiled=True),
            "56s": Resolution("56s", registrations=["pixel"], tiled=True),
        },
    ),
    "pluto_relief": GMTRemoteDataset(
        title="Pluto relief",
        name="pluto_relief",
        long_name="USGS Pluto relief",
        units="meters",
        extra_attributes={},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", tiled=True),
            "52s": Resolution("52s", registrations=["pixel"], tiled=True),
        },
    ),
    "venus_relief": GMTRemoteDataset(
        title="Venus relief",
        name="venus_relief",
        long_name="NASA Magellan Venus relief",
        units="meters",
        extra_attributes={},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "06m": Resolution("06m"),
            "05m": Resolution("05m", tiled=True),
            "04m": Resolution("04m", tiled=True),
            "03m": Resolution("03m", tiled=True),
            "02m": Resolution("02m", tiled=True),
            "01m": Resolution("01m", registrations=["gridline"], tiled=True),
        },
    ),
}


@kwargs_to_strings(region="sequence")
def _load_remote_dataset(
    dataset_name: str,
    dataset_prefix: str,
    resolution: str,
    region: str | list,
    registration: str,
) -> xr.DataArray:
    r"""
    Load GMT remote datasets.

    Parameters
    ----------
    dataset_name
        The name for the dataset in the 'datasets' dictionary.
    dataset_prefix
        The prefix for the dataset that will be passed to the GMT C API.
    resolution
        The grid resolution. The suffix ``d``, ``m``, and ``s`` stand for arc-degrees,
        arc-minutes, and arc-seconds, respectively.
    region
        The subregion of the grid to load, in the form of a list
        [*xmin*, *xmax*, *ymin*, *ymax*] or a string *xmin/xmax/ymin/ymax*.
        Required for tiled grids.
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, where
        a gridline-registered grid is returned unless only the pixel-registered grid
        is available.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The GMT remote dataset grid.

    Note
    ----
    The returned :class:`xarray.DataArray` doesn't support slice operation for tiled
    grids.
    """
    dataset = datasets[dataset_name]

    if resolution not in dataset.resolutions:
        raise GMTInvalidInput(
            f"Invalid resolution '{resolution}' for {dataset.title} dataset. "
            f"Available resolutions are: {', '.join(dataset.resolutions)}."
        )

    # check registration
    valid_registrations = dataset.resolutions[resolution].registrations
    if registration is None:
        # use gridline registration unless only pixel registration is available
        registration = "gridline" if "gridline" in valid_registrations else "pixel"
    elif registration in ("pixel", "gridline"):
        if registration not in valid_registrations:
            raise GMTInvalidInput(
                f"{registration} registration is not available for the "
                f"{resolution} {dataset.title} dataset. Only "
                f"{valid_registrations[0]} registration is available."
            )
    else:
        raise GMTInvalidInput(
            f"Invalid grid registration: '{registration}', should be either 'pixel', "
            "'gridline' or None. Default is None, where a gridline-registered grid is "
            "returned unless only the pixel-registered grid is available."
        )
    reg = f"_{registration[0]}"

    # different ways to load tiled and non-tiled grids.
    # Known issue: tiled grids don't support slice operation
    # See https://github.com/GenericMappingTools/pygmt/issues/524
    if region is None:
        if dataset.resolutions[resolution].tiled:
            raise GMTInvalidInput(
                f"'region' is required for {dataset.title} resolution '{resolution}'."
            )
        fname = which(f"@{dataset_prefix}{resolution}{reg}", download="a")
        grid = load_dataarray(fname, engine="netcdf4")
    else:
        grid = grdcut(f"@{dataset_prefix}{resolution}{reg}", region=region)

    # Add some metadata to the grid
    grid.name = dataset.name
    grid.attrs["long_name"] = dataset.long_name
    if dataset.units:
        grid.attrs["units"] = dataset.units
    for key, value in dataset.extra_attributes.items():
        grid.attrs[key] = value
    # Remove the actual range because it gets outdated when indexing the grid, which
    # causes problems when exporting it to netCDF for usage on the command-line.
    grid.attrs.pop("actual_range", None)
    for coord in grid.coords:
        grid[coord].attrs.pop("actual_range", None)
    return grid
