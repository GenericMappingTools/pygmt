"""
Functions to load sample data.
"""

from collections.abc import Callable
from typing import Literal, NamedTuple

import pandas as pd
import xarray as xr
from pygmt.exceptions import GMTInvalidInput
from pygmt.io import load_dataarray
from pygmt.src import which


def _load_japan_quakes() -> pd.DataFrame:
    """
    Load a table of earthquakes around Japan.

    The data are from the NOAA NGDC database.

    Returns
    -------
    data
        The data table. The column names are "year", "month", "day", "latitude",
        "longitude", "depth_km", and "magnitude" of the earthquakes.
    """
    fname = which("@tut_quakes.ngdc", download="c")
    return pd.read_csv(
        fname,
        header=1,
        sep=r"\s+",
        names=[
            "year",
            "month",
            "day",
            "latitude",
            "longitude",
            "depth_km",
            "magnitude",
        ],
    )


def _load_ocean_ridge_points() -> pd.DataFrame:
    """
    Load a table of ocean ridge points for the entire world.

    Returns
    -------
    data
        The data table. The column names are "longitude" and "latitude".
    """
    fname = which("@ridge.txt", download="c")
    return pd.read_csv(
        fname,
        sep=r"\s+",
        names=["longitude", "latitude"],
        skiprows=1,
        comment=">",
    )


def _load_baja_california_bathymetry() -> pd.DataFrame:
    """
    Load a table of ship observations of bathymetry off Baja California.

    Returns
    -------
    data
        The data table. The column names are "longitude", "latitude", and "bathymetry".
    """
    fname = which("@tut_ship.xyz", download="c")
    return pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "bathymetry"]
    )


def _load_usgs_quakes() -> pd.DataFrame:
    """
    Load a table of global earthquakes from the USGS.

    Returns
    -------
    data
        The data table. Use ``print(data.describe())`` to see the available columns.
    """
    fname = which("@usgs_quakes_22.txt", download="c")
    return pd.read_csv(fname)


def _load_fractures_compilation() -> pd.DataFrame:
    """
    Load a table of fracture lengths and azimuths as hypothetically digitized from
    geological maps.

    Returns
    -------
    data
        The data table. The column names are "length" and "azimuth" of the fractures.
    """
    fname = which("@fractures_06.txt", download="c")
    data = pd.read_csv(fname, header=None, sep=r"\s+", names=["azimuth", "length"])
    return data[["length", "azimuth"]]


def _load_hotspots() -> pd.DataFrame:
    """
    Load a table with the locations, names, and suggested symbol sizes of hotspots.

    The data are from Mueller, Royer, and Lawver, 1993, Geology, vol. 21, pp. 275-278.
    The main 5 hotspots used by Doubrovine et al. [2012] have symbol sizes twice the
    size of all other hotspots.

    Returns
    -------
    data
        The data table. The column names are "longitude", "latitude", "symbol_size", and
        "place_name".
    """
    fname = which("@hotspots.txt", download="c")
    return pd.read_csv(
        fname,
        sep="\t",
        skiprows=3,
        names=["longitude", "latitude", "symbol_size", "place_name"],
    )


def _load_mars_shape() -> pd.DataFrame:
    """
    Load a table of data for the shape of Mars.

    Data and information are from Smith, D. E., and M. T. Zuber (1996), The shape of
    Mars and the topographic signature of the hemispheric dichotomy.

    Returns
    -------
    data
        The data table. The column names are "longitude", "latitude", and "radius_m".
    """
    fname = which("@mars370d.txt", download="c")
    return pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "radius_m"]
    )


def _load_rock_sample_compositions() -> pd.DataFrame:
    """
    Load a table of rock sample compositions.

    Returns
    -------
    data
        The data table. The column names are "limestone", "water", "air", and
        "permittivity".
    """
    fname = which("@ternary.txt", download="c")
    return pd.read_csv(
        fname,
        sep=r"\s+",
        header=None,
        names=["limestone", "water", "air", "permittivity"],
    )


def _load_notre_dame_topography() -> pd.DataFrame:
    """
    Load a table of Notre Dame topography.

    The data is Table 5.11 in Davis: Statistics and Data Analysis in Geology.

    Returns
    -------
    data
        The data table. The column names are "x", "y", and "z".
    """
    fname = which("@Table_5_11.txt", download="c")
    return pd.read_csv(fname, sep=r"\s+", header=None, names=["x", "y", "z"])


def _load_maunaloa_co2() -> pd.DataFrame:
    """
    Load a table of CO2 values from Mauna Loa.

    Returns
    -------
    data
        The data table. The column names are "date" and "co2_ppm".
    """
    fname = which("@MaunaLoa_CO2.txt", download="c")
    return pd.read_csv(
        fname, header=None, skiprows=1, sep=r"\s+", names=["date", "co2_ppm"]
    )


