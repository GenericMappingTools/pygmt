"""
PyGMT input/output (I/O) utilities.
"""

import xarray as xr


def load_dataarray(filename_or_obj, **kwargs):
    """
    Open, load into memory, and close a DataArray from a file or file-like object
    containing a single data variable.

    This is a thin wrapper around :py:func:`xarray.open_dataarray`. It differs
    from :py:func:`xarray.open_dataarray` in that it loads the DataArray into
    memory, gets GMT specific metadata about the grid via
    :py:meth:`GMTDataArrayAccessor`, closes the file, and returns the
    DataArray. In contrast, :py:func:`xarray.open_dataarray` keeps the file
    handle open and lazy loads its contents. All parameters are passed directly
    to :py:func:`xarray.open_dataarray`. See that documentation for further
    details.

    Parameters
    ----------
    filename_or_obj : str or pathlib.Path or file-like or DataStore
        Strings and Path objects are interpreted as a path to a netCDF file
        or an OpenDAP URL and opened with python-netCDF4, unless the filename
        ends with .gz, in which case the file is gunzipped and opened with
        scipy.io.netcdf (only netCDF3 supported). Byte-strings or file-like
        objects are opened by scipy.io.netcdf (netCDF3) or h5py (netCDF4/HDF).

    Returns
    -------
    datarray : xarray.DataArray
        The newly created DataArray.

    See Also
    --------
    xarray.open_dataarray
    """
    if "cache" in kwargs:
        raise TypeError("cache has no effect in this context")

    with xr.open_dataarray(filename_or_obj, **kwargs) as dataarray:
        result = dataarray.load()
        _ = result.gmt  # load GMTDataArray accessor information

    return result
