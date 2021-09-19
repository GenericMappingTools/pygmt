"""
grd2xyz - Convert grid to data table
"""
import warnings

import pandas as pd
import xarray as xr
from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)


@fmt_docstring
@use_alias(
    R="region",
    V="verbose",
)
@kwargs_to_strings(R="sequence")
def grd2xyz(grid, output_type="pandas", outfile=None, **kwargs):
    r"""
    Convert grid to data table.

    Read a grid and output xyz-triplets as a :class:`numpy.ndarray`,
    :class:`pandas.DataFrame`, or ASCII file.

    Full option list at :gmt-docs:`grd2xyz.html`

    {aliases}

    Parameters
    ----------
    grid : str or xarray.DataArray
        The file name of the input grid or the grid loaded as a
        :class:`xarray.DataArray`. This is the only required parameter.
    output_type : str
        Determine the format the xyz data will be returned in [Default is
        ``pandas``]:

            - ``numpy`` - :class:`numpy.ndarray`
            - ``pandas``- :class:`pandas.DataFrame`
            - ``file`` - ASCII file (requires ``outfile``)
    outfile : str
        The file name for the output ASCII file.
    {R}
        Adding `region` will select a subsection of the grid. If this
        subsection exceeds the boundaries of the grid, only the common region
        will be output.
    {V}

    Returns
    -------
    ret : pandas.DataFrame or numpy.ndarray or None
        Return type depends on ``outfile`` and ``output_type``:

        - None if ``outfile`` is set (output will be stored in file set by
          ``outfile``)
        - :class:`pandas.DataFrame` or :class:`numpy.ndarray` if ``outfile`` is
          not set (depends on ``output_type`` [Default is
          :class:`pandas.DataFrame`])

    """
    if output_type not in ["numpy", "pandas", "file"]:
        raise GMTInvalidInput(
            "Must specify `output_type` either as 'numpy', 'pandas' or 'file'."
        )

    if outfile is not None and output_type != "file":
        msg = (
            f"Changing `output_type` of grd2xyz from '{output_type}' to 'file' "
            "since `outfile` parameter is set. Please use `output_type='file'` "
            "to silence this warning."
        )
        warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
        output_type = "file"
    elif outfile is None and output_type == "file":
        raise GMTInvalidInput("Must specify `outfile` for ASCII output.")

    if "o" not in kwargs:  # Set default column names if not specified
        # Set the default column names for the pandas dataframe header
        dataframe_header = ["x", "y", "z"]
        # Let output pandas column names match input DataArray dimension names
        if isinstance(grid, xr.DataArray) and output_type == "pandas":
            # Reverse the dims because it is rows, columns ordered.
            dataframe_header = [grid.dims[1], grid.dims[0], grid.name]

    with GMTTempFile() as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="raster", data=grid)
            with file_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([infile, build_arg_string(kwargs), "->" + outfile])
                lib.call_module("grd2xyz", arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            if "o" not in kwargs:
                result = pd.read_csv(
                    tmpfile.name, sep="\t", names=dataframe_header, comment=">"
                )
            else:
                result = pd.read_csv(tmpfile.name, sep="\t", comment=">")
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

        if output_type == "numpy":
            result = result.to_numpy()
    return result
