"""
Functions to load sample data.
"""
import warnings

import pandas as pd
from pygmt.exceptions import GMTInvalidInput
from pygmt.src import which


def list_sample_dataframes():
    """
    Report tabular datasets available for tests and documentation examples.

    Returns
    -------
    output : dict
        Names and short descriptions of available sample dataframes.
    """
    names = {
        "tut_quakes.ngdc": "Table of earthquakes around Japan from NOAA NGDC database",
        "ridge.txt": "Table of ocean ridge points for the entire world",
    }
    return names


def load_sample_dataframe(name):
    """
    Load an example dataset from the GMT server.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Parameters
    ----------
    name : str
        Name of the dataset to load.

    Returns
    -------
    output : pandas.DataFrame
        Tabular dataset.
    """
    names = list_sample_dataframes()
    if name not in names:
        raise GMTInvalidInput(f"Invalid dataset name '{name}'")

    fname = which("@" + name, download="c")

    if name == "tut_quakes.ngdc":
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

    if name == "ridge.txt":
        data = pd.read_csv(
            fname, sep=r"\s+", names=["longitude", "latitude"], skiprows=1, comment=">"
        )
    return data


def load_japan_quakes():
    """
    Load a table of earthquakes around Japan as a pandas.DataFrame (Deprecated)

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_dataframe(name="tut_quakes.ngdc")`` and will be removed in
       v0.9.0.

    Data is from the NOAA NGDC database. This is the ``@tut_quakes.ngdc``
    dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.
    """

    warnings.warn(
        "This function has been deprecated since v0.6.0 and will be removed "
        "in v0.9.0. Please use load_sample_dataframe(name='tut_quakes.ngdc') "
        "instead.",
        category=FutureWarning,
        stacklevel=2,
    )

    return load_sample_dataframe("tut_quakes.ngdc")


def load_ocean_ridge_points():
    """
    Load a table of ocean ridge points for the entire world as a
    pandas.DataFrame (Deprecated).

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_dataframe(name="ridge.txt")`` and will be removed in
       v0.9.0.

    This is the ``@ridge.txt`` dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Columns are longitude and latitude.
    """
    warnings.warn(
        "This function has been deprecated since v0.6.0 and will be removed "
        "in v0.9.0. Please use load_sample_dataframe(name='ridge.txt') "
        "instead.",
        category=FutureWarning,
        stacklevel=2,
    )

    return load_sample_dataframe("ridge.txt")


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


def load_hotspots():
    """
    Load a table with the locations, names, and suggested symbol sizes of
    hotspots.

    This is the ``@hotspots.txt`` dataset used in the GMT tutorials, with data
    from Mueller, Royer, and Lawver, 1993, Geology, vol. 21, pp. 275-278. The
    main 5 hotspots used by Doubrovine et al. [2012] have symbol sizes twice
    the size of all other hotspots.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table with columns "longitude", "latitude", "symbol_size", and
        "placename".
    """
    fname = which("@hotspots.txt", download="c")
    columns = ["longitude", "latitude", "symbol_size", "place_name"]
    data = pd.read_table(filepath_or_buffer=fname, sep="\t", skiprows=3, names=columns)
    return data


def load_mars_shape():
    """
    Load a table of data for the shape of Mars.

    This is the ``@mars370d.txt`` dataset used in GMT examples, with data and
    information from Smith, D. E., and M. T. Zuber (1996), The shape of Mars
    and the topographic signature of the hemispheric dichotomy. Data columns
    are "longitude," "latitude", and "radius (meters)."

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table with columns "longitude", "latitude", and "radius(m)".
    """
    fname = which("@mars370d.txt", download="c")
    data = pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "radius(m)"]
    )
    return data
