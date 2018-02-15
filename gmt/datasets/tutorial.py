"""
Functions to load sample data from the GMT tutorials.
"""
import pandas as pd

from .. import which


def load_japan_quakes():
    """
    Load a table of earthquakes around Japan as a pandas.Dataframe.

    Data is from the NOAA NGDC database. This is the ``@tut_quakes.ngdc``
    dataset used in the GMT tutorials.

    The data are downloaded to a cache directory (usually ``~/.gmt/cache``) the
    first time you invoke this function. Afterwards, it will load the data from
    the cache. So you'll need an internet connection the first time around.

    Returns
    -------
    data :  pandas.Dataframe
        The data table. Columns are year, month, day, latitude, longitude,
        depth (in km), and magnitude of the earthquakes.

    """
    fname = which('@tut_quakes.ngdc', download='c')
    data = pd.read_table(fname, header=1, sep=r'\s+')
    data.columns = ['year', 'month', 'day', 'latitude', 'longitude',
                    'depth_km', 'magnitude']
    return data
