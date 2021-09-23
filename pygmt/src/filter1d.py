"""
filter1d - Time domain filtering of 1-D data tables
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
    E="end",
    F="filter",
)
def filter1d(data, output_type="pandas", outfile=None, **kwargs):
    r"""
    Time domain filtering of 1-D data tables

    Filter a general time domain for multiple column time
    series data. The user specifies which column is the time (i.e., the
    independent variable). The fastest operation
    occurs when the input time series are equally spaced and have no gaps or
    outliers and the special options are not needed.
    Read a table and output as a :class:`numpy.ndarray`,
    :class:`pandas.DataFrame`, or ASCII file.

    Full option list at :gmt-docs:`filter1d.html`

    {aliases}

    Parameters
    ----------.
    output_type : str
        Determine the format the xyz data will be returned in [Default is
        ``pandas``]:

            - ``numpy`` - :class:`numpy.ndarray`
            - ``pandas``- :class:`pandas.DataFrame`
            - ``file`` - ASCII file (requires ``outfile``)
    outfile : str
        The file name for the output ASCII file.

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
    if "F" not in kwargs:
        raise GMTInvalidInput("""Pass a required argument to 'filter'.""")
    if output_type not in ["numpy", "pandas", "file"]:
        raise GMTInvalidInput(
            """Must specify format as either numpy, pandas, or file."""
        )
    if outfile is not None and output_type != "file":
        msg = (
            f"Changing `output_type` of filter1d from '{output_type}' to 'file' "
            "since `outfile` parameter is set. Please use `output_type='file'` "
            "to silence this warning."
        )
        warnings.warn(msg, category=RuntimeWarning, stacklevel=2)
        output_type = "file"
    elif output_type == "file" and outfile is None:
        raise GMTInvalidInput("""Must specify outfile for ASCII output.""")

    with GMTTempFile() as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if outfile is None:
                    outfile = tmpfile.name
                arg_str = " ".join([infile, build_arg_string(kwargs), "->" + outfile])
                lib.call_module("filter1d", arg_str)

        # Read temporary csv output to a pandas table
        if outfile == tmpfile.name:  # if user did not set outfile, return pd.DataFrame
            result = pd.read_csv(tmpfile.name, sep="\t", comment=">")
        elif outfile != tmpfile.name:  # return None if outfile set, output in outfile
            result = None

        if output_type == "numpy":
            result = result.to_numpy()
    return result
