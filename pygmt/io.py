"""
PyGMT input/output (I/O) utilities.
"""
import xarray as xr


def process_output_grid(grid_name, tmpfile_name):
    """
    Processes the output from the GMT API to return an xarray.DataArray if
    ``grid_name`` matches ``tmpfile_name`` and return None if it does not.

    Parameters
    ----------
    grid_name : str
        The name of the output netCDF file with extension .nc to store the grid
        in.
    tmpfile_name : str
        The name attribute from a GMTTempFile instance.

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    if grid_name == tmpfile_name:  # Implies user did not set outgrid, return DataArray
        with xr.open_dataarray(grid_name) as dataarray:
            result = dataarray.load()
            _ = result.gmt  # load GMTDataArray accessor information
    else:
        result = None  # Implies user set an outgrid, return None

    return result
