"""
Functions to load sample data.
"""
import textwrap
from typing import Callable, NamedTuple

import pandas as pd
from pygmt.exceptions import GMTInvalidInput
from pygmt.io import load_dataarray
from pygmt.src import which


def _load_japan_quakes():
    """
    Load a table of earthquakes around Japan as a pandas.DataFrame.

    The data are from the NOAA NGDC database.

    Returns
    -------
    data : pandas.DataFrame
        The data table. The column names are "year", "month", "day",
        "latitude", "longitude", "depth_km", and "magnitude" of the
        earthquakes.
    """
    fname = which("@tut_quakes.ngdc", download="c")
    return pd.read_csv(
        fname,
        header=1,
        delim_whitespace=True,
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


def _load_ocean_ridge_points():
    """
    Load a table of ocean ridge points for the entire world as a
    pandas.DataFrame.

    Returns
    -------
    data : pandas.DataFrame
        The data table. The column names are "longitude" and "latitude".
    """
    fname = which("@ridge.txt", download="c")
    return pd.read_csv(
        fname,
        delim_whitespace=True,
        names=["longitude", "latitude"],
        skiprows=1,
        comment=">",
    )


def _load_baja_california_bathymetry():
    """
    Load a table of ship observations of bathymetry off Baja California as a
    pandas.DataFrame.

    Returns
    -------
    data : pandas.DataFrame
        The data table. The column names are "longitude", "latitude",
        and "bathymetry".
    """

    fname = which("@tut_ship.xyz", download="c")
    return pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "bathymetry"]
    )


def _load_usgs_quakes():
    """
    Load a table of global earthquakes from the USGS as a pandas.DataFrame.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Use ``print(data.describe())`` to see the available
        columns.
    """
    fname = which("@usgs_quakes_22.txt", download="c")
    return pd.read_csv(fname)


def _load_fractures_compilation():
    """
    Load a table of fracture lengths and azimuths as hypothetically digitized
    from geological maps as a pandas.DataFrame.

    Returns
    -------
    data : pandas.DataFrame
        The data table. The column names are "length" and
        "azimuth" of the fractures.
    """

    fname = which("@fractures_06.txt", download="c")
    data = pd.read_csv(
        fname, header=None, delim_whitespace=True, names=["azimuth", "length"]
    )
    return data[["length", "azimuth"]]


def _load_hotspots():
    """
    Load a table with the locations, names, and suggested symbol sizes of
    hotspots as a pandas.DataFrame.

    The data are from Mueller, Royer, and Lawver, 1993, Geology, vol. 21,
    pp. 275-278. The main 5 hotspots used by Doubrovine et al. [2012]
    have symbol sizes twice the size of all other hotspots.

    Returns
    -------
    data : pandas.DataFrame
        The data table. The column names are "longitude", "latitude",
        "symbol_size", and "place_name".
    """

    fname = which("@hotspots.txt", download="c")
    return pd.read_csv(
        fname,
        sep="\t",
        skiprows=3,
        names=["longitude", "latitude", "symbol_size", "place_name"],
    )


def _load_mars_shape():
    """
    Load a table of data for the shape of Mars as a pandas.DataFrame.

    Data and information are from Smith, D. E., and M. T. Zuber (1996),
    The shape of Mars and the topographic signature of the hemispheric
    dichotomy.

    Returns
    -------
    data : pandas.DataFrame
        The data table with column names "longitude", "latitude", and
        "radius_m".
    """
    fname = which("@mars370d.txt", download="c")
    data = pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "radius_m"]
    )
    return data


def _load_rock_sample_compositions():
    """
    Loads a table of rock sample compositions.

    Returns
    -------
    data : pandas.DataFrame
        The data table with columns "limestone", "water", "air",
        and "permittivity".
    """

    fname = which("@ternary.txt", download="c")
    return pd.read_csv(
        fname,
        delim_whitespace=True,
        header=None,
        names=["limestone", "water", "air", "permittivity"],
    )


def _load_notre_dame_topography():
    """
    Load Table 5.11 in Davis: Statistics and Data Analysis in Geology.

    Returns
    -------
    data : pandas.DataFrame
        The data table with columns "x", "y", and "z".
    """
    fname = which("@Table_5_11.txt", download="c")
    return pd.read_csv(fname, delim_whitespace=True, header=None, names=["x", "y", "z"])


def _load_maunaloa_co2():
    """
    Load a table of CO2 values from Mauna Loa.

    Returns
    -------
    data : pandas.DataFrame
        The data table with columns "date" and "co2_ppm".
    """
    fname = which("@MaunaLoa_CO2.txt", download="c")
    return pd.read_csv(
        fname, header=None, skiprows=1, delim_whitespace=True, names=["date", "co2_ppm"]
    )


def _load_earth_relief_holes():
    """
    Loads the remote file @earth_relief_20m_holes.grd.

    Returns
    -------
    grid : :class:`xarray.DataArray`
        The Earth relief grid. Coordinates are latitude and longitude in
        degrees. Relief is in meters.
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
        "Mueller et al., 1993",
    ),
    "japan_quakes": GMTSampleData(
        func=_load_japan_quakes,
        description="Table of earthquakes around Japan from NOAA NGDC database",
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


def fmt_dataset_list(module_func):
    """
    Decorator to replace the ``{dataset_list}`` placeholder in the docstring.

    Parameters
    ----------
    module_func : function
        The function to decorate.

    Returns
    -------
    module_func
        The same *module_func* but with the docstring formatted.
    """
    # Add a new lines and 8 white spaces for formatting in the documentation
    texts = "\n        ".join(
        f'- ``"{name}"``: {dataset.description}.' for name, dataset in datasets.items()
    )

    docstrings = module_func.__doc__.format(dataset_list=texts)
    module_func.__doc__ = textwrap.dedent(docstrings)
    return module_func


def list_sample_data():
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


@fmt_dataset_list
def load_sample_data(name):
    """
    Load an example dataset from the GMT server.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Parameters
    ----------
    name : str
        Name of the dataset to load. Available datasets are:

        {dataset_list}

    Returns
    -------
    :class:`pandas.DataFrame` or :class:`xarray.DataArray`
        Sample dataset loaded as a pandas.DataFrame for tabular data or
        xarray.DataArray for raster data.

    See Also
    --------
    list_sample_data : Report datasets available for tests and documentation
        examples.
    """
    if name not in datasets:
        raise GMTInvalidInput(f"Invalid dataset name '{name}'.")
    return datasets[name].func()
