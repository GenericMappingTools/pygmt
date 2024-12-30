"""
Internal function to load GMT remote datasets.
"""

from collections.abc import Sequence
from typing import Any, Literal, NamedTuple

import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import build_arg_list, kwargs_to_strings
from pygmt.src import which


class Resolution(NamedTuple):
    """
    Resolution code, the available grid registrations and whether it is tiled.

    Attributes
    ----------
    code
        The resolution code. E.g., "01d", "30m", "01s".
    registrations
        A list of the accepted registrations for a given resolution. Can be either
        "pixel" or "gridline".
    tiled
        States if the grid is tiled, which requires an argument for ``region``.
    """

    code: str
    registrations: Sequence[str] = ["gridline", "pixel"]
    tiled: bool = False


class GMTRemoteDataset(NamedTuple):
    """
    Standard information about a dataset and grid metadata.

    Attributes
    ----------
    description
       The name assigned as an attribute to the DataArray.
    units
        The units of the values in the DataArray.
    resolutions
        Dictionary of available resolution as keys and Resolution objects as values.
    extra_attributes
        A dictionary of extra or unique attributes of the dataset.
    """

    description: str
    units: str | None
    resolutions: dict[str, Resolution]
    extra_attributes: dict[str, Any]


datasets = {
    "earth_age": GMTRemoteDataset(
        description="EarthByte Earth seafloor crustal age",
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
    "earth_day": GMTRemoteDataset(
        description="NASA Day Images",
        units=None,
        extra_attributes={"long_name": "blue_marble", "horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d", registrations=["pixel"]),
            "30m": Resolution("30m", registrations=["pixel"]),
            "20m": Resolution("20m", registrations=["pixel"]),
            "15m": Resolution("15m", registrations=["pixel"]),
            "10m": Resolution("10m", registrations=["pixel"]),
            "06m": Resolution("06m", registrations=["pixel"]),
            "05m": Resolution("05m", registrations=["pixel"]),
            "04m": Resolution("04m", registrations=["pixel"]),
            "03m": Resolution("03m", registrations=["pixel"]),
            "02m": Resolution("02m", registrations=["pixel"]),
            "01m": Resolution("01m", registrations=["pixel"]),
            "30s": Resolution("30s", registrations=["pixel"]),
        },
    ),
    "earth_dist": GMTRemoteDataset(
        description="GSHHG Earth distance to shoreline",
        units="kilometers",
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
    "earth_faa": GMTRemoteDataset(
        description="IGPP Earth free-air anomaly",
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
    "earth_faaerror": GMTRemoteDataset(
        description="IGPP Earth free-air anomaly errors",
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
    "earth_gebco": GMTRemoteDataset(
        description="GEBCO Earth relief",
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
    "earth_geoid": GMTRemoteDataset(
        description="EGM2008 Earth geoid",
        units="meters",
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
    "earth_igpp": GMTRemoteDataset(
        description="IGPP Earth relief",
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
    "earth_mag": GMTRemoteDataset(
        description="EMAG2 Earth Magnetic Anomaly Model",
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
        description="GSHHG Earth mask",
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
    "earth_mss": GMTRemoteDataset(
        description="CNES Earth mean sea surface",
        units="meters",
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
            "01m": Resolution("01m", tiled=True, registrations=["gridline"]),
        },
    ),
    "earth_night": GMTRemoteDataset(
        description="NASA Night Images",
        units=None,
        extra_attributes={"long_name": "black_marble", "horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d", registrations=["pixel"]),
            "30m": Resolution("30m", registrations=["pixel"]),
            "20m": Resolution("20m", registrations=["pixel"]),
            "15m": Resolution("15m", registrations=["pixel"]),
            "10m": Resolution("10m", registrations=["pixel"]),
            "06m": Resolution("06m", registrations=["pixel"]),
            "05m": Resolution("05m", registrations=["pixel"]),
            "04m": Resolution("04m", registrations=["pixel"]),
            "03m": Resolution("03m", registrations=["pixel"]),
            "02m": Resolution("02m", registrations=["pixel"]),
            "01m": Resolution("01m", registrations=["pixel"]),
            "30s": Resolution("30s", registrations=["pixel"]),
        },
    ),
    "earth_mdt": GMTRemoteDataset(
        description="CNES Earth mean dynamic topography",
        units="meters",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution("01d"),
            "30m": Resolution("30m"),
            "20m": Resolution("20m"),
            "15m": Resolution("15m"),
            "10m": Resolution("10m"),
            "07m": Resolution("07m", registrations=["gridline"]),
        },
    ),
    "earth_vgg": GMTRemoteDataset(
        description="IGPP Earth vertical gravity gradient",
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
        description="WDMAM World Digital Magnetic Anomaly Map",
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
        description="NASA Mars (MOLA) relief",
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
        description="USGS Moon (LOLA) relief",
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
        description="USGS Mercury relief",
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
        description="USGS Pluto relief",
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
        description="NASA Magellan Venus relief",
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
    name: str,
    prefix: str,
    resolution: str,
    region: Sequence[float] | str | None,
    registration: Literal["gridline", "pixel", None],
) -> xr.DataArray:
    r"""
    Load GMT remote datasets.

    Parameters
    ----------
    name
        The name for the dataset in the 'datasets' dictionary.
    prefix
        The prefix for the dataset that will be passed to the GMT C API.
    resolution
        The grid resolution. The suffix ``d``, ``m``, and ``s`` stand for arc-degrees,
        arc-minutes, and arc-seconds, respectively.
    region
        The subregion of the grid to load, in the form of a sequence [*xmin*, *xmax*,
        *ymin*, *ymax*] or an ISO country code. Required for tiled grids.
    registration
        Grid registration type. Either ``"pixel"`` for pixel registration or
        ``"gridline"`` for gridline registration. Default is ``None``, where
        a gridline-registered grid is returned unless only the pixel-registered grid
        is available.

    Returns
    -------
    grid
        The GMT remote dataset grid.

    Note
    ----
    The registration and coordinate system type of the returned
    :class:`xarray.DataArray` grid can be accessed via the GMT accessors (i.e.,
    ``grid.gmt.registration`` and ``grid.gmt.gtype`` respectively). However, these
    properties may be lost after specific grid operations (such as slicing) and will
    need to be manually set before passing the grid to any PyGMT data processing or
    plotting functions. Refer to :class:`pygmt.GMTDataArrayAccessor` for detailed
    explanations and workarounds.
    """
    dataset = datasets[name]

    # Check resolution
    if resolution not in dataset.resolutions:
        msg = (
            f"Invalid resolution '{resolution}' for {dataset.description} dataset. "
            f"Available resolutions are: {', '.join(dataset.resolutions)}."
        )
        raise GMTInvalidInput(msg)
    resinfo = dataset.resolutions[resolution]

    # Check registration
    match registration:
        case None:
            # Use gridline registration unless only pixel registration is available
            reg = "g" if "gridline" in resinfo.registrations else "p"
        case x if x not in resinfo.registrations:
            msg = (
                f"Invalid grid registration '{registration}' for the {resolution} "
                f"{dataset.description} dataset. Should be either 'pixel', 'gridline' "
                "or None. Default is None, where a gridline-registered grid is "
                "returned unless only the pixel-registered grid is available."
            )
            raise GMTInvalidInput(msg)
        case _:
            reg = registration[0]

    if resinfo.tiled and region is None:
        msg = (
            f"The 'region' parameter is required for {dataset.description} "
            f"resolution '{resolution}'."
        )
        raise GMTInvalidInput(msg)

    fname = f"@{prefix}_{resolution}_{reg}"
    kind = "image" if name in {"earth_day", "earth_night"} else "grid"
    kwdict = {"R": region, "T": {"grid": "g", "image": "i"}[kind]}
    with Session() as lib:
        with lib.virtualfile_out(kind=kind) as voutgrd:
            lib.call_module(
                module="read",
                args=[fname, voutgrd, *build_arg_list(kwdict)],
            )
            grid = lib.virtualfile_to_raster(kind=kind, outgrid=None, vfname=voutgrd)

    # Full path to the grid if not tiled grids.
    source = which(fname, download="a") if not resinfo.tiled else None
    # Manually add source to xarray.DataArray encoding to make the GMT accessors work.
    if source:
        grid.encoding["source"] = source

    # Add some metadata to the grid
    grid.attrs["description"] = dataset.description
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