def _load_earth_relief_holes() -> xr.DataArray:
    """
    Load the earth relief grid with some holes.

    Returns
    -------
    grid
        The Earth relief grid. Coordinates are latitude and longitude in degrees. Relief
        is in meters.
    """
    fname = which("@earth_relief_20m_holes.grd", download="c")
    return load_dataarray(fname, engine="netcdf4")


class GMTSampleData(NamedTuple):
    """
    Information of a sample dataset.

    Attributes
    ----------
    func : callable
        The function that loads the sample dataset.
    description : str
        The description of the sample dataset.
    """

    func: Callable
    description: str


datasets = {
    "bathymetry": GMTSampleData(
        func=_load_baja_california_bathymetry,
        description="Table of ship bathymetric observations off Baja California",
    ),
    "earth_relief_holes": GMTSampleData(
        func=_load_earth_relief_holes,
        description="Regional 20 arc-minutes Earth relief grid with holes",
    ),
    "fractures": GMTSampleData(
        func=_load_fractures_compilation,
        description="Table of hypothetical fracture lengths and azimuths",
    ),
    "hotspots": GMTSampleData(
        func=_load_hotspots,
        description="Table of locations, names, and symbol sizes of hotpots from "
        "Müller et al. (1993)",
    ),
    "japan_quakes": GMTSampleData(
        func=_load_japan_quakes,
        description="Table of earthquakes around Japan from the NOAA NGDC database",
    ),
    "mars_shape": GMTSampleData(
        func=_load_mars_shape,
        description="Table of topographic signature of the hemispheric dichotomy of "
        "Mars from Smith and Zuber (1996)",
    ),
    "maunaloa_co2": GMTSampleData(
        func=_load_maunaloa_co2,
        description="Table of CO2 readings from Mauna Loa",
    ),
    "notre_dame_topography": GMTSampleData(
        func=_load_notre_dame_topography,
        description="Table 5.11 in Davis: Statistics and Data Analysis in Geology",
    ),
    "ocean_ridge_points": GMTSampleData(
        func=_load_ocean_ridge_points,
        description="Table of ocean ridge points for the entire world",
    ),
    "rock_compositions": GMTSampleData(
        func=_load_rock_sample_compositions,
        description="Table of rock sample compositions",
    ),
    "usgs_quakes": GMTSampleData(
        func=_load_usgs_quakes,
        description="Table of earthquakes from the USGS",
    ),
}


def list_sample_data() -> dict[str, str]:
    """
    Report datasets available for tests and documentation examples.

    Returns
    -------
    dict
        Names and short descriptions of available sample datasets.

    See Also
    --------
    load_sample_data : Load an example dataset from the GMT server.
    """
    return {name: dataset.description for name, dataset in datasets.items()}


def load_sample_data(
    name: Literal[
        "bathymetry",
        "earth_relief_holes",
        "fractures",
        "hotspots",
        "japan_quakes",
        "mars_shape",
        "maunaloa_co2",
        "notre_dame_topography",
        "ocean_ridge_points",
        "rock_compositions",
        "usgs_quakes",
    ],
) -> pd.DataFrame | xr.DataArray:
    """
    Load an example dataset from the GMT server.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the first
    time you invoke this function. Afterwards, it will load the data from the cache. So
    you'll need an internet connection the first time around.

    Parameters
    ----------
    name
        Name of the dataset to load.

    Returns
    -------
    data
        Sample dataset loaded as a :class:`pandas.DataFrame` for tabular data or
        :class:`xarray.DataArray` for raster data.

    See Also
    --------
    list_sample_data : Report datasets available for tests and documentation examples.

    Examples
    --------
    >>> from pprint import pprint
    >>> from pygmt.datasets import list_sample_data, load_sample_data
    >>> # use list_sample_data to see the available datasets
    >>> pprint(list_sample_data(), width=120)
    {'bathymetry': 'Table of ship bathymetric observations off Baja California',
     'earth_relief_holes': 'Regional 20 arc-minutes Earth relief grid with holes',
     'fractures': 'Table of hypothetical fracture lengths and azimuths',
     'hotspots': 'Table of locations, names, and symbol sizes of hotpots from Müller et al. (1993)',
     'japan_quakes': 'Table of earthquakes around Japan from the NOAA NGDC database',
     'mars_shape': 'Table of topographic signature of the hemispheric dichotomy of Mars from Smith and Zuber (1996)',
     'maunaloa_co2': 'Table of CO2 readings from Mauna Loa',
     'notre_dame_topography': 'Table 5.11 in Davis: Statistics and Data Analysis in Geology',
     'ocean_ridge_points': 'Table of ocean ridge points for the entire world',
     'rock_compositions': 'Table of rock sample compositions',
     'usgs_quakes': 'Table of earthquakes from the USGS'}
    >>> # load the sample bathymetry dataset
    >>> data = load_sample_data("bathymetry")
    """  # noqa: W505
    if name not in datasets:
        raise GMTInvalidInput(f"Invalid dataset name '{name}'.")
    return datasets[name].func()
