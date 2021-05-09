"""
Functions to load sample data.
"""
import pandas as pd
from pygmt.src import which


def load_japan_quakes():
    """
    Load a table of earthquakes around Japan as a pandas.DataFrame.

    Data is from the NOAA NGDC database. This is the ``@tut_quakes.ngdc``
    dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Columns are year, month, day, latitude, longitude,
        depth (in km), and magnitude of the earthquakes.
    """
    fname = which("@tut_quakes.ngdc", download="c")
    data = pd.read_csv(fname, header=1, sep=r"\s+")
    data.columns = [
        "year",
        "month",
        "day",
        "latitude",
        "longitude",
        "depth_km",
        "magnitude",
    ]
    return data


def load_ocean_ridge_points():
    """
    Load a table of ocean ridge points for the entire world as a
    pandas.DataFrame.

    This is the ``@ridge.txt`` dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Columns are longitude and latitude.
    """
    fname = which("@ridge.txt", download="c")
    data = pd.read_csv(
        fname, sep=r"\s+", names=["longitude", "latitude"], skiprows=1, comment=">"
    )
    return data


def load_sample_bathymetry():
    """
    Load a table of ship observations of bathymetry off Baja California as a
    pandas.DataFrame.

    This is the ``@tut_ship.xyz`` dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Columns are longitude, latitude, and bathymetry.
    """
    fname = which("@tut_ship.xyz", download="c")
    data = pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "bathymetry"]
    )
    return data


def load_usgs_quakes():
    """
    Load a table of global earthquakes form the USGS as a pandas.DataFrame.

    This is the ``@usgs_quakes_22.txt`` dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Use ``print(data.describe())`` to see the available
        columns.
    """
    fname = which("@usgs_quakes_22.txt", download="c")
    data = pd.read_csv(fname)
    return data


def load_fractures_compilation():
    """
    Load a table of fracture lengths and azimuths as hypothetically digitized
    from geological maps as a pandas.DataFrame.

    This is the ``@fractures_06.txt`` dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Use ``print(data.describe())`` to see the available
        columns.
    """
    fname = which("@fractures_06.txt", download="c")
    data = pd.read_csv(fname, header=None, sep=r"\s+", names=["azimuth", "length"])
    return data[["length", "azimuth"]]
