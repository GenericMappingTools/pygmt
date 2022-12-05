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
    "earth_relief": GMTRemoteDataset(
        title="Earth relief",
        name="elevation",
        long_name="Earth elevation relative to the geoid",
        units="meters",
        extra_attributes={"vertical_datum": "EGM96", "horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["pixel", "gridline"], False),
            "30m": Resolution(["pixel", "gridline"], False),
            "20m": Resolution(["pixel", "gridline"], False),
            "15m": Resolution(["pixel", "gridline"], False),
            "10m": Resolution(["pixel", "gridline"], False),
            "06m": Resolution(["pixel", "gridline"], False),
            "05m": Resolution(["pixel", "gridline"], True),
            "04m": Resolution(["pixel", "gridline"], True),
            "03m": Resolution(["pixel", "gridline"], True),
            "02m": Resolution(["pixel", "gridline"], True),
            "01m": Resolution(["pixel", "gridline"], True),
            "30s": Resolution(["pixel", "gridline"], True),
            "15s": Resolution(["pixel"], True),
            "03s": Resolution(["gridline"], True),
            "01s": Resolution(["gridline"], True),
        },
    ),
    "earth_age": GMTRemoteDataset(
        title="seafloor age",
        name="seafloor_age",
        long_name="age of seafloor crust",
        units="Myr",
        extra_attributes={"horizontal_datum": "WGS84"},
        resolutions={
            "01d": Resolution(["pixel", "gridline"], False),
            "30m": Resolution(["pixel", "gridline"], False),
            "20m": Resolution(["pixel", "gridline"], False),
            "15m": Resolution(["pixel", "gridline"], False),
            "10m": Resolution(["pixel", "gridline"], False),
            "06m": Resolution(["pixel", "gridline"], False),
            "05m": Resolution(["pixel", "gridline"], True),
            "04m": Resolution(["pixel", "gridline"], True),
            "03m": Resolution(["pixel", "gridline"], True),
            "02m": Resolution(["pixel", "gridline"], True),
            "01m": Resolution(["gridline"], True),
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
        arc-degree, arc-minute, and arc-second respectively.

    region : str or list
        The subregion of the grid to load, in the forms of a list
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

    if registration in ("pixel", "gridline", None):
        # If None, let GMT decide on Pixel/Gridline type
        reg = f"_{registration[0]}" if registration else ""
    else:
        raise GMTInvalidInput(
            f"Invalid grid registration: '{registration}', should be either "
            "'pixel', 'gridline' or None. Default is None, where a "
            "pixel-registered grid is returned unless only the "
            "gridline-registered grid is available."
        )
    dataset = datasets[dataset_name]
    if resolution not in dataset.resolutions.keys():
        raise GMTInvalidInput(f"Invalid resolution '{resolution}'.")
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
