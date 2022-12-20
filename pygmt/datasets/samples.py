"""
Functions to load sample data.
"""
import warnings

import pandas as pd
from pygmt.exceptions import GMTInvalidInput
from pygmt.io import load_dataarray
from pygmt.src import which


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
    names = {
        "bathymetry": "Table of ship bathymetric observations off Baja California",
        "earth_relief_holes": "Regional 20 arc-minutes Earth relief grid with holes",
        "fractures": "Table of hypothetical fracture lengths and azimuths",
        "hotspots": "Table of locations, names, and symbol sizes of hotpots from "
        " Mueller et al., 1993",
        "japan_quakes": "Table of earthquakes around Japan from NOAA NGDC database",
        "mars_shape": "Table of topographic signature of the hemispheric dichotomy of "
        " Mars from Smith and Zuber (1996)",
        "maunaloa_co2": "Table of CO2 readings from Mauna Loa",
        "notre_dame_topography": "Table 5.11 in Davis: Statistics and Data Analysis in Geology",
        "ocean_ridge_points": "Table of ocean ridge points for the entire world",
        "rock_compositions": "Table of rock sample compositions",
        "usgs_quakes": "Table of global earthquakes from the USGS",
    }
    return names


def load_sample_data(name):
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
    :class:`pandas.DataFrame` or :class:`xarray.DataArray`
        Sample dataset loaded as a pandas.DataFrame for tabular data or
        xarray.DataArray for raster data.

    See Also
    --------
    list_sample_data : Report datasets available for tests and documentation
        examples.
    """
    names = list_sample_data()
    if name not in names:
        raise GMTInvalidInput(f"Invalid dataset name '{name}'.")

    # Dictionary of public load functions for backwards compatibility
    load_func_old = {
        "bathymetry": load_sample_bathymetry,
        "fractures": load_fractures_compilation,
        "hotspots": load_hotspots,
        "japan_quakes": load_japan_quakes,
        "mars_shape": load_mars_shape,
        "ocean_ridge_points": load_ocean_ridge_points,
        "usgs_quakes": load_usgs_quakes,
    }

    # Dictionary of private load functions
    load_func = {
        "rock_compositions": _load_rock_sample_compositions,
        "earth_relief_holes": _load_earth_relief_holes,
        "maunaloa_co2": _load_maunaloa_co2,
        "notre_dame_topography": _load_notre_dame_topography,
    }

    if name in load_func_old:
        data = load_func_old[name](suppress_warning=True)
    elif name in load_func:
        data = load_func[name]()

    return data


def load_japan_quakes(**kwargs):
    """
    (Deprecated) Load a table of earthquakes around Japan as a
    pandas.DataFrame.

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_data(name="japan_quakes")`` and will be removed in
       v0.9.0.

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

    if "suppress_warning" not in kwargs:
        warnings.warn(
            "This function has been deprecated since v0.6.0 and will be "
            "removed in v0.9.0. Please use "
            "load_sample_data(name='japan_quakes') instead.",
            category=FutureWarning,
            stacklevel=2,
        )

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


def load_ocean_ridge_points(**kwargs):
    """
    (Deprecated) Load a table of ocean ridge points for the entire world as a
    pandas.DataFrame.

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_data(name="ocean_ridge_points")`` and will be removed in
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

    if "suppress_warning" not in kwargs:
        warnings.warn(
            "This function has been deprecated since v0.6.0 and will be removed "
            "in v0.9.0. Please use load_sample_data(name='ocean_ridge_points') "
            "instead.",
            category=FutureWarning,
            stacklevel=2,
        )

    fname = which("@ridge.txt", download="c")
    data = pd.read_csv(
        fname, sep=r"\s+", names=["longitude", "latitude"], skiprows=1, comment=">"
    )
    return data


def load_sample_bathymetry(**kwargs):
    """
    (Deprecated) Load a table of ship observations of bathymetry off Baja
    California as a pandas.DataFrame.

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_data(name="bathymetry")`` and will be removed in
       v0.9.0.

    This is the ``@tut_ship.xyz`` dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data : pandas.DataFrame
        The data table. Columns are longitude, latitude, and bathymetry.
    """

    if "suppress_warning" not in kwargs:
        warnings.warn(
            "This function has been deprecated since v0.6.0 and will be "
            "removed in v0.9.0. Please use "
            "load_sample_data(name='bathymetry') instead.",
            category=FutureWarning,
            stacklevel=2,
        )
    fname = which("@tut_ship.xyz", download="c")
    data = pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "bathymetry"]
    )
    return data


def load_usgs_quakes(**kwargs):
    """
    (Deprecated) Load a table of global earthquakes from the USGS as a
    pandas.DataFrame.

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_data(name="usgs_quakes")`` and will be removed in
       v0.9.0.

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

    if "suppress_warning" not in kwargs:
        warnings.warn(
            "This function has been deprecated since v0.6.0 and will be "
            "removed in v0.9.0. Please use "
            "load_sample_data(name='usgs_quakes') instead.",
            category=FutureWarning,
            stacklevel=2,
        )
    fname = which("@usgs_quakes_22.txt", download="c")
    data = pd.read_csv(fname)
    return data


def load_fractures_compilation(**kwargs):
    """
    (Deprecated) Load a table of fracture lengths and azimuths as
    hypothetically digitized from geological maps as a pandas.DataFrame.

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_data(name="fractures")`` and will be removed in
       v0.9.0.

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

    if "suppress_warning" not in kwargs:
        warnings.warn(
            "This function has been deprecated since v0.6.0 and will be "
            "removed in v0.9.0. Please use "
            "load_sample_data(name='fractures') instead.",
            category=FutureWarning,
            stacklevel=2,
        )
    fname = which("@fractures_06.txt", download="c")
    data = pd.read_csv(fname, header=None, sep=r"\s+", names=["azimuth", "length"])
    return data[["length", "azimuth"]]


def load_hotspots(**kwargs):
    """
    (Deprecated) Load a table with the locations, names, and suggested symbol
    sizes of hotspots.

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_data(name="hotspots")`` and will be removed in
       v0.9.0.

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

    if "suppress_warning" not in kwargs:
        warnings.warn(
            "This function has been deprecated since v0.6.0 and will be "
            "removed in v0.9.0. Please use "
            "load_sample_data(name='hotspots') instead.",
            category=FutureWarning,
            stacklevel=2,
        )
    fname = which("@hotspots.txt", download="c")
    columns = ["longitude", "latitude", "symbol_size", "place_name"]
    data = pd.read_table(filepath_or_buffer=fname, sep="\t", skiprows=3, names=columns)
    return data


def load_mars_shape(**kwargs):
    """
    (Deprecated) Load a table of data for the shape of Mars.

    .. warning:: Deprecated since v0.6.0. This function has been replaced with
       ``load_sample_data(name="mars_shape")`` and will be removed in
       v0.9.0.

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

    if "suppress_warning" not in kwargs:
        warnings.warn(
            "This function has been deprecated since v0.6.0 and will be "
            "removed in v0.9.0. Please use "
            "load_sample_data(name='mars_shape') instead.",
            category=FutureWarning,
            stacklevel=2,
        )
    fname = which("@mars370d.txt", download="c")
    data = pd.read_csv(
        fname, sep="\t", header=None, names=["longitude", "latitude", "radius(m)"]
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
    return pd.read_csv(fname, sep=r"\s+", header=None, names=["x", "y", "z"])


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
        fname, header=None, skiprows=1, sep=r"\s+", names=["date", "co2_ppm"]
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
