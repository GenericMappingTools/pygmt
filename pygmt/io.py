"""
PyGMT input/output (I/O) utilities.
"""

import warnings

import xarray as xr


# TODO(PyGMT>=0.20.0): Remove pygmt.io.load_dataarray
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

    .. deprecated:: v0.16.0
       The 'pygmt.io.load_dataarray' function will be removed in v0.20.0. Please use
       `xarray.load_dataarray(..., engine='gmt', raster_kind='grid')` instead if you
       were reading grids using the engine='netcdf'; otherwise use `raster_kind='image'`
       if you were reading multi-band images using engine='rasterio'.

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
    msg = (
        "The 'pygmt.io.load_dataarray' function will be removed in v0.20.0. Please use "
        "`xarray.load_dataarray(..., engine='gmt', raster_kind='grid')` instead if you "
        "were reading grids using the engine='netcdf'; otherwise use "
        "`raster_kind='image'` if you were reading multi-band images using "
        "engine='rasterio'."
    )
    warnings.warn(message=msg, category=FutureWarning, stacklevel=1)

    if "cache" in kwargs:
        msg = "'cache' has no effect in this context."
        raise TypeError(msg)

    with xr.open_dataarray(filename_or_obj, **kwargs) as dataarray:
        result = dataarray.load()
        _ = result.gmt  # load GMTDataArray accessor information

    return result
